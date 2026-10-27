import io
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from wineapp.models import COLS, WineSample

URL = 'https://archive.ics.uci.edu/static/public/186/wine+quality.zip'


class Command(BaseCommand):
    help = 'Import winequality-red.csv (downloads it from UCI if backend/data/ has no copy).'

    def add_arguments(self, parser):
        parser.add_argument('--csv', help='Path to winequality-red.csv')

    def handle(self, *args, **opts):
        path = Path(opts['csv']) if opts['csv'] else settings.BASE_DIR / 'data' / 'winequality-red.csv'
        if not path.exists():
            self.stdout.write('CSV not found, downloading from UCI...')
            try:
                with urllib.request.urlopen(URL, timeout=30) as resp:
                    z = zipfile.ZipFile(io.BytesIO(resp.read()))
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(z.read('winequality-red.csv'))
            except Exception:
                raise CommandError('Download failed. Download winequality-red.csv manually from '
                                   'https://archive.ics.uci.edu/dataset/186/wine+quality and place it in backend/data/')
        df = pd.read_csv(path, sep=None, engine='python')
        df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]
        missing = [c for c in COLS if c not in df.columns]
        if missing:
            raise CommandError(f'Missing columns: {missing}')
        total = len(df)
        df = df[COLS].apply(pd.to_numeric, errors='coerce').dropna()  # invalid rows are rejected, never filled in
        WineSample.objects.all().delete()
        WineSample.objects.bulk_create([WineSample(**{**row, 'quality': int(row['quality'])})
                                        for row in df.to_dict('records')], batch_size=500)
        self.stdout.write(self.style.SUCCESS(f'Imported {len(df)} rows, rejected {total - len(df)}.'))
