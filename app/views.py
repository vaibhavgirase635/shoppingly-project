from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views import View
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        nuts = Product.objects.filter(category='N')
        oils = Product.objects.filter(category='CO')
        pasta = Product.objects.filter(category='P')
        special = Product.objects.filter(category='SO')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,
        'mobiles':mobiles, 'totalitem':totalitem, 'nuts':nuts, 'oils':oils, 'pasta':pasta, 'Special':special})

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        review = ReviewRating.objects.filter(product=product, status=True)
        item_already_in_cart = False
        if not request.user.is_authenticated:
            return redirect('login')
        totalitem = len(Cart.objects.filter(user=request.user))
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        try:
            orderproduct = OrderPlaced.objects.filter(user=request.user, product=product).exists()
        except OrderPlaced.DoesNotExist:
            orderproduct = None
        return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart,
        'totalitem':totalitem, 'reviews':review, 'orderproduct':orderproduct})



def add_to_cart(request):
    
    user=request.user
    product_id = request.GET.get('prod_id')
    print(product_id)
    product = Product.objects.get(id=product_id)
    Cart(product=product, user=user).save()  
    #return render(request, 'addtocart.html')
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        totalitem = 0
        user = request.user
        
        cart =Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product= [ p for p in Cart.objects.all() if p.user == user]
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product= [ p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            

        data ={
            'quantity': c.quantity,
            'amount':  amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        #print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product= [ p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            

        data ={
            'quantity': c.quantity,
            'amount':  amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        #print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product= [ p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            
        data ={
            'amount':  amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

def update_address(request,id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        fm = CustomerProfileForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('address')
    else:
        pi = Customer.objects.get(pk=id)
        fm = CustomerProfileForm(instance=pi)
    return render(request, 'app/updateaddress.html', {'form':fm})

def delete_address(request,id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        pi.delete()
        return redirect('address')

def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op, 'totalitem':totalitem})


def mobile(request, data=None):
    print(data)
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'OPPO' or data == 'ViVo':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'iPhone' or data == 'ViVo':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data =='below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data =='above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def atta(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    attas = Product.objects.filter(category='A')
    return render(request, 'app/atta.html', {'attas':attas, 'totalitem':totalitem})

def chhola(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    chholas = Product.objects.filter(category='C')
    print(chholas)
    return render(request, 'app/chhola.html', {'chholas':chholas, 'totalitem':totalitem})

def CookingOil(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    oils = Product.objects.filter(category='CO')
    print(oils)
    return render(request, 'app/cookingoil.html', {'oils':oils, 'totalitem':totalitem})

def Kitchen(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    kitchen = Product.objects.filter(category='K')
    print(kitchen)
    return render(request, 'app/kitchen.html', {'kitchen':kitchen, 'totalitem':totalitem})

def Rice(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    rice = Product.objects.filter(category='R')
    print(rice)
    return render(request, 'app/rice.html', {'rice':rice, 'totalitem':totalitem})

def Dal(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    dal = Product.objects.filter(category='DP')
    print(dal)
    return render(request, 'app/dal.html', {'dal':dal, 'totalitem':totalitem})

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerregistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self, request):
        form = CustomerregistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('profile')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'app/login.html')

def selectaddress(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product= [ p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount
    
    
    return render(request, 'app/selectaddress.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})


def payment_done(request):
    user = request.user
    #print(user)
    custid = request.POST.get('custid')
    #print(custid)
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    #print(cart)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        
    return redirect("checkout")

def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    for i in cart_items:
        order = OrderPlaced.objects.filter(user=user, product=i.product.id)
        #print(order)
    for j in order:
        add = Customer.objects.get(id=j.customer.id)
        print(add)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product= [ p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount
    
    client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
    payment = client.order.create({'amount':totalamount*100, 'currency':'INR', 'payment_capture':1})
    p.razorpay_order_id = payment['id']
    p.save()
    order_id = payment['id']
    #print(payment)
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 
                'payment':payment, 'order_id':order_id, 'user':request.user})



class ProfileView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form':form,'active':'btn-primary'})



# My Reviews
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

def search(request):
    if request.method == 'GET':
        query = request.GET.get('Search')
        
        if query is not None:
            data = (Q(title__icontains=query)|Q(brand__icontains=query)|Q(category__icontains=query))
           
            product = Product.objects.filter(data)
            
            return render(request, 'app/search.html',{'product':product})
        else:
            return render(request, 'app/search.html')
    else:
        return render(request, 'app/search.html')


@csrf_exempt
def success(request):
    if request.method == "POST":
        user = request.user.id
        
        user = request.POST.get('custid')
        #print(user)
        a = request.POST
        #print(a)
        order_id = ""
        for key,val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        
        cart = Cart.objects.filter(razorpay_order_id=order_id)
        for c in cart:
            
            c.delete()
    return redirect('orders')

