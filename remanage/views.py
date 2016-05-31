from django.shortcuts import render

def index(request):
    return render(request, 'remanage/templates/dashboard.html')