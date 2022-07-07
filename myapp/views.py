import email
from django.http import JsonResponse,HttpResponseBadRequest
from django.shortcuts import redirect, render

from myapp.models import *
from seller.models import *

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def register(request):

    if request.method=='POST':
        try:
            userobj = User.objects.get(email=request.POST['Email'])
            return render(request,'register.html',{'msg':'Email already registered'})
        except:
            if request.POST['Password']==request.POST['Password Confirmation']:
                User.objects.create(
                    name=request.POST['Username'],
                    email=request.POST['Email'],
                    password=request.POST['Password']
                )
                return render(request,'login.html')
            else: 
                return render(request,'register.html',{'msg':'Wrong Password'})

    return render(request,'register.html')

def login(request):

    if request.method=='POST':
        try:
            userobj = User.objects.get(email=request.POST['Email'])
            if request.POST['Password']==userobj.password:
                request.session['email']=request.POST['Email']
                request.session['name']=userobj.name
                return redirect('index')
        except:
            return render(request,'login.html',{'msg':'Email not Registered'})
    
    return render(request,'login.html')

def logout(request):
    del request.session['email']
    del request.session['name']
    return redirect('login')

def products(request):
    products=Product.objects.all()
    return render(request,'products.html',{'productlist':products})

def single(request,pid):
    pobj=Product.objects.get(id=pid)
    pobj.discountedprice=pobj.price-(pobj.price*pobj.discount/100)
    return render(request, 'single.html',{'productobj':pobj}) 

# def add_to_cart(request,pid):
#     pobj=Product.objects.get(id=pid)
#     userobj = User.objects.get(email=request.session['email'])
#     Cart.objects.create(
#         product=pobj,
#         quantity=1,
#         user=userobj
#     )
#     return redirect('products')

def add_to_cart(request):
    itemobj=request.GET['pid']

    pobj=Product.objects.get(id=itemobj)
    userobj = User.objects.get(email=request.session['email'])
    Cart.objects.create(
        product=pobj,
        quantity=1,
        user=userobj
    )
    pobj.save()
    return JsonResponse({'msg':'Item Added to Cart'})

def view_cart(request):
    userobj = User.objects.get(email=request.session['email'])
    cart=Cart.objects.filter(user=userobj)
    totalamount=0
    for item in cart:
        item.product.discountedprice=item.product.price-(item.product.price*item.product.discount/100)
        item.product.discountedprice=item.product.discountedprice*item.quantity
        totalamount+= item.product.discountedprice

    return render(request,'viewcart.html',{'cartitems':cart,'totalamount':totalamount},)

def remove_product(request,pid):
    cartobj=Cart.objects.get(id=pid)
    cartobj.delete()

    return redirect('viewcart')

def updatecartqty(request):
    cartid=request.GET['id']
    qty=request.GET['qty']

    cartobj=Cart.objects.get(id=cartid)
    cartobj.quantity=qty
    cartobj.save()

    return JsonResponse({'msg':'Quantity Updated'})

def checkout(request):
    userobj = User.objects.get(email=request.session['email'])
    orderobj = Order.objects.create(
        user=userobj,
        order_status='Confirmed'
    )

    cartobj=Cart.objects.filter(user=userobj)
    for i in cartobj:
        OrderDetails.objects.create(
            product=i.product,
            quantity=i.quantity,
            order=orderobj
        )
    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'pay.html', context=context)



### Payment


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
