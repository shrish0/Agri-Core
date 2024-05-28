from django.shortcuts import render,redirect
from krishi.models import *

# Create your views here.
def show(request,id):
    sell1=selling.objects.filter(product=id).all()
    return render(request,"show.html",{"sell1":sell1,"id":id})
