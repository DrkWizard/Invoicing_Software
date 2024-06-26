from django.urls import path
from . import views

app_name = 'products' 

urlpatterns = [
    path('', views.product, name='product'),
    path('addnew/', views.new_product, name='new_product'),
    path('delproduct/', views.del_product, name='del_product'),
    path('editproduct/<str:productName>/', views.edit_product, name='edit_product')
]
