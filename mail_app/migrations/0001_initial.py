# Generated by Django 4.2.3 on 2023-08-25 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('surname', models.CharField(max_length=100, verbose_name='surname')),
                ('patronymic', models.CharField(blank=True, max_length=100, null=True, verbose_name='patronymic')),
                ('comment', models.CharField(blank=True, max_length=300, null=True, verbose_name='comment')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ('email',),
            },
        ),
        migrations.CreateModel(
            name='MailingLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_of_last_attempt', models.DateTimeField(verbose_name='datetime_of_last_attempt')),
                ('attempt_status', models.BooleanField(verbose_name='attempt_status')),
                ('mail_server_response', models.CharField(max_length=600, verbose_name='mail_server_response')),
            ],
            options={
                'verbose_name': 'MailingLogs',
                'ordering': ('attempt_status',),
            },
        ),
        migrations.CreateModel(
            name='MessageToMailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter_subject', models.CharField(max_length=500, verbose_name='letter_subject')),
                ('letter_body', models.TextField(verbose_name='letter_body')),
            ],
            options={
                'verbose_name': 'MessageToMailing',
                'ordering': ('letter_subject',),
            },
        ),
    ]