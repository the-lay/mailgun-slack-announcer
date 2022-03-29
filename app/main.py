import os
import hashlib
import requests
from flask import Flask, request

SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL", "#general")

app = Flask(__name__)


@app.route("/mail-webhook", methods=["POST"])
def mail_webhook():
    print(request.form.to_dict())
    email_subject = request.form.get("subject", "[unknown]")

    # Announcement
    announcement = requests.post(
        url="https://slack.com/api/chat.postMessage",
        data={
            "token": SLACK_API_TOKEN,
            "channel": SLACK_CHANNEL,
            "parse": "full",
            "text": f"Sender: {request.form.get('from', request.form.get('sender', '[unknown]'))}\n"
            f"To: {request.form.get('recipient', '[unknown]')}\n"
            f"Time: {request.form.get('recipient', '[unknown]')}\n"
            f"Subject: {request.form.get('subject', '[unknown]')}",
        },
    )

    # Actual email content
    content = requests.post(
        url="https://slack.com/api/chat.postMessage",
        data={
            "token": SLACK_API_TOKEN,
            "channel": SLACK_CHANNEL,
            "thread_ts": announcement.json()["ts"],
            "parse": "full",
            "text": f"{request.form.get('body-plain', '[unknown]')}",
        },
    )

    return "OK"
