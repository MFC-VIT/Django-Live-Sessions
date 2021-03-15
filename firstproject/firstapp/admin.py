from django.contrib import admin
from .models import MovieDetails,MovieReviews
# Register your models here.

admin.site.register(MovieDetails)
admin.site.register(MovieReviews)

# @admin.register(MovieDetails)
# class MovieDetailsAdmin(admin.ModelAdmin):
#     list_display = ['name','dor']
