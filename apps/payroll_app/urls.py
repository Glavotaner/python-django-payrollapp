from django.urls import path

from . import views

app_name = 'payroll_app'

urlpatterns = [
    path('', views.select_period, name='select_period'),
    
]
