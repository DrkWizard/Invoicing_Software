from django.shortcuts import render
from firebase_admin import firestore

db = firestore.client()
db_connect_customer = db.collection('customer')
db_connect_product = db.collection('product')

def dashboard(request):
     a = db_connect_customer.get()
     b = db_connect_product.get()
     return render(request, 'dashboard/dashboard.html',{"customer_count":len(a),"product_count":len(b)})