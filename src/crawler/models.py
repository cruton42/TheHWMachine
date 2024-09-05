from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    url = models.URLField()
    header = models.CharField(max_length=255)
    description = models.TextField()  # Use TextField for longer text like job descriptions

    def __str__(self):
        return self.header
    
class twJob(models.Model):
    url = models.URLField()
    header = models.CharField(max_length=255)
    description = models.TextField()  # Use TextField for longer text like job descriptions

    def __str__(self):
        return self.header

class UserPDF(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='user_pdfs/', null=True, blank=True)

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='resumes/')
    text_content = models.TextField(blank=True, null=True)  # Store extracted text from the PDF