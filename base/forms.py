from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'password1', 'password2', 'email', 'avatar', 'bio']


class RoomForm(ModelForm):
    class Meta: 
        model = Room
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta: 
        model = User
        fields = ['name', 'username', 'password', 'email', 'avatar']
        
