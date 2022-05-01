from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput


class Signup(ModelForm):
    def clean(self):
        super(Signup, self).clean()

    class Meta:
        model = User 
        fields = ('email', 'username', 'password')
        help_texts = {
            "username": None,
        }
        widgets = {
            'email': EmailInput(attrs={
                'class': "form-control", 
                'placeholder': 'Email'
            }),
            'username': TextInput(attrs={
                'class': "form-control", 
                'placeholder': 'Username'
            }),
            'password': PasswordInput(attrs={
                'class': "form-control", 
                'placeholder': '••••••••',
            })
        }


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
