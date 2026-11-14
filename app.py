import os
import smtplib
import threading
import time
from datetime import datetime, timezone
from email.message import EmailMessage

from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, template_folder="template")

# Configure these values in your hosting provider's Environment settings.
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
MAIL_TO = os.environ.get("MAIL_TO", "")

COOLDOWN_SECONDS = 3600
BOT_WORDS = ("bot", "crawl", "spider", "slurp", "curl", "wget", "python-requests")

_last_sent = {}
_pending = set()
_lock = threading.Lock()

# Render places the app behind a trusted reverse proxy.
# Trust one forwarded address from that proxy. Do not enable this blindly
# when running behind an unknown or user-controlled proxy.
if os.environ.get("TRUST_RENDER_PROXY", "false").lower() == "true":
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)


def get_ip():
    # With TRUST_RENDER_PROXY=true, ProxyFix safely adjusts remote_addr
    # using the hosting platform's forwarded header.
    return request.remote_addr or "unknown"


def send_email(ip, user_agent, path):
    if not all((SMTP_USER, SMTP_PASS, MAIL_TO)):
        print("Email notification skipped: SMTP_USER, SMTP_PASS or MAIL_TO is missing.")
        return False

    msg = EmailMessage()
    msg["Subject"] = "New visitor on your website"
    msg["From"] = SMTP_USER
    msg["To"] = MAIL_TO
    msg.set_content(
        f"IP: {ip}\n"
        f"Time (UTC): {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S}\n"
        f"Page: {path}\n"
        f"Browser: {user_agent}\n"
    )

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as exc:
        # Avoid printing credentials or message contents.
        print("Email notification failed:", type(exc).__name__, str(exc))
        return False


def notify(ip, user_agent, path):
    if any(word in user_agent.lower() for word in BOT_WORDS):
        return

    now = time.time()
    with _lock:
        if ip in _pending:
            return
        if now - _last_sent.get(ip, 0) < COOLDOWN_SECONDS:
            return
        _pending.add(ip)

    def worker():
        success = send_email(ip, user_agent, path)
        with _lock:
            _pending.discard(ip)
            if success:
                _last_sent[ip] = time.time()

    threading.Thread(target=worker, daemon=True).start()


@app.route("/")
def index():
    notify(
        get_ip(),
        request.headers.get("User-Agent", "unknown"),
        request.path
    )
    return render_template("index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    # Local development only. Production uses Gunicorn (see Render settings).
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
