from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Teacher, StudentsInClass, ClassAssignment, SubmitAssignment

class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username','password1','password2']

class TeacherProfileForm(forms.ModelForm):
    class Meta():
        model = Teacher
        fields = ['name','subject_name','email','phone']

class StudentProfileForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ['name','roll_no','email','phone']

class ClassAssignmentForm(forms.ModelForm):
    class Meta():
        model = ClassAssignment
        fields = ['assignment_name','assignment']

class SubmitAssignmentForm(forms.ModelForm):
    class Meta():
        model = SubmitAssignment
        fields = ['submission']
