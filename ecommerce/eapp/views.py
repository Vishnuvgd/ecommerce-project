import os
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
                 return HttpResponse("login failed")
    return render(request,'userlogin.html')

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
                 return HttpResponse("login failed")
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
    a = addcartmodel.objects.get (id=id)
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
