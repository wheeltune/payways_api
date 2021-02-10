from django.contrib import admin, auth

from .models import Room, Membership


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'room_id']
