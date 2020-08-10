from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index (request):
    text="Django Kurulumu : pip install django <br> Proje Oluşturma : django-admin startproject mysite <br> App Ekleme : python manage.py startapp polls <br> Server Etkinleştirme : python manage.py runserver"
    context = {'text': text}
    return render(request, 'index.html', context)