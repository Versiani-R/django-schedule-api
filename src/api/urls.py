from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api_index, name='api'),
    path('api/detail/<int:day>-<int:month>-<int:year>/', views.api_detail, name='detail'),
    path('api/schedule/', views.api_schedule, name='schedule'),
    path('api/error/<int:error_code>/', views.api_error, name='schedule_error'),
]
