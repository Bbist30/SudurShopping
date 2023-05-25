from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, Orderplaced
from django.http import HttpResponse
from.  forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles})
    
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', 
        {'product': product})
    

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        total_amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount

        return render(request, 'app/addtocart.html', {'carts': cart, 'total_amount': total_amount, 'amount':amount})
    else:
        return render(request, 'app/emptycart.html')
    

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
       



        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount' : amount + shipping_amount
        }
        
        return JsonResponse(data)
    
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        



        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount' : amount + shipping_amount
        }
        
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
       

        data = {
            
            'amount': amount,
            'totalamount' : amount + shipping_amount
        }
        
        return JsonResponse(data)




def buy_now(request):
    return render(request, 'app/buynow.html')

def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active': 'btn-primary'})



def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung' or data =='Nokia':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data== 'below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data== 'above': 
        mobiles= Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def topwear(request, ): 
  return render(request, 'app/topwear.html', {'topwears':topwear})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Sucessfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})






def login(request):
    return render(request, 'app/login.html')



def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        total_amount = amount + shipping_amount
    
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': total_amount,'cart_items':cart_items})


def orders(request):
    op=Orderplaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_place':op})


def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Orderplaced(user=user, customer=customer, product=c.product, quantity=c.quantity,).save()
        c.delete()
    return redirect("orders")



    
   
           


  

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
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
            messages.success(request, 'Congratulations!! Profile updated successfully.')
            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
        else:
            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
