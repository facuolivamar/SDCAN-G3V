from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
# from .models import CSVData

def index(request):
    return render(request, "interfaceApp/dashboard.html")
