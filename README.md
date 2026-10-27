# WineIQ – React + Django + PostgreSQL

Open this `WineIQ` folder in VS Code. Use two terminals (Terminal → New Terminal).

## 0. Prerequisites
Python 3.10+, Node.js 18+, PostgreSQL. Create the database once:
```
psql -U postgres -c "CREATE DATABASE wineiq;"
```

## 1. Backend (terminal 1)
Windows PowerShell:
```
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env        # then edit DB_PASSWORD in .env
```
macOS/Linux: `python3 -m venv venv && source venv/bin/activate`, `cp .env.example .env`.

Then (same terminal):
```
python manage.py makemigrations wineapp
python manage.py migrate
python manage.py import_wine_data     # downloads winequality-red.csv from UCI, or place it in backend/data/
python manage.py train_wine_model     # trains and evaluates the model
python manage.py runserver            # http://localhost:8000/api/health/
```

## 2. Frontend (terminal 2)
```
cd frontend
npm install
npm run dev                           # http://localhost:5173
```

## API
GET /api/health/ · GET /api/analysis/ · GET /api/dataset/?page=&quality=&min_alcohol=&max_alcohol=&search=&sort=
GET /api/export/ (same filters, CSV) · POST /api/predict/ (11 numeric fields) · GET /api/predictions/

## Troubleshooting
- `password authentication failed`: fix DB_PASSWORD in backend/.env.
- Download fails: get the CSV from the UCI page and put it at backend/data/winequality-red.csv.
- Predict says model not trained: run `python manage.py train_wine_model`.
- Local demo only: no login. Do not deploy publicly without adding authentication.
