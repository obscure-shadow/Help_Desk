from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=20)
    cohort = models.CharField(max_length=20)
    is_instructor = models.BooleanField(default=False)
    is_senior = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'
