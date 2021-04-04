from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User,related_name="Student",on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    roll_no = models.CharField(max_length=254)
    phone_no = models.IntegerField()
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User,related_name="Teacher",on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    subject_name = models.CharField(max_length=254)
    phone_no = models.IntegerField()
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

class StudentsInClass(models.Model):
    teacher = models.ForeignKey(Teacher,related_name="teacher_class",on_delete=models.CASCADE)
    student = models.ForeignKey(Student,related_name="student_class",on_delete=models.CASCADE)

    def __str__(self):
        return self.student.name + ' in ' + self.teacher.name

    class Meta:
        unique_together = ('student','teacher')

class ClassAssignment(models.Model):
    teacher = models.ForeignKey(Teacher,related_name="teacher_assignment",on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,related_name="student_assignment")
    created_at = models.DateTimeField(auto_now=True)
    assignment_name = models.CharField(max_length=254)
    assignment = models.FileField(upload_to='assignment')

    def __str__(self):
        return self.assignment_name
