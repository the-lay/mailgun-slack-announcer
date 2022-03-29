import os
import requests
from datetime import datetime

from flask import Flask, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL", "#general")

app = Flask(__name__)
api = WebClient(token=SLACK_API_TOKEN)


@app.route("/mail-webhook", methods=["POST"])
def mail_webhook():

    sender = request.form.get("from", request.form.get("sender", "[unknown]"))
    recipients = ", ".join(request.form.get("recipient", "[unknown]").split(","))
    timestamp = int(request.form.get("timestamp", 0))
    parsed_timestamp = datetime.fromtimestamp(timestamp)
    subject = request.form.get("subject", "[unknown]")
    plain_text = request.form.get("body-plain", "[unknown]")

    try:
        announcement = api.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=f"📧📧📧\n"
            f"*Sender:* {sender}\n"
            f"*Recipients:* {recipients}\n"
            f"*Time:* {parsed_timestamp:%Y-%m-%d %H:%M:%S} UTC\n"
            f"*Subject:* {subject}",
            parse="full",
        )
        thread_ts = announcement.get("ts")

        api.chat_postMessage(
            channel=SLACK_CHANNEL, thread_ts=thread_ts, text=plain_text
        )

        for attachment in request.files.values():
            api.files_upload(
                channels=SLACK_CHANNEL,
                thread_ts=thread_ts,
                filename=attachment.filename,
                file=attachment.stream.read(),
            )

    except SlackApiError as e:
        api.chat_postMessage(channel=SLACK_CHANNEL, text=e.response["error"])

    return "OK"
