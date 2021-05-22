from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from .models import extendeduser, lotverification,parkinglot,locality
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        walletbalance = 0

        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('signup')

            else:
                user = User.objects.create_user(username=email,email=email,password=password1,first_name=username)
                newextendeduser = extendeduser(mobile=mobile, walletbalance=walletbalance, user=user)
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

        newlot = parkinglot(locality=place,title=title,description=description,monthlyrent=monthly,image=image,price=price,userid_id=userid)
        newlot.save();
        messages.info(request,'Listing successful')
        return render(request,'myspacehome.html')

    else:
        localities = locality.objects.all()
        return render(request,'addparking.html',{'localities' : localities})


def editlisting(request):
    if request.method == 'POST':

        if 'edit' in request.POST:
            lotid = request.POST['lotid']
            title = request.POST['title']
            description = request.POST['description']
            price = request.POST['price']
            if 'monthly' in request.POST:
                monthly = request.POST['monthly']
            else:
                monthly = False

            editlot = parkinglot.objects.get(id = lotid)
            editlot.title = title
            editlot.description = description
            editlot.monthlyrent = monthly
            editlot.price = price     
            editlot.save();
            messages.info(request,'Update successful')
            return redirect('myspacehome')

        elif 'deactivate' in request.POST:
            lotid = request.POST['lotid']
            deactivatelot = parkinglot.objects.get(id = lotid)
            deactivatelot.activestatus = False
            deactivatelot.save();
            messages.info(request,'Deactivated parking successfully')
            return redirect('myspacehome')

        elif 'activate' in request.POST:
            lotid = request.POST['lotid']
            activatelot = parkinglot.objects.get(id = lotid)
            activatelot.activestatus = True
            activatelot.save();
            messages.info(request,'Re-activated parking successfully')
            return redirect('myspacehome')

    else:
        id = request.GET.get('parking')
        lotobjs = parkinglot.objects.filter(id=id)
        return render(request,'editlisting.html',{'lotobjs' : lotobjs})


def employeelogin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:

                auth.login(request, user)
                return redirect("/employeehome")
            else:
                messages.info(request,'No Authorization to visit the page, Login Here')
                return redirect('login')  
        else:
            messages.info(request,'invalid credentials')
            return redirect('emp')
    else:

        return render(request,'employeelogin.html')

@login_required
def employeehome(request):
    if request.user.is_staff:

        lotobjs = parkinglot.objects.filter(verifystatus=False)
        return render(request,'employeehome.html',{'lotobjs' : lotobjs})
    else:
        return redirect('/')

@login_required
def acceptrequest(request):
    lot_id = request.GET.get('parking') 
    lotobjs = parkinglot.objects.get(id=lot_id)
    myuserid = lotobjs.userid_id
    usermobobj = extendeduser.objects.get(user=myuserid)
    commitobj = lotverification.objects.filter(lotid=lot_id).first()
    return render(request,'acceptrequest.html',{'lotobjs' : lotobjs, 'usermobobj' : usermobobj, 'commitobj' : commitobj})

def commiting(request):
    lotid = request.GET.get('parking')
    verifier = request.user.id
    commit = lotverification(allotedstatus=True,lotid_id=lotid,verifier_id=verifier)
    commit.save();
    return redirect('employeehome')

@login_required
def verification(request):
    userid = request.user.id
    lotverifyobj = lotverification.objects.filter(allotedstatus=True,verifier_id=userid)
    
    return render(request,'verification.html',{'lotverifyobj' : lotverifyobj})