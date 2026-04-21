from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=50)
    first_name = forms.CharField(required=True, max_length=50)
    last_name = forms.CharField(required=True, max_length=50)
    address = forms.CharField(max_length=50, required=False)
    phone = forms.CharField(max_length=13, required=False)
    city = forms.CharField(max_length=30, required=False)
    country = forms.CharField(max_length=30, required=False)
    date_of_birth = forms.DateField(required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, max_length=50)
    first_name = forms.CharField(required=False, max_length=50)
    last_name = forms.CharField(required=False, max_length=50)

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'date_of_birth', 'avatar']