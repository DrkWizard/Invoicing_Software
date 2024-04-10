from django.contrib import admin
from django.urls import include, path

urlpatterns = [
     path('',include('dashboard.urls',namespace='dashboard')),
    path('customers/', include('customers.urls',namespace='customers') ),
    path('products/', include('products.urls', namespace='products')),
    path('admin/', admin.site.urls),
]