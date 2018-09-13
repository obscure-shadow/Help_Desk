from django.db import models
from django.db.models import *
from django.contrib.auth.models import User

class Issue(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    is_complete = models.BooleanField(default=False)
    is_escalated = models.BooleanField(default=False)
    issue_desc = models.CharField(max_length=200)

    def __str__(self):
        return f"Student: {self.user.username} Issue: {self.issue_desc} Status: {self.is_escalated} Complete: {self.is_complete}"
