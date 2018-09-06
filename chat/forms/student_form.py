from django import forms
from chat.models.student import Student

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('cohort',)
