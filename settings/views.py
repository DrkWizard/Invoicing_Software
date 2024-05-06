from django.shortcuts import render,redirect
from firebase_admin import firestore

def setting(request):
    return render(request, 'setting/setting.html')
