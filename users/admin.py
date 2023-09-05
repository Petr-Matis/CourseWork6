from django.contrib import admin

from users.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Клиенты"""
    # admin.site.register(User)
    list_display = ('email', 'phone', 'avatar', 'country', 'is_verified')
    search_fields = ('email',)

    moderator_readonly_fields = ('first_name', 'last_name', 'email', 'phone', 'avatar', 'country', 'is_verified',)
    # all_fields_my = ( 'phone', 'avatar', 'country', 'is_verified')
    # readonly_fields = all_fields_my

    f = ('is_staff', 'is_active', 'date_joined')


    def get_readonly_fields(self, request, obj=None):
        """Данный метод отдает кортеж с элементами только для чтения"""
        is_superuser = request.user.is_superuser
        if not is_superuser:
            # exclude = ('clients',)
            return self.moderator_readonly_fields
        else:
            ###
            return super(UserAdmin, self).get_readonly_fields(request, obj=obj)
            # pass

    def get_exclude(self, request, obj=None):
        """
        Hook for specifying exclude.
        Если модератор, то убираем ненужные поля
        """
        if request.user.groups.filter(name='moderator').exists():
            print('moderator')
            is_superuser = request.user.is_superuser
            if not is_superuser:
                print('notsuper')
                self.exclude = ('password', 'last_login', 'groups', 'date_joined', 'user_permissions', 'is_superuser', 'is_staff')

        # else:
        #     print('dddddddddddddddddddd')
        return self.exclude

    # def get_readonly_fields(self, request, obj=None):
    #     """Данный метод отдает кортеж с элементами только для чтения"""
    #     if request.user.groups.filter(name='moderator').exists():
    #         return self.moderator_readonly_fields
    #
    #     else:
    #         return super(UserAdmin, self).get_readonly_fields(request, obj=obj)
