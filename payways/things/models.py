from django.db import models

from ..users.models import PayWaysUser
from ..rooms.models import Room, Membership


class Thing(models.Model):
    name = models.TextField()
    cost = models.FloatField()

    from_room = models.ForeignKey(Room, on_delete=models.CASCADE)

    added_by = models.ForeignKey(PayWaysUser, on_delete=models.CASCADE, related_name='added_by')
    buyer = models.ForeignKey(PayWaysUser, on_delete=models.CASCADE, related_name='buyer')
    used_by = models.ManyToManyField(PayWaysUser, through='Useship')


class Useship(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.PROTECT)
    user = models.ForeignKey(PayWaysUser, on_delete=models.PROTECT)
