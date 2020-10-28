from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # path('api/', views.api_index, name='api'),
    # path('api/detail/', views.api_detail, name='detail'),
    path('register/', views.register, name='register'),
    path('register/success', views.handle_register, name='handle_register'),
    path('api/schedule/', views.api_schedule, name='schedule'),
    # path('api/error/<int:error_code>/', views.api_error, name='schedule_error'),
    # path('api/success/<int:day>-<int:month>-<int:year>/<int:hours>-<int:minutes>/<str:company_name>/',
    #      views.api_success,
    #      name='schedule_success'),
]
