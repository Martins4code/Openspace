from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Space,User


class My_usercreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']
        
        

class Spaceform(ModelForm):
    class Meta:
        model = Space # this is the model or database the form is using
        fields = '__all__'
        exclude = ["host","participants"]
        
class Userform(ModelForm):
    class Meta: # now specify your fields
        model = User
        fields = ['avatar','name','username', 'email','bio']