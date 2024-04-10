from django.urls import path
from . import views

app_name = 'products' 

urlpatterns = [
    path('', views.product, name='product'),
    path('addnew/', views.new_product, name='new_product'),
]
