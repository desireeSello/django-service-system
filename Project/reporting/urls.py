from django.urls import path
from . import views

app_name = 'reporting'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('submit/', views.submit_report, name='submit_report'),
    path('api/municipalities/', views.get_municipalities, name='get_municipalities'),
    path('success/<str:ref>/', views.success, name='success'),  # Changed from report_success
]