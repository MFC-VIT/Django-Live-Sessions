from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
# Create your views here.

def index(request):
    insert_me = 'hello from views.py file!'
    return render(request, 'newapp/index.html',{'insert_me':insert_me})

def movie(request):
    movie_list = Movie.objects.all()
    return render(request, 'newapp/movie_list.html',{'movie_list':movie_list})
