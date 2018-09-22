from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import PayWaysUser


class UserAdmin(_UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = PayWaysUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'telegram_id', 'vk_id']


admin.site.register(PayWaysUser, UserAdmin)
