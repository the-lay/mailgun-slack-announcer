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
    email_sender = request.form.get("from", request.form.get("sender", "[unknown]"))
    if " <" in email_sender:
        email_sender = email_sender.split(" <")[0]
    sender_hash = hashlib.sha1(email_sender.encode("utf-8")).hexdigest()
    avatar = "https://www.gravatar.com/avatar/%s?d=retro" % sender_hash

    # Announcement
    announcement = requests.post(
        url="https://slack.com/api/chat.postMessage",
        data={
            "token": SLACK_API_TOKEN,
            "channel": SLACK_CHANNEL,
            "icon_url": avatar,
            "parse": "full",
            "text": f"Subject: {email_subject}",
            "username": email_sender,
        },
    )

    # Actual email content
    content = requests.post(
        url="https://slack.com/api/chat.postMessage",
        data={
            "token": SLACK_API_TOKEN,
            "channel": SLACK_CHANNEL,
            "thread_ts": announcement.json()["ts"],
            "icon_url": avatar,
            "parse": "full",
            "text": f"{email_subject}",
            "username": email_sender,
        },
    )

    return "OK"
