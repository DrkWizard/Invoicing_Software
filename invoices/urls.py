from django.urls import path
from . import views

app_name = 'invoices' 


urlpatterns = [
    path('', views.invoice, name='invoice'),
    path('fetch_data/', views.fetch_data, name='fetch_data'),
    path('fetch_data_product/', views.fetch_data_product, name='fetch_data_product'),
]
