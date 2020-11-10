from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from api import views


router = DefaultRouter()
router.register(r'register', views.RegisterViewSet, basename='register')
router.register(r'api', views.ScheduleApiViewSet, basename='api')
router.register(r'calls', views.ApiCallsViewSet, basename='calls')


urlpatterns = [
    path('', views.index, name='index'),
    path('', include(router.urls)),
    path('docs/', get_schema_view(
        title='Schedule Api',
        description='A simple-core, well documented api, for schedules.'
    ), name='openapi-schema')
]
