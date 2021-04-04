from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from .models import extendeduser,parkinglot
from django.contrib import messages
# Create your views here.

def home(request):
    lotobjs = parkinglot.objects.all()
    return render(request,'home.html',{'lotobjs' : lotobjs})

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
    lotobjs = parkinglot.objects.all()
    return render(request,'monthlyhome.html',{'lotobjs' : lotobjs})


def logout(request):
    auth.logout(request)
    return redirect('/')

def myspacehome(request):
    return render(request,'myspacehome.html')

def addparking(request):
    return render(request,'addparking.html')