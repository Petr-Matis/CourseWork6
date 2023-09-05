from django.db import models

from users.models import User

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """Клиент сервиса:"""
    email = models.EmailField(max_length=254, verbose_name='email')
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество', **NULLABLE)
    comment = models.CharField(max_length=300, verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)
    def __int__(self):
        return f'{self.email} {self.name} {self.surname}'

    def __str__(self):
        return f'{self.email} {self.name} {self.surname}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ('email',)


class MailingSettings(models.Model):
    """Рассылка (настройки)"""
    FREQUENCY_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )
    STATUS_CHOICES = (
        ('completed', 'Завершена'),
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('off', 'Отключена')
    )

    title = models.CharField(max_length=50, verbose_name='Название')
    mailing_start_time = models.DateTimeField(**NULLABLE, verbose_name='Время начала рассылки')
    mailing_end_time = models.DateTimeField(**NULLABLE, verbose_name='Время конца рассылки')
    mailing_period = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, verbose_name='Периодичность рассылки')
    mailing_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created', verbose_name='Статус рассылки')
    mail = models.ForeignKey('MessageToMailing', on_delete=models.CASCADE, verbose_name='Сообщение рассылки',
                             related_name='log_of_message')
    clients = models.ManyToManyField('Client', verbose_name='Клиенты')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return (f"Название: '{self.title}' {self.get_mailing_period_display()} рассылка в {self.mailing_start_time}"
                f"{self.mail }/{self.clients} /{self.owner}")

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def get_clients(self):
        verbose_name = 'Клиенты'
        """Для админки, чтоб выводить в админку, иначе error:'must not be a ManyToManyField.'"""
        return ",".join([str(p) for p in self.clients.all()])


class MessageToMailing(models.Model):
    """Сообщение для рассылки"""
    letter_subject = models.CharField(max_length=500, verbose_name='тема письма')
    letter_body = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)
    def __int__(self):
        return f'{self.letter_subject} {self.letter_body} '

    def __str__(self):
        return f'{self.letter_subject} {self.letter_body}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'
        ordering = ('letter_subject',)


class MailingLogs(models.Model):
    """Логи рассылки"""
    MAILING_STATUS = (
        ('successful', 'Успешно отправлено'),
        ('failed', 'Ошибка отправки'),
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    attempt_status = models.CharField(max_length=50, choices=MAILING_STATUS, verbose_name='Статус попытки')
    server_response = models.TextField(blank=True, null=True, verbose_name='Ответ сервера')
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, verbose_name='Клиент', **NULLABLE)
    mailing = models.ForeignKey('MailingSettings', on_delete=models.SET_NULL, verbose_name='mailing', **NULLABLE)


    def __int__(self):
        return f'{self.timestamp} {self.attempt_status} '

    def __str__(self):
        return f'{self.timestamp} {self.attempt_status}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
        ordering = ('attempt_status',)

