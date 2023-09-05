from django.contrib import admin
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin
from mail_app.models import Client, MessageToMailing, MailingLogs, MailingSettings


# # Unregister the provided model admin
# admin.site.unregister(User)
#
# # Register out own model admin, based on the default UserAdmin
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         is_superuser = request.user.is_superuser
#         if not is_superuser:
#             form.base_fields['title'].disabled = True
#         return form

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Клиенты"""
    list_display = ('email', 'name', 'surname', 'patronymic', 'comment', 'owner')
    # list_display = ('__all__')
    list_filter = ('email',)
    search_fields = ('name', 'email', 'surname',)


@admin.register(MessageToMailing)
class MessageToMailingAdmin(admin.ModelAdmin):
    """Сообщение для рассылки"""
    list_display = ('letter_subject', 'letter_body', 'owner')
    list_filter = ('letter_subject',)
    search_fields = ('letter_subject',)


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    """Рассылка"""
    # list_display = ('__all__',)
    list_display = ('title', 'mailing_start_time', 'mailing_end_time', 'mailing_period',
                    'mailing_status', 'owner', 'mail', 'get_clients',)  # , 'clients'
    list_filter = ('mailing_start_time', 'mailing_end_time', 'mailing_period', 'clients',)
    search_fields = ('title', 'clients')
    ordering = ('-mailing_status',)

    moderator_readonly_fields = ('title', 'mailing_start_time', 'mailing_end_time', 'mailing_period', 'owner', 'mail','get_clients',)

    exclude = ('clients',)

    def get_readonly_fields(self, request, obj=None):
        """Данный метод отдает кортеж с элементами только для чтения"""
        is_superuser = request.user.is_superuser
        if not is_superuser:
            # exclude = ('clients',)
            return self.moderator_readonly_fields
        else:
            ###
            return super(MailingSettingsAdmin, self).get_readonly_fields(request, obj=obj)
            # pass

    # def get_form(self, request, obj=None, **kwargs):
    #     """Отключаем поля для не суперпользователей"""
    #     form = super().get_form(request, obj, **kwargs)
    #     is_superuser = request.user.is_superuser
    #     if not is_superuser:
    #         form.base_fields['title'].disabled = True
    #         form.base_fields['mailing_start_time'].disabled = True
    #     return form



@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    """Логи рассылки"""
    list_display = ('timestamp', 'attempt_status', 'server_response', 'client', 'mailing')
    list_filter = ('attempt_status', 'server_response', 'client',)
    search_fields = ('timestamp', 'client', 'mailing',)
    ordering = ('-timestamp',)  # сортировка по последнему времени попытки
