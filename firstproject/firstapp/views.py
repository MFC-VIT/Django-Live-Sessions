from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import MovieDetails,MovieReviews
from .forms import ReviewForm
from django.contrib import messages

# Create your views here.

########################################### View for Home Page ###########################################
def HomePage(request):
    movies = MovieDetails.objects.all()
    return render(request,'firstapp/homepage.html',{'movies':movies})

########################################### User Login Logout and Register ##############################

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if(User.objects.filter(username=username).exists()):
            messages.warning(request, "Username Already exists")
            return redirect('firstapp:signup')
        else:
            user = User.objects.create_user(username = username,
                                            first_name = first_name,
                                            last_name = last_name,
                                            password = password,
                                            email = email)
            user.save()
            return HttpResponseRedirect(reverse('firstapp:home'))
    return render(request,'firstapp/signup.html',{})

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('firstapp:home'))
            else:
                return HttpResponse("Account not active")
        else:
            messages.warning(request, "Invalid Username or Password")
            return redirect("firstapp:login")
    return render(request,'firstapp/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('firstapp:home'))

#############################################################################################################
                                    #    Views for Movie Reviews    #
#############################################################################################################

def movie_description(request,pk):
    movie = MovieDetails.objects.get(pk=pk)
    movie_reviews = MovieReviews.objects.filter(movie=movie)
    form = ReviewForm()
    return render(request,'firstapp/movie_description.html',{'movie':movie,'movie_reviews':movie_reviews,'form':form})

@login_required
def add_review(request,pk):
    movie = MovieDetails.objects.get(pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            reviews = form.save(commit=False)
            reviews.user = request.user
            reviews.movie = movie
            try:
                reviews.save()
                messages.success(request, "Review added successfully")
            except:
                messages.warning(request, "You have already submited your review")
            return HttpResponseRedirect(reverse('firstapp:movie_description',kwargs={'pk':pk}))
        return HttpResponseRedirect(reverse('firstapp:movie_description',kwargs={'pk':pk}))
