import csv
import math
from functools import reduce
from operator import or_

import numpy as np
import pandas as pd
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .ml import get_model
from .models import COLS, FEATURES, PredictionRecord, WineSample

NO_DATA = {'error': 'Dataset not imported. Run: python manage.py import_wine_data'}


def r(x, n=3):
    return round(float(x), n)


def filtered(req):
    p, qs = req.query_params, WineSample.objects.all()
    try:
        if p.get('quality'): qs = qs.filter(quality=int(p['quality']))
        if p.get('min_alcohol'): qs = qs.filter(alcohol__gte=float(p['min_alcohol']))
        if p.get('max_alcohol'): qs = qs.filter(alcohol__lte=float(p['max_alcohol']))
    except ValueError:
        raise ValidationError('quality must be an integer; alcohol bounds must be numbers.')
    if p.get('search'):
        try:
            v = float(p['search'])
        except ValueError:
            raise ValidationError('search must be a number (matches any column exactly).')
        qs = qs.filter(reduce(or_, [Q(**{c: v}) for c in COLS]))
    sort = p.get('sort', 'id')
    if sort.lstrip('-') not in COLS + ['id']:
        raise ValidationError('Invalid sort column.')
    return qs.order_by(sort)


@api_view(['GET'])
def health(req):
    m = get_model()
    return Response({'status': 'ok', 'samples': WineSample.objects.count(),
                     'dataset_ready': WineSample.objects.exists(), 'model_ready': m is not None,
                     'model_metrics': m['metrics'] if m else None})


@api_view(['GET'])
def dataset(req):
    qs = filtered(req)
    try:
        page = max(1, int(req.query_params.get('page', 1)))
    except ValueError:
        raise ValidationError('page must be an integer.')
    size, total = 25, qs.count()
    rows = list(qs[(page - 1) * size: page * size].values('id', *COLS))
    return Response({'count': total, 'page': page, 'pages': max(1, math.ceil(total / size)), 'results': rows})


@api_view(['GET'])
def export(req):
    res = HttpResponse(content_type='text/csv')
    res['Content-Disposition'] = 'attachment; filename="wineiq_filtered.csv"'
    w = csv.writer(res)
    w.writerow(COLS)
    for row in filtered(req).values_list(*COLS).iterator():
        w.writerow(row)
    return res


@api_view(['GET'])
def analysis(req):
    df = pd.DataFrame(list(WineSample.objects.values(*COLS)))
    if df.empty:
        return Response(NO_DATA, status=503)
    q = df['quality']
    vc = q.value_counts().sort_index()
    mode = int(q.value_counts().idxmax())
    hist, edges = np.histogram(df['alcohol'], bins=12)
    corr = df.corr()['quality'].drop('quality').sort_values()
    top = corr.abs().idxmax()
    stats = [{'column': c, 'mean': r(df[c].mean()), 'median': r(df[c].median()), 'std': r(df[c].std()),
              'min': r(df[c].min()), 'q1': r(df[c].quantile(.25)), 'q3': r(df[c].quantile(.75)),
              'max': r(df[c].max())} for c in COLS]
    return Response({
        'summary': {'samples': len(df), 'mean_quality': r(q.mean(), 2), 'mode_quality': mode,
                    'features': len(FEATURES), 'missing': int(df.isna().sum().sum()),
                    'duplicates': int(df.duplicated().sum())},
        'text': (f"Across {len(df)} samples, quality ranges {q.min()}-{q.max()} (mean {q.mean():.2f}); "
                 f"score {mode} is most common. {top} has the strongest linear correlation with quality "
                 f"(r = {corr[top]:.2f}). This is association, not proof of cause."),
        'quality_distribution': [{'quality': int(k), 'count': int(v)} for k, v in vc.items()],
        'alcohol_histogram': [{'bin': f'{edges[i]:.1f}', 'count': int(hist[i])} for i in range(len(hist))],
        'alcohol_by_quality': [{'quality': int(k), 'mean_alcohol': r(v)} for k, v in
                               df.groupby('quality')['alcohol'].mean().items()],
        'correlations': [{'feature': k, 'r': r(v)} for k, v in corr.items()],
        'stats': stats})


@api_view(['POST'])
def predict(req):
    bundle = get_model()
    if bundle is None:
        return Response({'error': 'Model not trained. Run: python manage.py train_wine_model'}, status=503)
    vals, errs = {}, {}
    for f in FEATURES:
        try:
            v = float(req.data.get(f))
            if not math.isfinite(v) or v < 0:
                raise ValueError
            vals[f] = v
        except (TypeError, ValueError):
            errs[f] = 'Enter a finite, non-negative number.'
    if errs:
        return Response({'errors': errs}, status=400)
    X = pd.DataFrame([vals])[bundle['features']]  # exact training feature order
    raw = float(bundle['model'].predict(X)[0])
    score = int(min(10, max(0, round(raw))))
    rec = PredictionRecord.objects.create(features=vals, predicted_raw=raw, predicted_score=score,
                                          model_name=bundle['name'])
    return Response({'id': rec.id, 'predicted_score': score, 'predicted_raw': round(raw, 3),
                     'model': bundle['name'], 'metrics': bundle['metrics'],
                     'created_at': rec.created_at,
                     'note': 'Estimate from a statistical model, not a laboratory measurement.'}, status=201)


@api_view(['GET'])
def predictions(req):
    rows = PredictionRecord.objects.all()[:50]
    return Response([{'id': p.id, 'predicted_score': p.predicted_score, 'predicted_raw': round(p.predicted_raw, 3),
                      'model': p.model_name, 'created_at': p.created_at, 'features': p.features} for p in rows])
