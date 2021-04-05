from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.index,name="home"),
    path('teacher_signup/',views.teacher_signup,name="teacher_signup"),
    path('student_signup/',views.student_signup,name="student_signup"),
    path('login/',views.user_login,name="login"),
    path('all_student_list/',views.all_student_list,name="all_student_list"),
    path('logout/',views.user_logout,name="logout"),
    path('add_student/<int:pk>/',views.add_student,name="add_student"),
    path('class_student_list/',views.class_students_list,name="class_students_list"),
    path('class_teacher_list',views.class_teacher_list,name="class_teacher_list"),
    path('upload_assignment',views.upload_assignment,name="upload_assignment"),
    path('assignment_list/<int:pk>/',views.assignment_list, name="assignment_list"),
    path('teacher_assignment_list/',views.teacher_assignment_list, name="teacher_assignment_list"),
    path('submit_assignment/<int:id>',views.submit_assignment, name="submit_assignment"),
    path('submit_list/<int:id>',views.submit_list, name="submit_list"),
]
