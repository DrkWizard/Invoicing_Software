from django.shortcuts import render,redirect
from firebase_admin import firestore


db = firestore.client()
db_connect = db.collection('customer')

def customer(request):
     return render(request, 'customer/customer.html')

def new_customer(request):
     company_name = request.POST['company_name']
     person_name = request.POST['person_name']
     contact_number = request.POST['contact_number']
     email = request.POST['email']
     address = request.POST['address']
     city = request.POST['city']
     state = request.POST['state']
     zipcode = request.POST['zipcode']
     country = request.POST['country']
     data = {
          'company_name': company_name,
          'person_name': person_name,
          'contact': contact_number,
          'email': email,
          'address': address,
          'city': city,
          'state': state,
          'country': country,
          'zip_code': zipcode
     }
     db_connect.add(data)
     return redirect("customers:customer") 
     