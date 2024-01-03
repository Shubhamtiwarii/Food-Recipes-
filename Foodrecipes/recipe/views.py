from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.
def index(request):
    
    if request.method=='POST':
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        custome=request.POST.get('customer')
        print(custome)
        #print(product)
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1
        
        request.session['cart']=cart
        print('cart',request.session['cart'])
        #print(cart)
        return redirect('homepage')
    else:    
    #products=Product.get_all_products()
        
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}
        products=None
        #request.session.get('cart').clear()
        #request.session.clear()
        
        categories=Category.get_all_categories()
    #print(products)
        categoryID=request.GET.get('category')
        if categoryID:
            products=Product.get_all_products_by_categoryid(categoryID)
        else:
            if 'q' in request.GET:
                q=request.GET['q']
                products=Product.objects.all().filter(name__icontains=q)
            else:
                products=Product.get_all_products()
        data={}
        data['products']=products
        data['categories']=categories
        #data['data']=data
        #print('Your are:',request.session.get('email'))

    #return render(request,'orders/order.html')
    #return render(request,'index.html',{'products':products})
    return render(request,'index.html',data)

def validateCustomer(customer):
    error_message=None
    if(not customer.first_name):
        error_message="Firstname Required!!"
    elif(not customer.last_name):
        error_message="Lastname Required"
    elif len(customer.phone)<10:
        error_message="Phone Number must be a 10 digit"
    elif(not customer.email):
        error_message="Email Must Be Required!!"
    #elif(email==Customer.objects.filter(email=email).exists):
    #    error_message='Email Is Already Exist Please Login'
    elif(not customer.password):
        error_message="Password Must Be Required!!"
    elif customer.isExists():
        error_message='Email Address Already Registered'
    return error_message

def registerUser(request):
    fname=request.POST.get('firstname')
    lname=request.POST.get('lastname')
    phone=request.POST.get('phone')
    email=request.POST.get('email')
    password=request.POST.get('password')
        #vALIDATION
    value={
        'fname':fname,
        'lname':lname,
        'phone':phone,
        'email':email,
        'password':password
        }
    error_message=None
    customer=Customer(first_name=fname,last_name=lname,phone=phone,email=email,password=password)
        
    error_message=validateCustomer(customer)

    if not error_message:
        customer.password=make_password(customer.password)
        customer.register()
        return redirect('homepage')
    else:
        data={
            'error':error_message,
            'values':value
            }
        return render(request,'signup.html',data)


def signup(request):

    if request.method=='GET':
    #print(request.method)
        return render(request,'signup.html')
    else:
        return registerUser(request)
    
def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        
        email=request.POST.get('email')
        password=request.POST.get('password')
        customer=Customer.get_customer_by_email(email)
        error_message=None

        #print(customer)
        
        #print(email,password)
        if customer:
            flag=check_password(password , customer.password)
            if flag:
                request.session['customer']=customer.id
                request.session['email']=customer.email
                #request.session['email']=customer.email
                return redirect('homepage')
            else:
                error_message='Email Or Password Invalid'
        else:
            error_message='Email Or Password Invalid'
        return render(request,'login.html',{'error':error_message})
    
def logout(request):
        request.session.clear()
        return redirect('login')

def cart(request):
        
        ids=list(request.session.get('cart').keys())
        products=Product.get_products_by_id(ids)
        print(products)
        return render(request,'cart.html',{'products':products})

def checkout(request):
        
        if request.method=="POST":
            address=request.POST.get('address')
            phone=request.POST.get('phone')
            customer=request.session.get('customer')
            cart=request.session.get('cart')
            products=Product.get_products_by_id(list(cart.keys()))

            print(address,phone,customer,cart,products)

            for product in products:
                print(cart.get(str(product.id)))
                order=Order(customer=Customer(id=customer),product=product,price=product.price,address=address,phone=phone,quantity=cart.get(str(product.id)))
                order.save()
            request.session['cart']={}
            return redirect('cart')
       
def orders(request):
        #if request.method=='GET':
        customer=request.session.get('customer')
        #order=Order.objects.all()
        #customer=Customer.objects.get(id=customer)
        orders=Order.get_orders_by_customer(customer)
        paginator=Paginator(orders,5)
        page=request.GET.get('page')
        orders=paginator.get_page(page)
        print(orders)

        return render(request,'orders.html',{'orders':orders})

def addcategory(request):
    category=Category.objects.all()
    if request.method=="POST":
        category=request.POST.get('category')
        print("category")
        if Category.objects.filter(name=category).exists():
            messages.error(request,'Category Already Exist')
            return redirect('addcategory')
        else:
            C=Category.objects.create(name=category)   #category=Category() Alternet option to save data
            C.save()   #category.name=request.POST.get('category') 
                    #category.save() 
            messages.success(request,"Category Added Successfully")  
            return render(request,"addcategory.html",{'category':category})
    else:
        return render(request,"addcategory.html",{'category':category})
    

        
        
def addproduct(request):
    category=Category.objects.all()
    product=Product.objects.all()
    if request.method=="POST" and request.FILES['myfile']:     
        name=request.POST.get('name')
        price=request.POST.get('price')
        category_id=request.POST.get('category')
        categoryy=Category.objects.get(id=category_id)
        description=request.POST.get('description')
        print(categoryy)
        if len(request.FILES) != 0:
            img=request.FILES['myfile']
        if Product.objects.filter(name=name).exists():
            messages.error(request,'Product Already Exist')
            return redirect('addproduct')
        else:
            p=Product.objects.create(name=name,price=price,category=categoryy,description=description,image=img)
            p.save()
            messages.success(request,"Product Added Successfully")
            return render(request,"addproduct.html",{'product':product,'category':category})
    else:
        return render(request,"addproduct.html",{'product':product,'category':category})

def detail(request,id):
    product=Product.objects.get(id=id)
    
    return render(request,"detail.html",{'product':product})