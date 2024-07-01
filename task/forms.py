from django import forms
from .models import Tasks
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'category']



class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'category', 'is_completed']
