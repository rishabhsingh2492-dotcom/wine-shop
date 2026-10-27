import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-only-insecure-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = ['django.contrib.contenttypes', 'django.contrib.auth',
                  'corsheaders', 'rest_framework', 'wineapp']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware',
              'django.middleware.security.SecurityMiddleware',
              'django.middleware.common.CommonMiddleware']
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
TEMPLATES = []

# PostgreSQL (create the database first, see README)
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv('DB_NAME', 'wineiq'),
    'USER': os.getenv('DB_USER', 'postgres'),
    'PASSWORD': os.getenv('DB_PASSWORD', ''),
    'HOST': os.getenv('DB_HOST', 'localhost'),
    'PORT': os.getenv('DB_PORT', '5432')}}

# Explicit CORS for the Vite dev server
CORS_ALLOWED_ORIGINS = ['http://localhost:5173', 'http://127.0.0.1:5173']

# JSON only, no auth: intended for LOCAL DEMO. Add authentication before any public deployment.
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True

# --- Neon / hosted PostgreSQL (overrides DATABASES above when DATABASE_URL is set) ---
from urllib.parse import urlparse, unquote

_url = os.getenv('DATABASE_URL')
if _url:
    _u = urlparse(_url)
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': _u.path.lstrip('/'),
        'USER': unquote(_u.username or ''),
        'PASSWORD': unquote(_u.password or ''),
        'HOST': _u.hostname,
        'PORT': _u.port or 5432,
        'OPTIONS': {'sslmode': 'require'}}}

# --- Production settings (Render) ---
import os
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-only-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h.strip()]
CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if o.strip()]
STATIC_ROOT = BASE_DIR / 'staticfiles'

if 'corsheaders' not in INSTALLED_APPS:
    INSTALLED_APPS.append('corsheaders')
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
if 'corsheaders.middleware.CorsMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')

# ---- Production settings ----
import os, dj_database_url
SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY)
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = [".onrender.com", "localhost", "127.0.0.1"]
if os.environ.get("DATABASE_URL"):
    DATABASES = {"default": dj_database_url.config(conn_max_age=600)}
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
CORS_ALLOWED_ORIGINS = [o for o in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if o]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
