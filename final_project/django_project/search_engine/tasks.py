from __future__ import absolute_import
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPException
from .actions import get_tasks_date
import datetime


@shared_task
def mail():
    today_date = datetime.date.today()
    yesterday_date = today_date - datetime.timedelta(days=1)
    tasks = get_tasks_date(today_date)
    str_tasks = '<h3>Requests today:</h3><ul>'
    if tasks:
        for task in tasks:
            str_tasks += '<li>'
            str_tasks += task.keywords
            str_tasks += '</li>'
        str_tasks += '<ul>'
        try:
            email = EmailMultiAlternatives(
                'Subject.',
                # str_tasks[:-2],
                str_tasks,
                to=['n.a.s.t.y.a28v@gmail.com']
            )
            email.attach_alternative(str_tasks, "text/html")
            if email.send():
                return 'Message send.'
            else:
                return 'Error send.'
        except SMTPException as ex:
            return 'Error! {}'.format(ex.__dict__)
