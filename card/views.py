from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Product,Contact,review,userorder
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date, datetime,timedelta

import random

def cards(request):
    product = Product.objects.all()
    return render(request,'card/index.html',{"prod":product})

def product(request):
    product = Product.objects.all()
    return render(request,'card/product.html',{"product":product})

def about(request):
    return render(request,'card/about.html')

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name',"")
        email = request.POST.get('email','')
        number = request.POST.get('number','')
        message = request.POST.get('message','')
        contact = Contact(name=name,email=email,number=number,message=message)
        contact.save()
    return render(request,'card/contact.html')



def orders(request):
    discount = random.randrange(250,300)
    if request.method =="POST":
        ids = request.POST.getlist('id','')
        if ids == ['']:
            messages.error(request, 'No any item in the Cart Please goto the Products and get Shopping')
            return render(request,'card/error.html')
        else:
            id = list(ids)
            arr = []
            for i in range(0,len(id),2):
                for j in id[i].split(','):
                    arr.append(int(j))
            product = Product.objects.filter(id__in=[i for i in arr]).values()
            return render(request,'card/order.html',{'prod':product,'discount':discount,'ids':ids})
    return redirect("/card/order/")
def search(request):
    data = request.GET['search']
    if len(data)>80:
        messages.warning(request, 'No record found')
        return render(request,'card/search.html',{"searchdata":data})
    else:
        name = Product.objects.filter(product_name__icontains=data)
        category = Product.objects.filter(category__icontains=data)
        detail = Product.objects.filter(product_detail__icontains = data)
        sub_product = name.union(category)
        main_product = sub_product.union(detail)
    return render(request,'card/search.html',{"products":main_product,"searchdata":data})

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username","")
        fname = request.POST.get("fname","")
        lname = request.POST.get("lname","")
        email = request.POST.get("email","")
        password = request.POST.get("pass","")
        cpassword = request.POST.get("cpass","")
        if len(username)>10:
            messages.error(request,"Please Enter Username in 10 character")
            return redirect("/")
        if not username.isalnum():
            messages.error(request,"Please do not use special character")
            return redirect("/")
        if(password==cpassword):
            myuser = User.objects.create_user(username,email,password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request,"Your Account successfully regestered")
            return redirect("/")
        else:
            messages.error(request,"Please Enter Correct Password")
            return redirect("/")
    else:
        messages.error(request,"Sorry Something is wrong") 
        return redirect("/")

def userlogin(request):
    if request.method == "POST":
        username = request.POST.get("username","")
        password = request.POST.get("pass","")
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are Logged in successfully")
            return redirect("/")
        else:
            messages.error(request,"Please Enter Valid username and Password")
            return redirect("/")
    else:
        return HttpResponse("404 - Not found")
def userlogout(request):
    logout(request)
    messages.success(request,"You are Successfully Logout")
    return redirect("/")

def checklist(request,id):
    product = Product.objects.filter(id = id);
    pro_id = Product.objects.get(id=id)
    review_data = review.objects.filter(product=pro_id)
    # data = Product.objects.filter(id = 6).update(product_detail = "DELL Mouse - 4022 new version for gaming",product_name = "Mouse")
    return render(request,'card/checklist.html',{'prod':product,"pro_id":id,"data":review_data})

def reviews(request):
    if request.method == "POST":
        reviews = request.POST.get("review","")
        user = request.user
        id = request.POST.get("pro_id","")
        product = Product.objects.get(id=id)
        Review = review(review = reviews,user = user, product = product)
        Review.save()
        messages.success(request,"Your comment send successfully")
        return redirect(f"/card/checklist/{id}")
    else:
        messages.error(request,"Sorry")
        return redirect(f"/card/checklist/{id}")

def orderdetails(request):
    id = random.randrange(1000,10000)
    arr = []
    if request.method == "POST":
        name = request.POST.get("name","")
        mobile = request.POST.get("number","")
        user = request.user
        address = request.POST.get("address","")
        city = request.POST.get("city","")
        state = request.POST.get("state","")
        pin = request.POST.get("pin","")
        user_order = userorder(user = user,order_id = id,o_name = name,o_mobile = mobile,o_address = address,o_city = city,o_state = state, o_pin = pin)
        user_order.save()
        messages.success(request,"Your order is successfully send")
        return redirect("/card/confirm/")
    return render(request,"card/orderdetail.html")

def confirm(request):
    user = request.user
    detail = userorder.objects.filter(user=user)
    return render(request,"card/confirm.html",{"details":detail})
 
def trackorder(request):
    progresses = 0
    if request.method == "POST":
        number = request.POST.get("number","")
        id = request.POST.get("orderid","")
        ids = request.POST.getlist("productid","")
        detail = userorder.objects.filter(o_mobile=number).filter(order_id = id)
        status = 0
        if detail.exists():
            status = 1
            new = userorder.objects.get(o_mobile = number,order_id=id)
            today = new.date
            order_date = today.strftime("%d/%m/%Y")
            Enddate = today + timedelta(days=10)
            todays = date.today()
            finaldate = Enddate.date()
            diff = -(todays - finaldate).days
            progresses = 100
            if diff<0:
                progresses = 100
            else:
                for i in range(1,diff+1):
                    progresses = progresses - 10
            delivery_date = Enddate.strftime("%d/%m/%Y")
            #items of product
            if ids == ['']:
                messages.error(request, 'No any item in the Cart Please goto the Products and get Shopping')
                return render(request,'card/error.html')
            else:
                id = list(ids)
                arr = []
                for i in range(0,len(id),2):
                    for j in id[i].split(','):
                        arr.append(int(j))
                product = Product.objects.filter(id__in=[i for i in arr]).values()
                return render(request,"card/track.html",{"details":detail,"order_date":order_date,"delivery_date":delivery_date,"progesses":progresses,"status":status,"products":product})
        else:
            messages.error(request,"Please enter correct order id and mobile number")
        return render(request,"card/track.html")
    return render(request,"card/track.html")

def userprofile(request):
    user = request.user
    orderdetail = userorder.objects.filter(user=user)
    userprofile = User.objects.filter(username=user)
    if orderdetail.exists():
        return render(request,"card/profile.html",{"users":userprofile,"orderdetail":orderdetail})
    return render(request,"card/profile.html",{"users":userprofile})

def userfeedback(request):
    return render(request,"card/feedback.html")