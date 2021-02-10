from django import forms
from django.contrib.auth import forms

from .models import PayWaysUser


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = PayWaysUser
        fields = ('username', 'email', 'first_name', 'last_name')


class UserChangeForm(forms.UserChangeForm):
    class Meta:
        model = PayWaysUser
        fields = ('username', 'email', 'first_name', 'last_name')
