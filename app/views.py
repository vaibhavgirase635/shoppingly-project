from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views import View
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,
        'mobiles':mobiles})

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',{'product':product})



def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(product=product, user=user).save()  
    #return render(request, 'addtocart.html')
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart =Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product= [ p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart, 'totalamount':totalamount, 'amount':amount})
        else:
            return render(request, 'app/emptycart.html')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart =Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product= [ p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart, 'totalamount':totalamount, 'amount':amount})
        else:
            return render(request, 'app/emptycart.html')
    #return render(request, 'addtocart.html')

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
            totalamount = amount + shipping_amount

        data ={
            'quantity': c.quantity,
            'amount':  amount,
            'totalamount': totalamount
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
            totalamount = amount + shipping_amount

        data ={
            'quantity': c.quantity,
            'amount':  amount,
            'totalamount': totalamount
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
            totalamount = amount + shipping_amount

        data ={
            'amount':  amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

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
 return render(request, 'app/orders.html')


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
    attas = Product.objects.filter(category='A')
    return render(request, 'app/atta.html', {'attas':attas})

def chhola(request):
    chholas = Product.objects.filter(category='C')
    print(chholas)
    return render(request, 'app/atta.html', {'chholas':chholas})

def CookingOil(request):
    oils = Product.objects.filter(category='CO')
    print(oils)
    return render(request, 'app/cookingoil.html', {'oils':oils})

def Kitchen(request):
    kitchen = Product.objects.filter(category='K')
    print(kitchen)
    return render(request, 'app/kitchen.html', {'kitchen':kitchen})

def Rice(request):
    rice = Product.objects.filter(category='R')
    print(rice)
    return render(request, 'app/rice.html', {'rice':rice})

def Dal(request):
    dal = Product.objects.filter(category='DP')
    print(dal)
    return render(request, 'app/dal.html', {'dal':dal})

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
  

def checkout(request):
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

    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items6})

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

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

