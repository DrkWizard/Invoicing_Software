from django.shortcuts import render,redirect
from firebase_admin import firestore

db = firestore.client()
db_connect = db.collection('product')

def product(request):
     return render(request, 'product/product.html')

def new_product(request):
     print("hello")
     if request.method == 'POST':
          product_name = request.POST['product_name']
          amount = request.POST['amount']
          description = request.POST['description']
          data = {
               'product_name': product_name,
               'amount': amount,
               'description': description,
          }
          db_connect.add(data)
     return redirect("products:product") 