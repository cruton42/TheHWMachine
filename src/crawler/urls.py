from django.contrib import admin
from django.urls import path
from crawler import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('crawl/', views.crawl_view, name='crawl'),
    path('jobcrawl/', views.jobcrawl_view, name='jobcrawl'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('upload-pdf/', views.upload_pdf_view, name='upload_pdf'),
    path('success/', views.success_view, name='success'),
]