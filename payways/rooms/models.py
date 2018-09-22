from django.db import models


from ..users.models import PayWaysUser


class Room(models.Model):
    name = models.TextField()
    members = models.ManyToManyField(PayWaysUser, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(PayWaysUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    is_admin = models.BooleanField(default=False)
