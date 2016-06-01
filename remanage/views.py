from django.shortcuts import render

def index(request):
    return render(request, 'remanage/templates/dashboard.html')

def portfolio(request):
    return render(request, 'remanage/templates/portfolio.html')
