from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from app.forms.user_register_form import UserRegisterForm

from app.forms.user_login_form import UserLoginForm


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу логиним после регистрации
            return redirect('app:index')
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('app:index')
    else:
        form = UserLoginForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('app:login')
