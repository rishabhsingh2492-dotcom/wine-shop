import joblib
from django.conf import settings

PATH = settings.BASE_DIR / 'ml_models' / 'wine_model.joblib'
_bundle = None


def get_model():
    """Load the trained bundle once and cache it. Returns None if not trained yet."""
    global _bundle
    if _bundle is None and PATH.exists():
        _bundle = joblib.load(PATH)
    return _bundle
