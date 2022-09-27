from django import forms
from .models import Cinema, Screening


class CinemaListForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = ['name', 'city', 'movies']


# class CinemaDetailViewForm(forms.ModelForm):
#     class Meta:
#         model = Cinema
#         fields = ['name', 'city', 'movies']
