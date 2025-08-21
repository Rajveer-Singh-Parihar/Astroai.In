# AI Astrology

Flask-based AI astrology app generating profiles using zodiac and numerology. Smooth UI, client validation, and robust backend.

## Local Run

```bash
python app.py
```

## Deploy to Render (Free)

1. Push this folder as a GitHub repository.
2. In Render, click New > Web Service > Connect your repo.
3. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - Environment: Python 3.12
4. Click Create Web Service.

Alternatively, with the blueprint `render.yaml`: use Render Blueprints to auto-create the service.
