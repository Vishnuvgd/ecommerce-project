import os
import uuid

from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *
# Create your views here.


def index(request):
    return render(request,'index.html')

#userlogin
def userlog(request):
    if request.method=='POST':
        a=ulogform(request.POST)
        if a.is_valid():
            em=a.cleaned_data['email']
            psw=a.cleaned_data['password']
            b=regmodel.objects.all()
            for i in b:
                id=i.id
                uname=i.name
                #global declaration(method 1)
                #request.session['username']=uname

                #(method 2)
                #global val
                #def val():
                    #return uname
                if em==i.email and psw==i.password:
                    return render(request,'userprofile.html',{'id':id,'uname':uname})
            else:
                 return redirect(loginfail)
    return render(request,'userlogin.html')

#loginfailed
def loginfail(request):
    return render(request,'loginfailed.html')

def register(request):
    if request.method=='POST':
        a=regform(request.POST)
        if a.is_valid():
            nm=a.cleaned_data['name']
            em=a.cleaned_data['email']
            pas=a.cleaned_data['password']
            b=regmodel(name=nm,email=em,password=pas)
            b.save()
            return redirect(userlog)
        else:
            return HttpResponse("failed..")
    return render(request,'register.html')

# ==================================================

#userauthentication
def userauth(request):
    if request.method=='POST':
        us=request.POST.get("username")
        em=request.POST.get("email")
        ps=request.POST.get("password")

        if User.objects.filter(username=us).first():
            #it will get first object from filter query
            messages.success(request,"user name already taken")
            #messages.success() it is function that is used send message from backend to front end
            return redirect(userauth)
        if User.objects.filter(email=em).first():
            messages.success(request,"email already taken")
            return redirect(userauth)

        user_obj=User(username=us,email=em)
        user_obj.set_password(ps)
        user_obj.save()
        auth_token=str(uuid.uuid4())
        #uuid(universaly unique identifiers),uuid4() create random UUID

        #new model
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        #user defined function
        send_mail_regis(em,auth_token)
        return render(request,'success.html')
    return render(request,'register.html')

def send_mail_regis(email,auth_token):
    subject="your account has be verified"
    message=f'paste the link to verify your account http://127.0.0.1:8000/verification/{auth_token}'
    #f--> string formater

    email_from=EMAIL_HOST_USER #from
    recipient=[email] #to
    send_mail(subject,message,email_from,recipient)

def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified: #if profile object is false
            messages.success(request,'your account has been verified')
            return redirect(login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request, 'your account has been verified')
        return redirect(login)
    else:
        messages.success(request,"user not found")
        return redirect(login)

def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_obj = User.objects.filter(email=email).first()
        # user_obj=shan
        if user_obj is None:
            messages.success(request, 'user not found')
            return HttpResponse("user not found")
        profile_obj = profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:  # if not profile is false
            messages.success(request, 'profile not verified check your mail')
            return HttpResponse("profile not verified")
        user = authenticate(email=email,password=password)
        # user=valid
        # if the given credentials are valid ,return User object.
        if user is None:

            messages.success(request, 'wrong password or username')
            return HttpResponse("password")
        return HttpResponse('success')
    return render(request, 'userlogin.html')

 # =============================================================

def shopreg(request):
    if request.method == 'POST':
        a=shopregform(request.POST)
        if a.is_valid():
            sm=a.cleaned_data['sname']
            em=a.cleaned_data['semail']
            psw=a.cleaned_data['spassword']
            b=shopregmodel(sname=sm,semail=em,spassword=psw)
            b.save()
            return redirect(spregdiplay)
        else:
            return HttpResponse("failed..")
    return render(request,'shopreg.html')


#edit
def editshopreg(request,id): #id=5
    a=shopregmodel.objects.get(id=id) #
    if request.method=='POST':
        a.sname=request.POST.get('sname')
        a.semail = request.POST.get('semail')
        a.spassword = request.POST.get('spassword')
        a.save()
        return redirect(profile)
    return render(request,'editshopreg.html',{'a':a})

#edit userreg
def editregister(request,id):
    a=regmodel.objects.get(id=id)
    if request.method == 'POST':
        a.name = request.POST.get('name')
        a.email = request.POST.get('email')
        a.password = request.POST.get('password')
        a.save()
        return redirect(userprofile)
    return render(request,'editregister.html',{'a': a})

