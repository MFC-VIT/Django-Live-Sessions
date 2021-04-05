from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username','password1','password2']

class StudentForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ['name','roll_no','phone_no','email']

class TeacherForm(forms.ModelForm):
    class Meta():
        model = Teacher
        fields = ['name','subject_name','phone_no','email']

class ClassAssignmentForm(forms.ModelForm):
    class Meta():
        model = ClassAssignment
        fields = ['assignment_name','assignment']

class SubmitForm(forms.ModelForm):
    class Meta():
        model = SubmitAssignment
        fields = ['submit']
