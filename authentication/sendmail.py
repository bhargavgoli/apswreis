from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def sendAppMail(to, name, refNo):

    text_content = 'Hey {}, You are eligible to transfer, your reference number is {}. Please login and save/modify your preferences'.format(
        name, refNo)
    send_mail('Hey '+name+', APSWREIS Reference No:'+refNo, text_content, 'info@bhargavgoli.com',
              [to], html_message=text_content, fail_silently=False)
    return True
