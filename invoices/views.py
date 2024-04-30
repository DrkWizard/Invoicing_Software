from django.shortcuts import render,redirect
from firebase_admin import firestore
from datetime import date
from django.http import JsonResponse

db = firestore.client()
db_connect_customer = db.collection('customer')
db_connect_product = db.collection('product')

data = []

def invoice(request):
     global data
     data = []
     today = date.today().isoformat() 
     customers = db_connect_customer.get()
     products = db_connect_product.get()
     cus_data = []
     pro_data = []
     for doc in customers:
          user_data = doc.to_dict()  # Convert Firestore document to Python dictionary
          cus_data.append(user_data)
     for doc1 in products:
          prod_data = doc1.to_dict()  # Convert Firestore document to Python dictionary
          pro_data.append(prod_data)
     return render(request, 'invoice/invoice.html',{'data':cus_data,'pro_data':pro_data,'today':today})


def fetch_data(request):
     global data
     selected_option = request.GET['option']
     if selected_option == "default":
          data = ["select a client"]
     else:
          d = db_connect_customer.where("company_name",'==',selected_option).get()
          for doc in d:
               single = doc.to_dict()  # Convert Firestore document to Python dictionary
          data = [single["person_name"],single["contact"],single["address"],single["order_number"],single["company_name"]]
     return JsonResponse({'data': data})

def fetch_data_product(request):
     selected_option = request.GET['option']
     p = db_connect_product.where("product_name",'==',selected_option).get()
     if p:
          for doc1 in p:
               product_selected = doc1.to_dict()  # Convert Firestore document to Python dictionary
          res = [product_selected["amount"]]
     else:
          res  = [""]
     return JsonResponse({'res':res} )


def generate_invoice(request):
     if request.method == 'POST' and len(data):
          customer_invoice = db_connect_customer.where("company_name",'==',data[4]).get()
          for c in customer_invoice:
               c_id = c.id
               o_order = c.to_dict()["order_number"]
               c_ref = db_connect_customer.document(c_id)
               c_ref.update({"order_number": o_order +1 })     
     else:
          print("ee")
     return redirect('invoices:invoice')