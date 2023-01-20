from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from .models import CircadianTime_Named

def index(request):
    circadian_jobs = CircadianTime_Named.objects.order_by('-pub_date')
    return HttpResponse(circadian_jobs, reverse('linear_caller:index'))