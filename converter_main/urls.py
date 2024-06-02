from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name="home-page"),
    path('download-ready-file/', views.import_file, name="download-ready-file")
]