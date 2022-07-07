import email
from itertools import product
import re
from django.shortcuts import redirect, render

from seller.models import *

# Create your views here.

def seller_index(request):
    return render(request,'seller-index.html')

def seller_login(request):
    if request.method=='POST':
        try:
            sellerobj=seller.objects.get(email=request.POST['email'])
            if request.POST['password']==sellerobj.password:
                request.session['email']=sellerobj.email
                request.session['name']=sellerobj.name
                return render(request, 'seller-index.html')
            else:
                return render(request,'seller-login.html', {'msg':'Wrong Password'})
        except:
            return render(request,'seller-login.html', {'msg':'Email not found'})

    return render(request,'seller-login.html')

def add_product(request):
    sellerobj=seller.objects.get(email=request.session['email'])
    if request.method=='POST':
        if 'pic' in request.FILES:
            Product.objects.create(
            seller=sellerobj,
            name=request.POST['name'],
            des=request.POST['des'],
            price=request.POST['price'],
            quantity=request.POST['quantity'],
            discount=request.POST['discount'],
            pic=request.FILES['pic']
        )
        else:
            Product.objects.create(
            seller=sellerobj,
            name=request.POST['name'],
            des=request.POST['des'],
            price=request.POST['price'],
            quantity=request.POST['quantity'],
            discount=request.POST['discount'],
            #pic=request.FILES['pic']
            )
    return render(request,'add-product.html')

def manage_products(request):
    sellerobj=seller.objects.get(email=request.session['email'])
    plist = Product.objects.filter(seller=sellerobj)
    return render(request,'manage-products.html',{'productdata':plist})

def seller_logout(request):
    del request.session['email']
    del request.session['name']
    return redirect('seller-login')

def edit_product(request,pid):
    productobj=Product.objects.get(id=pid)
    if request.method=='POST':
        productobj.name=request.POST['name']
        productobj.des=request.POST['des']
        productobj.price=request.POST['price']
        productobj.quantity=request.POST['quantity']
        productobj.discount=request.POST['discount']
        if 'pic' in request.FILES:
            productobj.pic=request.FILES['pic']
        productobj.save()
        return redirect('manage-products')
    return render(request,'edit-product.html',{'productobj':productobj})

def delete_product(request,pid):
    productobj=Product.objects.get(id=pid)
    productobj.delete()
    return redirect('manage-products')