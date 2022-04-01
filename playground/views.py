from django.shortcuts import render, redirect
from django.http import HttpResponse
name = {'name': ''}

# Create your views here.
def say_hello(request):
    return render(request, 'hello.html', {'name': 'Johannes'})

def sut(request):
    print(request.GET.get('password'))
    if request.method == 'POST':
        name['name'] = request.POST.get('email')
        return redirect('home')
    return render(request, 'login_test.html')

def home_screen(request):
    return render(request, 'home_screen.html', name)

def redirect_to_home(request):
    return redirect('home')