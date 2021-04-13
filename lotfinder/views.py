from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from .models import extendeduser,parkinglot,locality
from django.contrib import messages
# Create your views here.

def home(request):
        if request.method=='POST':
            place = request.POST['place']
            lotobjs = parkinglot.objects.filter(locality = place)
            localities = locality.objects.all()
            return render(request,'home.html',{'lotobjs' : lotobjs, 'localities' : localities})

        else:
            lotobjs = parkinglot.objects.all()
            localities = locality.objects.all()
            return render(request,'home.html',{'lotobjs' : lotobjs, 'localities' : localities})

def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')


    else:
        return render(request,'login.html')

    

def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['phno']
        password1 = request.POST['password']
        password2 = request.POST['retypepassword']

        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('signup')

            else:
                user = User.objects.create_user(username=email,email=email,password=password1,first_name=username)
                newextendeduser = extendeduser(mobile=mobile, user=user)
                newextendeduser.save();
                print('user created')
                return redirect('login')                
        else:
            messages.info(request,'Passwords not matching')
            return redirect('signup')

        return redirect('/')
        
    else:
        return render(request,'signup.html')

def monthlyhome(request):

        if request.method=='POST':
            place = request.POST['place']
            lotobjs = parkinglot.objects.filter(locality = place,monthlyrent=True)
            localities = locality.objects.all()
            return render(request,'monthlyhome.html',{'lotobjs' : lotobjs, 'localities' : localities})
        else:
            lotobjs = parkinglot.objects.filter(monthlyrent=True)
            localities = locality.objects.all()
            return render(request,'monthlyhome.html',{'lotobjs' : lotobjs, 'localities' : localities})


def logout(request):
    auth.logout(request)
    return redirect('/')

def myspacehome(request):
    userid = request.user.id
    lotobjs = parkinglot.objects.filter(userid=userid)
    return render(request,'myspacehome.html',{'lotobjs' : lotobjs})

def addparking(request):

    if request.method == 'POST':
        place = request.POST['locality']
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        if 'monthly' in request.POST:
            monthly = request.POST['monthly']
        else:
            monthly = False
        image = request.FILES['image']
        userid = request.user.id

        newlot = parkinglot(locality=place,title=title,description=description,monthlyrent=monthly,image=image,price=price,userid=userid)
        newlot.save();
        messages.info(request,'Listing successful')
        return render(request,'myspacehome.html')

    else:
        localities = locality.objects.all()
        return render(request,'addparking.html',{'localities' : localities})