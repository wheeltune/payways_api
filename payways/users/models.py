from django.db import models
from django.contrib.auth.models import AbstractUser


class PayWaysUser(AbstractUser):
    telegram_id = models.IntegerField(blank=True, null=True)
    vk_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username


