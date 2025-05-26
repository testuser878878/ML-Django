from django import forms
from app.models import User


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ['username', 'email', 'role']
