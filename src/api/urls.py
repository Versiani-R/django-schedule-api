from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register/user/', views.handle_register, name='handle_register'),
    path('api/schedule/', views.api_schedule, name='schedule'),
    path('api/time/', views.api_time, name='time'),
]
