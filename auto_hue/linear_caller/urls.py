from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:circadian_job_name>'),
]
