from django.urls import path

from . import views

app_name = 'payroll_app'

urlpatterns = [
    path('labour', views.Table.as_view(), name='labour_index'),
    path('labour/set-labour', views.set_labour, name='set_labour')
]
