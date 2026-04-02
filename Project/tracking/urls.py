# tracking/urls.py
from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),  
    path('track/<str:ref_number>/', views.report_detail_view, name='report_detail'),
]