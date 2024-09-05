# forms.py
from django import forms
from .models import UserPDF
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UploadPDFForm(forms.ModelForm):
    class Meta:
        model = UserPDF
        fields = ['pdf_file']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CoverLetterRequestForm(forms.Form):
    job_id = forms.IntegerField()
    resume_id = forms.IntegerField()
    # You may add other fields if needed for additional data

    def clean(self):
        cleaned_data = super().clean()
        job_id = cleaned_data.get("job_id")
        resume_id = cleaned_data.get("resume_id")

        # Optional: Add custom validation if needed
        # Example: Ensure job_id and resume_id are positive integers
        if job_id <= 0:
            self.add_error('job_id', 'Job ID must be a positive integer.')
        if resume_id <= 0:
            self.add_error('resume_id', 'Resume ID must be a positive integer.')
        
        return cleaned_data