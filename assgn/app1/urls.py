from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index, name="home"),
    path('teacher_signup/',views.TeacherSignUp,name="teacher_signup"),
    path('student_signup/',views.StudentSignUp,name="student_signup"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('all_students_list/',views.all_students_list,name="all_students_list"),
    path('add_student/<int:pk>/',views.add_student,name="add_student"),
    path('class_students_list/',views.class_students_list,name="class_student_list"),
    path('all_teacher_list/',views.all_teacher_list,name="all_teacher_list"),
    path('upload_assignment/',views.upload_assignment,name="upload_assignment"),
    path('assignment_list/<int:pk>/',views.assignment_list,name="assignment_list"),
    path('teacher_assignment_list/',views.teacher_assignment_list,name="teacher_assignment_list"),
    path('submit_assignment/<int:pk>/',views.submit_assignment,name="submit_assignment"),
    path('submission_list/<int:pk>/',views.submission_list,name="submission_list"),
]
