import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from app.forms.password_update_form import PasswordUpdateForm
from app.forms.user_profile_form import UserProfileForm

logger = logging.getLogger(__name__)


@login_required
def profile_view(request):
    if request.method == 'POST':
        # Определяем, какая форма была отправлена
        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('app:profile')
            # Если форма невалидна, продолжаем с ошибками
            password_form = PasswordUpdateForm(request.user)

        elif 'change_password' in request.POST:
            password_form = PasswordUpdateForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('app:profile')
            # Если форма невалидна, продолжаем с ошибками
            profile_form = UserProfileForm(instance=request.user)

    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = PasswordUpdateForm(request.user)

    return render(request, 'app/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })
