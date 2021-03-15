from django import forms
from .models import MovieReviews

class ReviewForm(forms.ModelForm):
    class Meta():
        model = MovieReviews
        fields = ['review']
