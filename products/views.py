from django.shortcuts import render,redirect
from firebase_admin import firestore

db = firestore.client()
db_connect = db.collection('product')


def is_unique(field_name, value):
     query = db_connect.where(field_name, '==', value)
     docs = query.get()
     return len(docs) == 0

def product(request):
     button_search_value = request.GET.get('searchInput', '')
     if button_search_value !=  "":
          products = db_connect.where("product_name",'==',button_search_value).get()
          pro_data = []
          for doc in products:
               prod_data = doc.to_dict()  # Convert Firestore document to Python dictionary
               pro_data.append(prod_data)
     else:
          products = db_connect.get()
          pro_data = []
          for doc in products:
               prod_data = doc.to_dict()  # Convert Firestore document to Python dictionary
               pro_data.append(prod_data)
     return render(request, 'product/product.html',{'pro_data': pro_data, "input":button_search_value})

def new_product(request):
     print("hello")
     if request.method == 'POST':
          product_name = request.POST['product_name']
          amount = request.POST['amount']
          description = request.POST['description']
          if is_unique('product_name', product_name):
               amount = float(amount)
               data = {
                    'product_name': product_name,
                    'amount': amount,
                    'description': description,
               }
               db_connect.add(data)
          else:
               print("Error")
     return redirect("products:product") 

def del_product(request):
     if request.method == 'POST':
          button_del_value = request.POST.get('del_button')
          button_edit_value = request.POST.get('edit_button')
          print(button_del_value)
          if(button_del_value):
               print("Delete")
               del_data = db_connect.where("product_name",'==',button_del_value).get()
               for d in del_data:
                    doc_ref = db_connect.document(d.id)
                    doc_ref.delete()
          if(button_edit_value):
               print("edit")
     return redirect("products:product")