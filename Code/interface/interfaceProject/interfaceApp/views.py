from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
# from .models import CSVData

def csv_data_view(request):
    # data = CSVData.objects.all()
    data = 'all okey'
    return render(request, 'interfaceApp/csv_data.html', {'data': data})
