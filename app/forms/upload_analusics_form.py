from django import forms
from app.models import Analysis


class UploadAnalysisForm(forms.ModelForm):
    glucose_level = forms.FloatField(required=True, label='Уровень глюкозы (мг/дл)',
                                     widget=forms.NumberInput(attrs={'step': '0.01'}))

    class Meta:
        model = Analysis
        fields = ['pdf_file', 'glucose_level']