from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Student")
    name = models.CharField(max_length=250)
    roll_no = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['roll_no']

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Teacher")
    name = models.CharField(max_length=254)
    subject_name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()

    def __str__(self):
        return self.name

class StudentsInClass(models.Model):
    teacher = models.ForeignKey(Teacher,related_name="class_teacher",on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name="student_class", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('teacher','student')

    def __str__(self):
        return self.student.name + ' in ' + self.teacher.name

class ClassAssignment(models.Model):
    teacher = models.ForeignKey(Teacher,related_name="teacher_assignment",on_delete=models.CASCADE)
    student = models.ManyToManyField(Student,related_name="student_assignment")
    created_at = models.DateTimeField(auto_now=True)
    assignment_name = models.CharField(max_length=250)
    assignment = models.FileField(upload_to='assignments')

    def __str__(self):
        return self.assignment_name

    class Meta:
        ordering = ['-created_at']

class SubmitAssignment(models.Model):
    student = models.ForeignKey(Student,related_name="student_submission",on_delete=models.CASCADE)
    assignment = models.ForeignKey(ClassAssignment,related_name="assignment_submission",on_delete=models.CASCADE)
    submission = models.FileField(upload_to='submission')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name + ' submitted ' + self.assignment.assignment_name

    class Meta:
        unique_together = ('student','assignment')
        ordering = ['-created_at']
