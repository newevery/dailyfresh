from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import time
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')

app=Celery('celery_tasks.tasks',broker='redis://192.168.12.75:6379/8')
@app.task
def send_register_active_email(to_email,username,token):
    subject = '哒哒哒哒哒哒多多多多多多多多多'
    message = '欢迎您成为天天生鲜注册用户</h1>请点击下面链接注册'
    sender = settings.EMAIL_PROM
    reciver = [to_email]
    html_message = '<h1>%s,欢迎您成为天天生鲜注册用户</h1>请点击下面链接注册<br/>' \
                             '<a href="http://127.0.0.1:8000/user/active/%s">' \
                             'http://127.0.0.1:8000/user/active/%s</a>' \
                             '' % (username, token, token)
    send_mail(subject,message, sender, reciver, html_message=html_message)
    time.sleep(5)