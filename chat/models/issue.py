from django.db import models
from django.db.models import *


class Issue(models.Model):
    customer_id = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE
    )
    is_complete = models.BooleanField(default=False)
    is_escalated = models.BooleanField(default=False)
    issue_desc = models.CharField(max_length=200)

    def __str__(self):
        return f"Issue: {self.issue_desc}"
