from django.contrib import admin
from django.urls import path
from crawler import views
from django.contrib.auth import views as auth_views
from .views import custom_logout_view
from .views import generate_cover_letter, no_resume
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('jobcrawl/', views.jobcrawl_view, name='jobcrawl'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('upload-pdf/', views.upload_pdf_view, name='upload_pdf'),
    path('success/', views.success_view, name='success'),
    path('generate-cover-letter/<int:job_id>/', generate_cover_letter, name='generate_cover_letter'),
    path('no-resume/', no_resume, name='no_resume'),
    path('error/', views.error_view, name='error'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)