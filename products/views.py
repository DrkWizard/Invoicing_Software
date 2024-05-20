from django.shortcuts import render,redirect
from firebase_admin import firestore

db = firestore.client()
db_connect = db.collection('product')

print("hello")
def is_unique(field_name, value):
     query = db_connect.where(field_name, '==', value)
     docs = query.get()
     return len(docs) == 0
print("JIII")
def product(request):
     products = db_connect.get()
     pro_data = []
     for doc in products:
          prod_data = doc.to_dict()  # Convert Firestore document to Python dictionary
          pro_data.append(prod_data)
     return render(request, 'product/product.html',{'pro_data': pro_data})

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
                    'qty_sold':0,
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
               return redirect("products:edit_product", productName=button_edit_value)
     return redirect("products:product")


def edit_product(request, productName):
     product_ref = db_connect.where("product_name", '==', productName).get()[0].reference
     product = product_ref.get().to_dict()
     if request.method == 'POST' and request.POST.get('save'):
          updated_data = {
               'amount': request.POST.get('amount'),
               'description': request.POST.get('description'),
          }
          product_ref = db_connect.where("product_name", '==', productName).get()[0].reference
          product_ref.update(updated_data)
          return redirect("products:product")
     elif request.method=='POST':
          return redirect("products:product")
     return render(request, 'product/edit.html',{'amount': product['amount'],'product_name' : productName,'description':product['description']})
