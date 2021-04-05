from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request,'app1/index.html',{})

def teacher_signup(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        teacher_form = TeacherForm(data = request.POST)

        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save()
            user.is_teacher = True
            user.save()

            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()

            registered = True

        else:
            print(user_form.errors, teacher_form.errors)
    else:
        user_form = UserForm()
        teacher_form = TeacherForm()

    return render(request,'app1/teacher_signup.html',{'registered':registered,'user_form':user_form,'teacher_form':teacher_form})

def student_signup(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        student_form = StudentForm(data = request.POST)

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.is_student = True
            user.save()

            student = student_form.save(commit=False)
            student.user = user
            student.save()

            registered = True

        else:
            print(user_form.errors, student_form.errors)
    else:
        user_form = UserForm()
        student_form = StudentForm()

    return render(request,'app1/student_signup.html',{'registered':registered,'user_form':user_form,'student_form':student_form})

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
def all_student_list(request):
    student_list = Student.objects.all()
    class_student = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    student_in_class = [x.student for x in class_student]
    student_not_in_class = []
    for x in student_list:
        if x not in student_in_class:
            student_not_in_class.append(x)

    return render(request,'app1/all_student_list.html',{'student_list':student_not_in_class})

@login_required
def add_student(request,pk):
    student = get_object_or_404(Student,pk=pk)
    teacher = request.user.Teacher
    student_in_class = StudentsInClass(teacher=teacher,student=student)
    student_in_class.save()
    return HttpResponseRedirect(reverse('all_student_list'))

@login_required
def class_students_list(request):
    teacher = request.user.Teacher
    class_student = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    student_list = [x.student for x in class_student]
    return render(request,'app1/class_student_list.html',{'student_list':student_list})

@login_required
def class_teacher_list(request):
    student = request.user.Student
    class_teachers = StudentsInClass.objects.filter(student=student)
    teacher_list = [x.teacher for x in class_teachers]
    return render(request,'app1/class_teacher_list.html',{'teacher_list':teacher_list})

@login_required
def upload_assignment(request):
    teacher = request.user.Teacher
    student_object = StudentsInClass.objects.filter(teacher=teacher)
    student_list = [x.student for x in student_object]

    if request.method == "POST":
        form = ClassAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            upload.save()
            upload.students.add(*student_list)
        else:
            print(form.errors)
        return HttpResponseRedirect(reverse('teacher_assignment_list'))

@login_required
def assignment_list(request,pk):
    teacher = get_object_or_404(Teacher,pk=pk)
    assignment_list = ClassAssignment.objects.filter(teacher=teacher)
    return render(request,'app1/class_assignment_list.html',{'assignment_list':assignment_list})

@login_required
def teacher_assignment_list(request):
    teacher = request.user.Teacher
    assignment_list = ClassAssignment.objects.filter(teacher=teacher)
    form = ClassAssignmentForm()
    return render(request,'app1/teacher_assignment_list.html',{'assignment_list':assignment_list,'form':form})

@login_required
def submit_assignment(request, id=None):
    student = request.user.Student
    assignment = get_object_or_404(ClassAssignment, id=id)
    teacher = assignment.teacher
    try:
        get_submission = SubmitAssignment.objects.get(student=student,submitted_assignment=assignment)
        already_submitted = True
    except:
        already_submitted = False

    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            upload.student = student
            upload.submitted_assignment = assignment
            upload.save()
            return HttpResponseRedirect(reverse('assignment_list',kwargs={'pk':teacher.pk}))
    else:
        form = SubmitForm()
    return render(request,'app1/submit_assignment.html',{'form':form,'already_submitted':already_submitted})

@login_required
def submit_list(request,id):
    teacher = request.user.Teacher
    assignment = get_object_or_404(ClassAssignment, id=id)
    submissions = SubmitAssignment.objects.filter(teacher=teacher,submitted_assignment=assignment)
    return render(request,'app1/submit_list.html',{'submissions':submissions})
