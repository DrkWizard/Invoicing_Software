from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Bar,Layout
from firebase_admin import firestore

db = firestore.client()
db_connect_customer = db.collection('customer')
db_connect_product = db.collection('product')
db_connect_invoice = db.collection('invoice')

def dashboard(request):
     a = db_connect_customer.get()
     b = db_connect_product.get()
     i = db_connect_invoice.get()
     total_revenue = 0
     due = 0
     paid = 0
     for doc in i:
          d = doc.to_dict() 
          total_revenue = total_revenue + int(d["total_amount"])
          if d["paid"]:
               paid = paid+1
          else:
               due = due +1
     # x_data = []
     # y_data = []
     # for p_graph in b:
     #      d = p_graph.to_dict()
     #      x_data.append(d["product_name"])
     #      y_data.append(d["qty_sold"])
          
     # layout = Layout(title='Quantity of products sold')
     # fig = {'data': [Bar(x=x_data, y=y_data, name='product_qty')], 'layout': layout}
     # no_products = plot(fig, output_type='div')
     return render(request, 'dashboard/dashboard.html',{"customer_count":len(a),"product_count":len(b), "invoice_count":len(i), "total_revenue":total_revenue,'no_products': "","paid":paid,"due":due})