from django.urls import path

from . import views

urlpatterns = [
    path('', views.monitor, name='monitor'),
    path('/chart_data',views.chart_data, name='chart_data')
]