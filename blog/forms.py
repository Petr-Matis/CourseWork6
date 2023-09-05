from django import forms
from django.forms import DateInput

from blog.models import Blog
from datetime import datetime
from django.forms import DateTimeInput, DateInput
from django.views.generic.edit import FormMixin



class BlogForm(forms.ModelForm):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_create'].widget = DateInput(attrs={'type': 'datetime-local'})

    class Meta:
        model = Blog
        fields = ('header', 'content', 'image','date_of_create',)
        # fields = '__all__'

        # widgets = {
        #     'date_of_create': forms.DateInput(
        #         attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
        #     )
        # }



        # self.fields['mailing_end_time'].widget = DateInput(attrs={'type': 'datetime-local'})
# class MailingSettingsFormNotUser(forms.ModelForm):
#
#     def __init__(self, *args, user=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['mailing_start_time'].widget = DateInput(attrs={'type': 'datetime-local'})
#         self.fields['mailing_end_time'].widget = DateInput(attrs={'type': 'datetime-local'})
#         self.user = user
#         self.fields['clients'].queryset = Client.objects.filter(owner=self.user)
#         self.fields['mail'].queryset = MessageToMailing.objects.filter(owner=self.user)