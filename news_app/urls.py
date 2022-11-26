from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('register/', views.register),
    path('scrape/', views.scrape),
    path('logout/',views.logout)
]
