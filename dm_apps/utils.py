import requests
from decouple import config, UndefinedValueError
from django.conf import settings
from python_http_client import BadRequestsError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Personalization
from django.core.mail import send_mail as django_send_mail


def is_connection_available(prefix):
    try:
        return config(prefix + '_DB_HOST') and \
               config(prefix + '_DB_PORT') and \
               config(prefix + '_DB_NAME') and \
               config(prefix + '_DB_USER') and \
               config(prefix + '_DB_PASSWORD')
    except UndefinedValueError:
        return False


def custom_send_mail(subject, html_message, from_email, recipient_list):
    """
    The role of this function is to handle the sending of an email message based on the configuration of the project setting.py file.
    - If settings.USE_SENDGRID = True, the mail will be sent with the python sendgrid package using the sendgrid REST api
    - If settings.USE_SMTP_EMAIL = True, the email will be send with django's send_mail function.
    - If settings.USE_SMTP_EMAIL and settings.USE_SENDGRID are both false, no email will be sent.

    :param subject:
    :param html_message:
    :param from_email:
    :param recipient_list:
    :return:
    """

    if settings.USE_SENDGRID:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        from_email = Email(from_email)
        to_list = Personalization()
        for email in set(recipient_list):
            to_list.add_to(Email(email))
        mail = Mail(
            from_email=from_email,
            to_emails=None,
            subject=subject,
            html_content=html_message
        )
        mail.add_personalization(to_list)
        try:
            sg.send(mail)
        except BadRequestsError:
            print("bad request. email not sent")

    elif settings.USE_SMTP_EMAIL:
        django_send_mail(
            message='',
            subject=subject,
            html_message=html_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )

    else:
        print('No email configuration present in application...')
        print("FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(from_email, recipient_list, subject, html_message))