from datetime import datetime, timezone
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "bruteguard-demo-secret-change-in-production"

# Demo credentials for the college project.
USERNAME = "admin"
PASSWORD = "admin123"
MAX_ATTEMPTS = 5
LOCK_SECONDS = 30

failed_attempts = 0
locked_until = None
security_logs = []


def now():
    return datetime.now(timezone.utc)


def client_ip():
    forwarded = request.headers.get("X-Forwarded-For")
    return (forwarded.split(",")[0].strip() if forwarded else request.remote_addr) or "Unknown"


def is_locked():
    return locked_until is not None and now().timestamp() < locked_until


def remaining_lock_seconds():
    if not is_locked():
        return 0
    return max(0, int(locked_until - now().timestamp() + 0.999))


def add_log(event, status, details):
    security_logs.insert(0, {
        "time": now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "event": event,
        "status": status,
        "details": details,
        "ip": client_ip(),
    })
    del security_logs[100:]


def clear_expired_lock():
    global failed_attempts, locked_until
    if locked_until is not None and not is_locked():
        locked_until = None
        failed_attempts = 0


@app.route("/", methods=["GET", "POST"])
def login():
    global failed_attempts, locked_until

    clear_expired_lock()

    if request.method == "POST":
        if is_locked():
            return render_template(
                "login.html",
                locked=True,
                remaining=remaining_lock_seconds(),
                message="Too many failed attempts. Account temporarily locked.",
                message_type="error",
            )

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:
            failed_attempts = 0
            session.clear()
            session["logged_in"] = True
            session["username"] = username
            add_log("Successful Login", "SUCCESS", "Valid credentials accepted.")
            return redirect(url_for("dashboard"))

        failed_attempts += 1
        add_log(
            "Failed Login",
            "WARNING",
            "Invalid username or password.",
        )

        if failed_attempts >= MAX_ATTEMPTS:
            locked_until = now().timestamp() + LOCK_SECONDS
            add_log(
                "Brute-Force Alert",
                "BLOCKED",
                f"Account locked for {LOCK_SECONDS} seconds after {MAX_ATTEMPTS} failed attempts.",
            )
            return render_template(
                "login.html",
                locked=True,
                remaining=LOCK_SECONDS,
                message="Too many failed attempts. Account temporarily locked.",
                message_type="error",
            )

        return render_template(
            "login.html",
            locked=False,
            remaining=0,
            message="Incorrect username or password. Please try again.",
            message_type="error",
        )

    if is_locked():
        return render_template(
            "login.html",
            locked=True,
            remaining=remaining_lock_seconds(),
            message="Account temporarily locked because of repeated failed login attempts.",
            message_type="error",
        )

    return render_template("login.html", locked=False, remaining=0, message=None)


@app.route("/dashboard")
def dashboard():
    clear_expired_lock()

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    alert_count = sum(1 for log in security_logs if log["event"] == "Brute-Force Alert")
    successful_count = sum(1 for log in security_logs if log["status"] == "SUCCESS")
    failed_count = sum(1 for log in security_logs if log["event"] == "Failed Login")

    return render_template(
        "dashboard.html",
        username=session.get("username", USERNAME),
        logs=security_logs,
        failed_attempts=failed_attempts,
        max_attempts=MAX_ATTEMPTS,
        locked=is_locked(),
        remaining=remaining_lock_seconds(),
        alert_count=alert_count,
        successful_count=successful_count,
        failed_count=failed_count,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
