import os
import logging

import requests

from django.conf import settings
from django.apps import apps
from django.template import Template, Context
from django.template.loader import render_to_string
from celery import shared_task


logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")


def inject_to_content(content, context):
    template = Template(content)
    ctx = Context(context)

    return template.render(ctx)


@shared_task(name="send_mail")
def send_mail(emails, payload, model, model_id):
    logging.info(
        "[send] | Request | Payload: (subject: {}, body: {}, mail_to: {})".format(
            payload.get("subject", ""), payload.get("body", ""), str(emails)
        )
    )

    if payload and settings.DEBUG:
        data_payload = {
            "from": settings.MAILGUN_FROM,
            "to": emails,
            "subject": payload.get("subject", ""),
            "text": payload.get("body", ""),
        }

        response = requests.post(
            settings.MAILGUN_API_ENDPOINT,
            auth=("api", settings.MAILGUN_API_KEY),
            data=data_payload,
        )

        if response.status_code == 200:
            Model = apps.get_model("manager.{}".format(model))
            obj = Model.objects.get(pk=model_id)
            obj.is_sent = True
            obj.save()

        logging.info(
            "[send] | Response (HTTP Code {}) | Payload: {}".format(
                response.status_code, response.text
            )
        )

        return {"status_code": response.status_code}
    return {"status_code": 200}
