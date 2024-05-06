from django.urls import path
from . import views

app_name = 'customers' 

urlpatterns = [
    path('', views.customer, name='customer'),
    path('addnew/', views.new_customer, name='new_customer'),
    path('delcustomer/', views.del_customer, name='del_customer'),
    path('editcustomer/<str:companyName>/', views.edit_customer, name='edit_customer')
]
