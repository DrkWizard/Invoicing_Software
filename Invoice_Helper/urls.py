from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('',include('dashboard.urls',namespace='dashboard')),
    path('customers/', include('customers.urls',namespace='customers') ),
    path('products/', include('products.urls', namespace='products')),
    path('invoices/', include('invoices.urls', namespace='invoices')),
    path('settings/', include('settings.urls', namespace='settings')),
    path('admin/', admin.site.urls),
]