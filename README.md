# Legal Document Analyzer

AI-powered contract classification app built with FastAPI, React, Vite, Tailwind CSS, and scikit-learn.

## Features

- Paste legal text or upload PDF, DOCX, and TXT files.
- Predicts one of 8 MCC document classes.
- Shows confidence scores, top predictions, and document preview.
- Includes model metrics and generated evaluation artifacts.

## Model

- Classifier: LinearSVC
- Features: TF-IDF
- Classes: employment, security, purchase&ma, services&supply, shareholder, other, lease, na
- Current test accuracy: 82.14%

## Backend Setup

```powershell
cd backend
python -m pip install -r requirements.txt
copy .env.example .env
$env:PYTHONPATH="."
uvicorn app.main:app --reload
```

Backend runs at:

```txt
http://127.0.0.1:8000
```

Swagger docs:

```txt
http://127.0.0.1:8000/docs
```

## Frontend Setup

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend runs at:

```txt
http://127.0.0.1:5173
```

## API Endpoints

- `GET /`
- `GET /health`
- `GET /version`
- `POST /predict`
- `POST /predict-document`

## Deployment Notes

- Deploy frontend on Vercel.
- Deploy backend on Render.
- Set `VITE_API_URL` in Vercel to the Render backend URL.
- Set `CORS_ORIGINS` in Render to the deployed frontend URL.

## Screenshots

Place project screenshots in:

```txt
screenshots/home.png
screenshots/upload.png
screenshots/prediction.png
screenshots/swagger.png
```
