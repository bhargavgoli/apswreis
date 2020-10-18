from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def sendAppMail(to, name, refNo):

    text_content = 'Hey {}, We have received your request and your reference number is {}'.format(
        name, refNo)
    send_mail('Hey '+name+', APSWREIS Reference No:'+refNo, text_content, 'no-reply@bhargavgoli.com',
              [to], html_message=text_content, fail_silently=False)
    return True
