from django.shortcuts import render,redirect
from firebase_admin import firestore
from datetime import date
from django.http import JsonResponse

db = firestore.client()
db_connect_customer = db.collection('customer')


def invoice(request):
     today = date.today().isoformat() 
     customers = db_connect_customer.get()
     cus_data = []
     for doc in customers:
          user_data = doc.to_dict()  # Convert Firestore document to Python dictionary
          cus_data.append(user_data)
     return render(request, 'invoice/invoice.html',{'data':cus_data,'today':today})


def fetch_data(request):
     selected_option = request.GET['option']
     if selected_option == "default":
          data = ["select a client"]
     else:
          d = db_connect_customer.where("company_name",'==',selected_option).get()
          for doc in d:
               single = doc.to_dict()  # Convert Firestore document to Python dictionary
          data = [single["person_name"],single["contact"]]
     return JsonResponse({'data': data})