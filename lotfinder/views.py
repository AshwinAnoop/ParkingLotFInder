from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from .models import booking, extendeduser, lotverification,parkinglot,locality,wallet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.

def home(request):
        if request.method=='POST':
            place = request.POST['place']
            lotobjs = parkinglot.objects.filter(locality = place,verifystatus = True,bookedstatus = False).order_by('-id')
            localities = locality.objects.all()
            return render(request,'home.html',{'lotobjs' : lotobjs, 'localities' : localities})

        else:
            lotobjs = parkinglot.objects.filter(verifystatus = True,bookedstatus = False).order_by('-id')
            localities = locality.objects.all()
            return render(request,'home.html',{'lotobjs' : lotobjs, 'localities' : localities})

def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            userid = user.id
            walletbalance = extendeduser.objects.values_list('walletbalance', flat=True).get(user_id = userid)
            request.session["walletbalance"] = walletbalance
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
            lotobjs = parkinglot.objects.filter(locality = place,monthlyrent=True,bookedstatus = False).order_by('-id')
            localities = locality.objects.all()
            return render(request,'monthlyhome.html',{'lotobjs' : lotobjs, 'localities' : localities})
        else:
            lotobjs = parkinglot.objects.filter(monthlyrent=True,bookedstatus = False).order_by('-id')
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
            return redirect('myspacehome<a class="dropdown-item" href="">Wallet Rs </a>')

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
    commitobj = lotverification.objects.filter(lotid=lot_id,allotedstatus=True).first()
    return render(request,'acceptrequest.html',{'lotobjs' : lotobjs, 'usermobobj' : usermobobj, 'commitobj' : commitobj})

def commiting(request):
    lotid = request.GET.get('parking')
    verifier = request.user.id
    commit = lotverification(allotedstatus=True,lotid_id=lotid,verifier_id=verifier)
    commit.save();
    messages.info(request,'You can now verify the alloted slot')
    return redirect('employeehome')

@login_required
def verification(request):
    userid = request.user.id
    lotverifyobj = lotverification.objects.filter(allotedstatus=True,verifier_id=userid)
    
    return render(request,'verification.html',{'lotverifyobj' : lotverifyobj})

def unallot(request):
    verifyid = request.GET.get('parking')
    allotedlot = lotverification.objects.get(id = verifyid)
    allotedlot.allotedstatus = False
    allotedlot.save();
    messages.info(request,'Slot Unallocation done successfully!!!')
    return redirect('verification')

def verifing(request):
    if request.method == 'POST':
        verifyid = request.POST['verifyid']
        adtitle = request.POST['title']
        parkinglotid = request.POST['parkinglotid']
        addescription = request.POST['description']
        adprice = request.POST['price']
        gmaplink = request.POST['gmaplink']
        verifyfeedback = request.POST['feedback']


        lotobj = parkinglot.objects.get(id = parkinglotid)
        lotobj.verifystatus = True
        lotobj.title = adtitle
        lotobj.description = addescription
        lotobj.price = adprice
        lotobj.gmaplink = gmaplink
        
        verifyobj = lotverification.objects.get(id = verifyid)
        verifyobj.feedback = verifyfeedback
        verifyobj.verifydate = datetime.datetime.now()

        lotobj.save();
        verifyobj.save();
        messages.info(request,'Slot verified successfully!!!')
        return redirect('verification')        


    else:
        verifyid = request.GET.get('verify')
        lotid = request.GET.get('lot')
        verifyobjs = lotverification.objects.get(id = verifyid)
        lotobjs = parkinglot.objects.get(id = lotid)
        return render(request,'verifing.html',{'verifyobjs' : verifyobjs, 'lotobjs' : lotobjs})


def verifiedbyme(request):
    userid = request.user.id
    lotverifyobj = lotverification.objects.filter(verifier_id=userid,lotid__verifystatus=True,allotedstatus=True)  
    return render(request,'verifiedbyme.html',{'lotverifyobj' : lotverifyobj})

