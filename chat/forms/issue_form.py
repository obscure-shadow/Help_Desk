from django import forms
from chat.models.issue import Issue
from chat.models.student import Student
from django.contrib.auth.models import User

class IssueForm(forms.ModelForm):



    class Meta:
        model = Issue
        fields = ['issue_desc',]