#shoplogin
def shoplog(request):
    if request.method=='POST':
        a=shopform(request.POST)
        if a.is_valid():
            em=a.cleaned_data['email']
            psw=a.cleaned_data['password']
            b=shopregmodel.objects.all()
            for i in b:
                id=i.id
                user=i.sname
                if em==i.semail and psw==i.spassword:
                    return render(request,'profilepage.html',{'id':id,'user':user})
            else:
                 return redirect(loginfail)
    return render(request, 'shoplogin.html')


#fileupload
def itemupload(request):
    if request.method=='POST':
        a=uploadform(request.POST,request.FILES)
        if a.is_valid():
            nm=a.cleaned_data['name']
            im=a.cleaned_data['image']
            pr=a.cleaned_data['price']
            des=a.cleaned_data['description']
            b=uploadmodel(name=nm,image=im,price=pr,description=des)
            b.save()
            return redirect(uploaddiplay)
        else:
            return HttpResponse("upload failed..")
    return render(request,'itemupload.html')

#diplay
def uploaddiplay(request):
    a=uploadmodel.objects.all()
    id=[]
    im=[]
    nm=[]
    pr=[]
    dis=[]
    for i in a:
        z=i.image
        im.append(str(z).split('/')[-1])
        v=i.name
        nm.append(v)
        e=i.id
        id.append(e)
        r=i.price
        pr.append(r)
        x=i.description
        dis.append(x)
    mylist=zip(id,im,nm,pr,dis)
    return render(request,'productdiplay.html',{'mylist':mylist})

#userproductview
def userview(request):
    a=uploadmodel.objects.all()
    id=[]
    im=[]
    nm=[]
    pr=[]
    dis=[]
    for i in a:
        z=i.image
        im.append(str(z).split('/')[-1])
        v=i.name
        nm.append(v)
        e=i.id
        id.append(e)
        r=i.price
        pr.append(r)
        x=i.description
        dis.append(x)
    mylist=zip(id,im,nm,pr,dis)
    return render(request,'userproductview.html',{'mylist':mylist})


def spregdiplay(request):
    a=shopregmodel.objects.all()
    return render(request, 'shopregdisplay.html', {'a': a})

#profile
def profile(request):
    return render(request,'profilepage.html')

def userprofile(request):
    return render(request,'userprofile.html')


#card delete

def productdel(request,id):
    a=uploadmodel.objects.get(id=id)
    # if len(a.iimg)>0:
    #    os.remove(a.iimg.path)
    a.delete()
    return redirect(uploaddiplay)

#product edit
def productedit(request,id):
    a=uploadmodel.objects.get(id=id)
    im = str(a.image).split ('/')[-1]
    if request.method == 'POST':
        if len(request.FILES) > 0:  # check new file
            if len(a.image) > 0:  # check old file
                os.remove(a.image.path)
            a.image= request.FILES['image']
        a.name = request.POST.get('name')
        a.price=request.POST.get('price')
        a.description=request.POST.get('description')
        a.save()
        return redirect(uploaddiplay)
    return render(request,'productedit.html',{'a': a,'im': im})

#add to cart
def addcart(request,id):
    a=uploadmodel.objects.get(id=id)
    b=addcartmodel(cartimage=a.image,cartname=a.name, cartprice=a.price, cartdescription=a.description)
    b.save()
    return redirect(cartdisplay)


def cartdisplay(request):
    id=[]
    nm=[]
    img=[]
    pr=[]
    des=[]
    a=addcartmodel.objects.all()
    for i in a:
        x=i.id
        id.append(x)

        y=i.cartname
        nm.append(y)

        z=i.cartimage
        img.append(str(z).split ('/')[-1])

        p=i.cartprice
        pr.append(p)

        d=i.cartdescription
        des.append(d)
    mylist=zip(id,nm,img,pr,des)
    return render(request,'cartdisplay.html',{'mylist':mylist})

#item remove
def itemremove(request,id):
    a=addcartmodel.objects.get(id=id)
    # if len(a.cartiimg) > 0:
    #     os.remove(a.cartiimg.path)
    a.delete()
    return redirect(cartdisplay)

#productbuy
def itembuy(request,id):
    a = addcartmodel.objects.get(id=id)
    if request.method == 'POST':
        # a.iname = request.POST.get ('iname')
        # a.iprice = request.POST.get ('iprice')
        # a.save()
        item_name=request.POST.get('name')
        item_price =request.POST.get('price')
        item_quantity=request.POST.get('qun')
        total=int(item_price)*int(item_quantity)
        return render(request,'productBill.html',{'itemname':item_name,'ip':item_price,'iq':item_quantity,'t':total})
    return render(request,'productbuy.html',{'a': a})

def Address(request):
    return render(request,'Address.html')