from django.urls import path
from . import views

app_name = 'invoices' 


urlpatterns = [
    path('', views.invoice, name='invoice'),
    path('view/', views.view_invoice, name='view_invoice'),
    path('fetch_data/', views.fetch_data, name='fetch_data'),
    path('fetch_data_product/', views.fetch_data_product, name='fetch_data_product'),
    path('generate/', views.generate_invoice, name='generate_invoice'),
]
