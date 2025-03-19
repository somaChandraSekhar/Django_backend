from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyDataViewSet, upload_excel, start_generate_random_data, 
    stop_generate_random_data, revenue_bar_chart_data, 
    country_pie_chart_data, dynamic_chart_data
)

router = DefaultRouter()
router.register(r'data', CompanyDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', upload_excel, name='upload_excel'),
    path('generate/start/', start_generate_random_data, name='start_generate_random_data'),
    path('generate/stop/', stop_generate_random_data, name='stop_generate_random_data'),
    path('charts/revenue/', revenue_bar_chart_data, name='revenue_bar_chart_data'),
    path('charts/country/', country_pie_chart_data, name='country_pie_chart_data'),
    path('charts/dynamic/', dynamic_chart_data, name='dynamic_chart_data'),
]