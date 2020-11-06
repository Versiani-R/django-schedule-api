from django.urls import path, include

from api import views


urlpatterns = [
    path('', views.index, name='index'),

    path('register/', views.RegisterView.as_view(), name='register'),
    # path('register/', views.register, name='register'),
    # path('register/user/', views.handle_register, name='handle_register'),

    path('api/', views.ScheduleApi.as_view(), name='schedule'),

    path('api/time/', views.TimeListView.as_view(), name='time'),


    # path('api/schedule/', views.api_schedule, name='schedule'),
    # path('api/time/', views.api_time, name='time'),
]
