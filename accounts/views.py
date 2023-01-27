from django.shortcuts import render, redirect
from accounts.forms import Authentication, UserCreation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = Authentication(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
            else:    
                return redirect('app:index')
    else:
        form = Authentication()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('app:index')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect ('app:index')
    else:
        form = UserCreation()
    return render(request, 'accounts/signup.html', {'form': form})

