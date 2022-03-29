import os
import requests
from datetime import datetime

from flask import Flask, request

SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL", "#general")

app = Flask(__name__)


@app.route("/mail-webhook", methods=["POST"])
def mail_webhook():

    sender = request.form.get("from", request.form.get("sender", "[unknown]"))
    recipients = ", ".join(request.form.get("recipient", "[unknown]").split(","))
    timestamp = int(request.form.get("timestamp", 0))
    parsed_timestamp = datetime.fromtimestamp(timestamp)
    subject = request.form.get("subject", "[unknown]")
    plain_text = request.form.get("body-plain", "[unknown]")
    n_attachments = int(request.form.get("attachment-count", 0))

    announcement = requests.post(
        url="https://slack.com/api/chat.postMessage",
        data={
            "token": SLACK_API_TOKEN,
            "channel": SLACK_CHANNEL,
            "parse": "full",
            "text": f"Sender: {sender}\n"
            f"Recipients: {recipients}\n"
            f"Time: {parsed_timestamp:%Y-%m-%d %H:%M:%S} UTC\n"
            f"# attachments: {n_attachments}\n"
            f"Subject: {subject}",
        },
    )

    content = requests.post(
        url="https://slack.com/api/chat.postMessage",
        data={
            "token": SLACK_API_TOKEN,
            "channel": SLACK_CHANNEL,
            "thread_ts": announcement.json()["ts"],
            "parse": "full",
            "text": f"{plain_text}",
        },
    )

    for i in range(n_attachments):
        attachment = request.form.get(f"attachment-{i}", "[unknown]")

        requests.post(
            url="https://slack.com/api/files.upload",
            data={
                "token": SLACK_API_TOKEN,
                "channel": SLACK_CHANNEL,
                "thread_ts": announcement.json()["ts"],
                "parse": "full",
                "file": attachment,
            },
        )

    return "OK"
