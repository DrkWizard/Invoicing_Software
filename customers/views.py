from django.shortcuts import render,redirect
from firebase_admin import firestore


db = firestore.client()
db_connect = db.collection('customer')

def is_unique(field_name, value):
     query = db_connect.where(field_name, '==', value)
     docs = query.get()
     return len(docs) == 0



def customer(request):
     button_search_value = request.GET.get('searchInput', '')
     if button_search_value !=  "":
          customers = db_connect.where("company_name",'==',button_search_value).get()
          cus_data = []
          for doc in customers:
               user_data = doc.to_dict()  # Convert Firestore document to Python dictionary
               cus_data.append(user_data)
     else:
          button_search_value = ""
          customers = db_connect.get()
          cus_data = []
          for doc in customers:
               user_data = doc.to_dict()  # Convert Firestore document to Python dictionary
               cus_data.append(user_data)
          
     return render(request, 'customer/customer.html',{'cus_data': cus_data, "input":button_search_value})

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
     if is_unique('company_name', company_name):
          data = {
               'company_name': company_name,
               'person_name': person_name,
               'contact': contact_number,
               'email': email,
               'address': address,
               'city': city,
               'state': state,
               'country': country,
               'zip_code': zipcode,
               'order_number':0,
          }
          db_connect.add(data)
          
     else:
          print("Error")
     return redirect("customers:customer")

def del_customer(request):
     if request.method == 'POST':
          button_del_value = request.POST.get('del_button')
          button_edit_value = request.POST.get('edit_button')
          if(button_del_value):
               del_data = db_connect.where("company_name",'==',button_del_value).get()
               for d in del_data:
                    doc_ref = db_connect.document(d.id)
                    doc_ref.delete()
          if(button_edit_value):
               return redirect("customers:edit_customer", companyName=button_edit_value)
     return redirect("customers:customer")


def edit_customer(request, companyName):
     customer_ref = db_connect.where("company_name", '==', companyName).get()[0].reference
     customer = customer_ref.get().to_dict()
     if request.method == 'POST' and request.POST.get('save'):
          updated_data = {
               'person_name': request.POST.get('person_name'),
               'contact': request.POST.get('contact_number'),
               'email': request.POST.get('email'),
               'address': request.POST.get('address'),
               'state': request.POST.get('state'),
               'zip_code': request.POST.get('zipcode'),
               'country': request.POST.get('country'),
               'city': request.POST.get('city'),
          }
          customer_ref = db_connect.where("company_name", '==', companyName).get()[0].reference
          customer_ref.update(updated_data)
          return redirect("customers:customer")
     elif request.method=='POST':
          return redirect("customers:customer")
     return render(request, 'customer/edit.html',{'contact': customer['contact'],'company_name' : companyName,'person_name':customer['person_name'],'email': customer['email'],'address':customer['address'],
                                                  'state': customer['state'],'zip_code': customer['zip_code'],'country': customer['country'], 'city':customer['city'] })
