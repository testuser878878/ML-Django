# app/models/analysis.py

from django.db import models
from app.models.user import User

class Analysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='analyses/')
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

