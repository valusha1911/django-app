from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.conf import settings

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    # created_at = models.DateTimeField()
    avatar = models.FileField(null=True, blank=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
