from django.shortcuts import render,redirect
from firebase_admin import firestore
from datetime import date
from django.http import JsonResponse
import json, re

db = firestore.client()
db_connect_customer = db.collection('customer')
db_connect_product = db.collection('product')
db_connect_invoice = db.collection('invoice')
data = []


def is_unique(field_name, value):
     query = db_connect_customer.where(field_name, '==', value)
     docs = query.get()
     return len(docs) == 0

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
     return render(request, 'invoice/invoice.html',{'data':cus_data,'pro_data':pro_data,'today':today,})

def fetch_data(request):
     global data,invoice_gen
     selected_option = request.GET['option']
     try:
          d = db_connect_customer.where("company_name",'==',selected_option).get()
          for doc in d:
               id = doc.id
               single = doc.to_dict()  # Convert Firestore document to Python dictionary
               o_order = single["order_number"]
               invoice_gen = f"#{id}-{o_order}"
          data = [single["person_name"],single["contact"],single["address"],single["order_number"],single["company_name"],invoice_gen,single["country"],single["state"],single["zip_code"]]
     except:
          new_client_name = selected_option
          invoice_gen = "_N789456147AA-00"
          data = ["default","00","A","0","#NEW",invoice_gen,new_client_name]
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
          if len(data) == 10:
               companyName = data[6]
          else:
               companyName = data[4]
          if is_unique('company_name', companyName):
               n_c = {
                    'company_name': companyName,
                    'person_name': "",
                    'contact': "",
                    'email': "",
                    'address': "",
                    'city': "",
                    'state': "",
                    'country': "",
                    'zip_code': "",
                    'order_number':0,
               }
               db_connect_customer.add(n_c)
          global invoice_gen
          if invoice_gen == "_N789456147AA-00":
               d = db_connect_customer.where("company_name",'==',companyName).get()
               for doc in d:
                    id = doc.id
                    invoice_gen = f"#{id}-0"
          table_data_json = request.POST.get('table_data')
          prod_data = json.loads(table_data_json)
          total = request.POST.get('total_amount')
          bill_date = request.POST.get('billdate')
          invoice_data = {
               'company_name': companyName,
               'date': bill_date,
               'total_amount': float(total),
               'invoice_number': invoice_gen,
               'paid' : False,
               'ordered_products': [{'sno': i[1], 'product_name': i[2] ,'qty': int(i[3]) ,'unit_price': float(i[4]),'sub_total': i[5]} for i in prod_data]
          }
          for i in prod_data:
               product_info = db_connect_product.where("product_name",'==',i[2]).get()
               for p in product_info:
                    p_id = p.id
                    q_old = p.to_dict()["qty_sold"]
                    p_ref = db_connect_product.document(p_id)
                    p_ref.update({"qty_sold": q_old +int(i[3]) }) 
                    
          db_connect_invoice.add(invoice_data)
          customer_invoice = db_connect_customer.where("company_name",'==',companyName).get()
          for c in customer_invoice:
               c_id = c.id
               o_order = c.to_dict()["order_number"]
               c_ref = db_connect_customer.document(c_id)
               c_ref.update({"order_number": o_order +1 })
     else:
          print("ee")
     return redirect('invoices:view_invoice')


def view_invoice(request):
     invoices = db_connect_invoice.get()
     invoice_data = []
     for doc in invoices:
          i_data = doc.to_dict()  # Convert Firestore document to Python dictionary
          invoice_data.append(i_data)
     if request.method=="POST":
          button_mark_value = request.POST.get('mark')
          button_delete_value = request.POST.get('delete')
          button_view_value = request.POST.get('view')
          if(button_mark_value):
               req_i = db_connect_invoice.where("invoice_number","==",button_mark_value).get()
               for r in req_i:
                    r_id = r.id
                    i_ref = i_ref = db_connect_invoice.document(r_id)
                    i_ref_d = i_ref.get().to_dict()
                    if i_ref_d["paid"]:
                         i_ref.update({"paid": False })
                    else:
                         i_ref.update({"paid": True })
               return redirect('invoices:view_invoice')
          elif(button_view_value):
               req_i = db_connect_invoice.where("invoice_number","==",button_view_value).get()
               for r in req_i:
                    ri_doc = r.to_dict()
               matches = re.search(r'#(.*?)-', button_view_value)
               c_ref = db_connect_customer.document(matches.group(1)).get().to_dict()
               return render(request, "invoice/template.html",{"r_data": ri_doc,"c_data":c_ref})
               
     return render(request, "invoice/view_invoice.html",{'invoice_data': invoice_data})