def lotoverview(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            bookingtime = datetime.datetime.now()
            lotid = request.POST['lotid']
            userid = request.user.id

            bookingobj = booking(booktime=bookingtime,lotid_id=lotid,userid_id=userid)
            bookingobj.save();

            loteditobj = parkinglot.objects.get(id=lotid)
            loteditobj.bookedstatus = True
            loteditobj.save();
            messages.info(request,'Succesfully Booked')
            return redirect('/')           

        else:               
            parking = request.GET.get('lot')
            lotobjs = parkinglot.objects.get(id=parking)  
            return render(request,'lotoverview.html',{'lotobjs' : lotobjs})
    else:
        messages.info(request,'Please Login to Continue')
        return redirect('login') 

def walletfunc(request):
    userid = request.user.id
    walletobjs = wallet.objects.filter(userid_id=userid).order_by('-Transactdate')
    return render(request,'wallet.html',{'walletobjs' : walletobjs})

def addmoney(request):
    if request.method == 'POST':
        amountvar = request.POST['cash']
        userid = request.user.id
        currbalance = request.session["walletbalance"]
        newbalance = int(currbalance) + int(amountvar)

        editbalance = extendeduser.objects.get(user=userid) 
        editbalance.walletbalance = newbalance
        editbalance.save();
        addobj = wallet(amount=amountvar,userid_id=userid)
        addobj.save();
        request.session["walletbalance"]=newbalance

        messages.info(request,'Deposit successful')
        return redirect('wallet')   

    else:
        return render(request,'addmoney.html')

def withdraw(request):
    if request.method == 'POST':
        amountvar = request.POST['cash']
        userid = request.user.id
        currbalance = request.session["walletbalance"]
        newbalance = int(currbalance) - int(amountvar)
        negamount = 0 - int(amountvar)

        editbalance = extendeduser.objects.get(user=userid) 
        editbalance.walletbalance = newbalance
        editbalance.save();
        addobj = wallet(amount=negamount,userid_id=userid)
        addobj.save();
        request.session["walletbalance"]=newbalance

        messages.info(request,'Withdrawl successful')
        return redirect('wallet')   

    else:
        return render(request,'withdraw.html')

def bookings(request):
    if request.method == 'POST':
        userid = request.user.id
        bookingid = request.POST['bookingid']
        priceperhour = request.POST['priceperhour']
        parkingid = request.POST['parkingid']
        vacatetime = datetime.datetime.now()
        editbooking = booking.objects.get(id=bookingid)
        starttime = editbooking.booktime
        starttime = starttime.replace(tzinfo=None)
        totaltime = vacatetime - starttime
        totalhour = totaltime.seconds/3600

        if totalhour < 2:
            totalcost = int(priceperhour) * 2
        elif totalhour < 12:
            totalhour = int(totalhour) + 1
            totalcost = int(priceperhour) * int(totalhour)
        elif totalhour < 24:
            totalcost = int(priceperhour) * 12
        else:
            totalday = int(totalhour)/24
            totalday = totalday + 1
            costperday = int(priceperhour) * 12
            totalcost = totalday * costperday

        editbooking.vacate = vacatetime
        editbooking.payment = totalcost
        editbooking.paymentstatus = True
        editbooking.save();

        parkingobj = parkinglot.objects.get(id=parkingid)
        parkingobj.bookedstatus = False
        parkingobj.save();

        userobj = extendeduser.objects.get(user_id=userid)
        currbalance = userobj.walletbalance
        newbalance = currbalance - totalcost
        userobj.walletbalance = newbalance
        userobj.save();
        request.session["walletbalance"]=newbalance
        messages.info(request,'Slot freed Successfully!!!')
        return redirect('bookings') 

    else:   
        userid = request.user.id
        bookedobjs = booking.objects.filter(userid_id = userid).order_by('-id')
        return render(request,'bookings.html',{'bookedobjs' : bookedobjs})

def monthlyoverview(request):
    if request.method == 'POST':
        bookingtime = datetime.datetime.now()
        lotid = request.POST['lotid']
        payment = request.POST['pricesub']
        userid = request.user.id
        vacatetime = datetime.datetime.now()+datetime.timedelta(days=30)

        bookingobj = booking(booktime=bookingtime,vacate=vacatetime,lotid_id=lotid,userid_id=userid,payment=payment,paymentstatus=True,monthlysubscribe=True)
        bookingobj.save();

        loteditobj = parkinglot.objects.get(id=lotid)
        loteditobj.bookedstatus = True
        loteditobj.save();

        userobj = extendeduser.objects.get(user_id=userid)
        currbalance = userobj.walletbalance
        newbalance = int(currbalance) - int(payment)
        userobj.walletbalance = newbalance
        userobj.save();
        request.session["walletbalance"]=newbalance

        messages.info(request,'Monthly subscription sucessful')
        return redirect('/') 
    else:
        parking = request.GET.get('lot')
        lotobjs = parkinglot.objects.get(id=parking)  
        return render(request,'monthlyoverview.html',{'lotobjs' : lotobjs})