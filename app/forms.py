from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from app.models import User, News, Analysis


class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, label='Роль')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ['username', 'email', 'role']

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


class UploadAnalysisForm(forms.ModelForm):
    glucose_level = forms.FloatField(required=True, label='Уровень глюкозы (мг/дл)',
                                     widget=forms.NumberInput(attrs={'step': '0.01'}))

    class Meta:
        model = Analysis
        fields = ['pdf_file', 'glucose_level']
