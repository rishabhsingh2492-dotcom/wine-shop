import joblib
import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from wineapp.ml import PATH
from wineapp.models import COLS, FEATURES, WineSample


class Command(BaseCommand):
    help = 'Train a RandomForestRegressor (80/20 split, seed 42) and save it with Joblib.'

    def handle(self, *args, **opts):
        df = pd.DataFrame(list(WineSample.objects.values(*COLS)))
        if len(df) < 100:
            raise CommandError('Import the dataset first: python manage.py import_wine_data')
        X, y = df[FEATURES], df['quality']  # target is excluded from X: no leakage
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1).fit(Xtr, ytr)
        pred = model.predict(Xte)  # metrics come from held-out test data only
        metrics = {'mae': round(mean_absolute_error(yte, pred), 4),
                   'rmse': round(float(np.sqrt(mean_squared_error(yte, pred))), 4),
                   'r2': round(r2_score(yte, pred), 4), 'test_rows': len(Xte), 'train_rows': len(Xtr)}
        PATH.parent.mkdir(exist_ok=True)
        joblib.dump({'model': model, 'features': FEATURES, 'metrics': metrics,
                     'name': 'RandomForestRegressor'}, PATH)
        self.stdout.write(self.style.SUCCESS(f'Model saved. Test metrics: {metrics}'))
