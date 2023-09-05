import logging
from datetime import timedelta
from django.db import models
import schedule
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from mail_app.forms import MailingSettingsForm, MailingSettingsUpdateFormModerator
from mail_app.models import *


def sending_mail(subject, body, clients_email):
    """Отправление письма"""
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        clients_email
    )


def send_mailing():
    """Рассылка. запуск отправки писем в зависимости от текущего времени"""
    mailing_settings = MailingSettings.objects.all()
    current_time = timezone.now()
    frequency = {'daily': 1, 'weekly': 7, 'monthly': 30}
    for mailing in mailing_settings:
        # Начало рассылки
        if mailing.mailing_status == 'created':  # or mailing.mailing_status == 'started'

            print('created')
            if mailing.mailing_start_time <= current_time <= mailing.mailing_end_time:
                print('time to send mail')
                for client in mailing.clients.all():
                    letter_subject = mailing.mail.letter_subject
                    letter_body = mailing.mail.letter_body
                    try:
                        # print(letter_subject, letter_body, settings.EMAIL_HOST_USER)
                        send_mail(letter_subject, letter_body, settings.EMAIL_HOST_USER, [client.email])
                        # Создание лога рассылки при успехе
                        MailingLogs.objects.create(
                            mailing=mailing,
                            client=client,
                            attempt_status='successful',
                            server_response='Сообщение успешно отправлено',
                        )
                        mailing.mailing_status = 'started'
                        # mailing.mailing_start_time += timedelta(days=frequency.get(mailing.mailing_period))
                        mailing.save()
                        print('sendmale')

                    except Exception as error:
                        # Создание лога рассылки при ошибке
                        MailingLogs.objects.create(
                            mailing=mailing,
                            client=client,
                            attempt_status='failed',
                            server_response=str(error),
                        )
                        print('failed sendmale')
            # Конец рассылки
            elif mailing.mailing_end_time <= current_time:
                mailing.mailing_status = 'completed status'
                mailing.save()
                print('completed status')
            else:
                pass

        elif mailing.mailing_status == 'started':
            print('started')
            if mailing.mailing_end_time <= current_time:
                mailing.mailing_status = 'completed'
                mailing.save()
                print('completed')
            else:
                pass


def job():
    schedule.every(5).seconds.do(send_mailing)
    logging.info('done')


def print_object():
    # print(MailingSettings.objects.all())
    r = MailingSettings.objects.filter(mail_id=11)
    # print(f'\n{MailingSettings.objects.filter(mail_id=11)}\n')
    print(f'\n{MailingLogs.objects.filter(mailing_id=r)}\n')
    # print(r.objects.title)


def get_filter_user_group(del_group, user):
    """Тут в зависимости от группы юзера выводятся разные формы продукта"""
    if user.groups.filter(name=del_group).exists():
        form_class = MailingSettingsUpdateFormModerator
    else:
        form_class = MailingSettingsForm
    return form_class