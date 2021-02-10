from django.contrib import admin, auth

from .models import Thing, Useship


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost']


@admin.register(Useship)
class UseshipAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'thing_id', 'weight']
