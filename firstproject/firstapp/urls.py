from django.urls import path
from . import views

app_name = 'firstapp'

urlpatterns = [
    path('', views.HomePage, name="home"),
    path('movie_description/<int:pk>/',views.movie_description, name="movie_description"),
    path('add_review/<int:pk>/',views.add_review, name="add_review"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.signin, name="login"),
    path('logout/', views.user_logout, name="logout"),
]
