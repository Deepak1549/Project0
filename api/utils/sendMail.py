from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from job_project import settings

def send_mail(message, email):
    message = "You have been selected for the next process of hiring" if message == 1 else "We are unable to proceed with your application"
    context = {"message": message, "subject":"Application status"}
    temp = render_to_string("mail/application_mail.html", context=context)
    msg = EmailMultiAlternatives("Don't Reply", temp, settings.DEFAULT_FROM_EMAIL, [email])
    msg.content_subtype = "html"
    msg.send()
    print("------------ sent --------------")