# BruteGuard — Brute-Force Attack & Defense Simulator

A beginner-friendly cybersecurity mini project based on **Unit 5: Cyber Crime and Information Security**. It demonstrates a brute-force password attack scenario and simple defensive controls.

## What the project demonstrates

1. **Login attempt** — accepts username and password.
2. **Failure detection** — records invalid login attempts.
3. **Temporary account lock** — after 5 failed attempts, the account is locked for 30 seconds.
4. **Security alert** — a brute-force alert is created when the threshold is reached.
5. **Security log** — login activity is recorded with time, event, status, and source IP.
6. **Dashboard** — shows the current protection state and security activity.

## Demo credentials

- Username: `admin`
- Password: `admin123`

These credentials are intentionally simple for demonstration. Do not use them for a real application.

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

Open `http://127.0.0.1:5000`.

## Deployment

The project includes `render.yaml` and `gunicorn` in `requirements.txt` for a simple Render deployment.

## Important limitation

This is an educational simulator. The login state and security logs are stored in application memory, so they reset when the application restarts or is redeployed. A production system should use a database, password hashing, persistent rate limiting, secure secrets, and stronger authentication controls.
