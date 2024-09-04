from django.contrib import admin
from django.urls import path
from crawler import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crawl/', views.crawl_view, name='crawl'),
    path('', views.home),
]