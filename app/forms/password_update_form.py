from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class PasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput, required=False)
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, required=False)

    def clean_old_password(self):
        # Если новый пароль пустой, старый пароль не требуется
        if not self.cleaned_data.get('new_password1'):
            return None
        return self.cleaned_data.get('old_password')

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if password:
            if len(password) < 8:
                raise forms.ValidationError('Пароль должен содержать хотя бы 8 символов.')
        return password

    def clean_new_password2(self):
        password2 = self.cleaned_data.get('new_password2')
        if password2 and password2 != self.cleaned_data.get('new_password1'):
            raise forms.ValidationError('Пароли не совпадают.')
        return password2

