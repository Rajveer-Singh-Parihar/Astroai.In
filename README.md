# AI Astrology

AI Astrology is a lightweight Flask web app that generates zodiac-based insights, numerology interpretations, future predictions, remedies, and marriage outlook from your name and birthdate—simple, fast, and privacy‑friendly.

## Run locally
```
pip install -r requirements.txt
python "AI Astrology/app.py"
```

## Production (Render)
- Connect repo → Web Service
- Build: `pip install -r requirements.txt`
- Start: `waitress-serve --port=$PORT wsgi:application`
