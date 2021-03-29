from django.shortcuts import render,get_object_or_404,redirect
from .models import User, Student, Teacher, StudentsInClass, ClassAssignment, SubmitAssignment
from .forms import UserForm, TeacherProfileForm, StudentProfileForm, ClassAssignmentForm, SubmitAssignmentForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

def index(request):
    return render(request,'app1/index.html',{})

def TeacherSignUp(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        teacher_profile_form = TeacherProfileForm(data = request.POST)

        if user_form.is_valid() and teacher_profile_form.is_valid():

            user = user_form.save()
            user.is_teacher = True
            user.save()

            teacher = teacher_profile_form.save(commit=False)
            teacher.user = user
            teacher.save()

            registered = True

        else:
            print(user_form.errors, teacher_profile_form.errors)
    else:
        user_form = UserForm()
        teacher_profile_form = TeacherProfileForm()

    return render(request,'app1/teacher_signup.html',{'user_form':user_form,'teacher_profile_form':teacher_profile_form, 'registered':registered})

def StudentSignUp(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        student_profile_form = StudentProfileForm(data = request.POST)

        if user_form.is_valid() and student_profile_form.is_valid():

            user = user_form.save()
            user.is_student = True
            user.save()

            student = student_profile_form.save(commit=False)
            student.user = user
            student.save()

            registered = True

        else:
            print(user_form.errors, student_profile_form.errors)
    else:
        user_form = UserForm()
        student_profile_form = StudentProfileForm()

    return render(request,'app1/student_signup.html',{'user_form':user_form,'student_profile_form':student_profile_form, 'registered':registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse("Account not active")

        else:
            print("Invalid details")
            return redirect('login')

    else:
        return render(request,'app1/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def all_students_list(request):
    students = Student.objects.all()
    class_student = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    class_student_obj = []
    for i in class_student:
        class_student_obj.append(get_object_or_404(Student,pk=i.student.pk))
    final_student_list = []
    for i in students:
        if i not in class_student_obj:
            final_student_list.append(i)
    print(students)
    print(class_student_obj)
    print(final_student_list)
    return render(request,'app1/student_list.html',{'students':final_student_list})

def add_student(request,pk):
    teacher = request.user.Teacher
    student = get_object_or_404(Student,pk=pk)

    student_add = StudentsInClass(teacher=teacher,student=student)
    student_add.save()

    return HttpResponseRedirect(reverse('all_students_list'))

@login_required
def class_students_list(request):
    teacher = request.user.Teacher
    class_student = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    return render(request,'app1/class_student_list.html',{'class_student':class_student})

@login_required
def all_teacher_list(request):
    student = request.user.Student
    teacher = StudentsInClass.objects.filter(student=request.user.Student)
    all_teacher_list = [x.teacher for x in teacher]
    # print(all_teachers_list)
    return render(request,'app1/all_teacher_list.html',{'all_teacher_list':all_teacher_list})

def upload_assignment(request):
    uploaded = False
    if request.method == "POST":
        students = StudentsInClass.objects.filter(teacher=request.user.Teacher)
        student_list = [x.student for x in students]
        form = ClassAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = request.user.Teacher
            upload.save()
            upload.student.add(*student_list)
            uploaded = True
        else:
            print(form.errors)
    else:
        form = ClassAssignmentForm()
    return render(request,'app1/upload_assignment.html',{'form':form,'uploaded':uploaded})

def assignment_list(request,pk):
    teacher = get_object_or_404(Teacher,pk=pk)
    assignment_list = ClassAssignment.objects.filter(teacher=teacher)
    return render(request,'app1/class_assignment_list.html',{'assignment_list':assignment_list})

def teacher_assignment_list(request):
    teacher = request.user.Teacher
    assignment_list = ClassAssignment.objects.filter(teacher=teacher)
    return render(request,'app1/teacher_assignment_list.html',{'assignment_list':assignment_list})

def submit_assignment(request,pk):
    uploaded = False
    assignment = get_object_or_404(ClassAssignment,pk=pk)
    if request.method == "POST":
        form = SubmitAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.assignment = assignment
            upload.student = request.user.Student
            upload.save()
            uploaded = True
    else:
        form = SubmitAssignmentForm()
    return render(request,'app1/submit_assignment.html',{'form':form,'uploaded':uploaded})

def submission_list(request,pk):
    assignment = get_object_or_404(ClassAssignment,pk=pk)
    submissions = SubmitAssignment.objects.filter(assignment=assignment)
    return render(request,'app1/submission_list.html',{'submissions':submissions})
