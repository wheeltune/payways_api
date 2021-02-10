from django.db import models
from django.contrib.auth.models import AbstractUser


class PayWaysUser(AbstractUser):
    telegram_id = models.IntegerField(blank=True, null=True)
    vk_id = models.IntegerField(blank=True, null=True)

    contacts = models.ManyToManyField(
        'self', through='Friendship', through_fields=('from_user', 'to_user'),
        symmetrical=False
    )

    def __str__(self):
        return self.username


class Friendship(models.Model):
    from_user = models.ForeignKey(PayWaysUser, on_delete=models.CASCADE,
                                  related_name='from_user')
    to_user = models.ForeignKey(PayWaysUser, on_delete=models.CASCADE)
