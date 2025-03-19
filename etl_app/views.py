from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CompanyData
from .serializers import CompanyDataSerializer
import pandas as pd
import random
import time
from django.http import StreamingHttpResponse
import json
from django.views.decorators.http import require_GET  # For plain Django view
from django.db import models
# Existing ViewSet
class CompanyDataViewSet(viewsets.ModelViewSet):
    queryset = CompanyData.objects.all()
    serializer_class = CompanyDataSerializer

# Existing Excel Upload
@api_view(['POST'])
def upload_excel(request):
    file = request.FILES['file']
    df = pd.read_excel(file)
    for _, row in df.iterrows():
        CompanyData.objects.create(
            name=row['name'],
            revenue=row['revenue'],
            profit=row['profit'],
            employees=row['employees'],
            country=row['country']
        )
    return Response({"message": "Data uploaded successfully"})

# Continuous Random Data Generation
generating = False

def generate_random_data_stream():
    global generating
    countries = ['USA', 'UK', 'India', 'China', 'Brazil']
    companies = ['A', 'B', 'C', 'D', 'E']
    while generating:
        data = {
            'name': random.choice(companies),
            'revenue': random.randint(1000, 15000),
            'profit': random.randint(100, 5000),
            'employees': random.randint(10, 1000),
            'country': random.choice(countries)
        }
        CompanyData.objects.create(**data)
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(1)

@require_GET  # Plain Django view instead of DRF api_view
def start_generate_random_data(request):
    global generating
    if not generating:
        generating = True
        response = StreamingHttpResponse(generate_random_data_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'  # Prevent caching
        return response
    return Response({"message": "Already generating"}, status=400)

@api_view(['POST'])
def stop_generate_random_data(request):
    global generating
    generating = False
    return Response({"message": "Stopped generating data"})

# Chart Data Endpoints (unchanged)
@api_view(['GET'])
def revenue_bar_chart_data(request):
    data = CompanyData.objects.filter(revenue__gt=10000).values('name', 'revenue')
    return Response(list(data))

@api_view(['GET'])
def country_pie_chart_data(request):
    data = CompanyData.objects.values('country').annotate(count=models.Count('id'))
    return Response(list(data))

@api_view(['GET'])
def dynamic_chart_data(request):
    data = CompanyData.objects.values('name', 'profit', 'employees')
    return Response(list(data))