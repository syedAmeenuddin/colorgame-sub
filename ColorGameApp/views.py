from django.shortcuts import redirect, render
from .models import lotteryimages, user, bankDetails, upiDetails, gameDetails, group, results, wallet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime
from django.conf import settings as config
import razorpay
import pytz

from .scheduler import countdown, period, GameTime, ResultTime

client = razorpay.Client(auth=(config.API_KEY, config._SECRET_KEY))

def register(request):
    if request.method == "POST":
        
        try:
            _userid = request.session.get('userid')
            userid = request.POST['mobilenumber']
            request.session['userid'] = userid
        except:
            pass
        try:
            password = request.POST['password']
            if len(_userid)==10 and len(password)>=8:
                try:
                    registeruser = User.objects.create_user(_userid,None,password)
                    registeruser.save()
                    messages.success(request,'successfully registered')
                    # moving auth User to user model
                    authUser = User.objects.get(username=_userid)
                    moveusertomodeluser = user(username = authUser)
                    moveusertomodeluser.save()
                    
                    # end
                    return redirect('signin')
                except:
                    messages.success(request,'entered mobile number is already registered !')
                    return redirect('register')
            else:
                messages.success(request,'enter mobileNumber with 10 digit | password should be above 8 char')
                return redirect('register')
        except:
            try:
                if len(userid)==10:
                    userid = request.POST['mobilenumber']
                    User.objects.get(username =userid )
                    #already an user
                    messages.success(request,'entered mobile number is already exists!!. try new number')
                    #0 = false
                    return render(request, 'lib/register.html',{'otpsign':0})
                else:
                    messages.success(request,'mobileNumber should have 10 digit')
                    return redirect('register')
            except:
                #new user
                # 1 = true
                messages.success(request,'OTP has Sent')
                return render(request, 'lib/register.html',{'mobilenumber':userid,'otpsign':1})

        
     
    return render(request, 'lib/register.html')



def signin(request):
    if request.method == "POST":
        userid = request.POST['mobilenumber']
        password = request.POST['password'] 
        if len(userid)==10 and len(password)>=8:
            try:
                User.objects.get(username =userid )
                user = authenticate(username=userid, password=password)
                if user is not None:
                    login(request,user)
                    isloged = True
                    request.session['userid'] = userid
                    request.session['isloged'] = isloged
                    return redirect('win')
                else:
                    messages.success(request,'entered password is incorrect !')
                    return render(request, 'lib/signin.html',{'mobilenumber':userid})
            except:
                messages.success(request,'entered mobile number is not exist! please register or check ur number again')
                return redirect('signin')
        else:
            messages.success(request,'mobile number 10 digits and password more than 8 characters should be entered')
            return redirect('signin')

    return render(request, 'lib/signin.html')



def forgotpassword(request):
    if request.method == "POST":
        
        try:
            _userid = request.session.get('userid')
            userid = request.POST['mobilenumber']
            request.session['userid'] = userid
        except:
            pass
        try:
            newpassword = request.POST['password']
            if len(_userid)==10 and len(newpassword)>=8:
                try:
                    changepass = User.objects.get(username=_userid)
                    changepass.set_password(newpassword)
                    changepass.save()
                    messages.success(request,'password updated successfully')
                    # end
                    return redirect('signin')
                except:
                    messages.success(request,'Something went wrong try again!!')
                    return redirect('forgotpassword')
            else:
                messages.success(request,'enter mobileNumber with 10 digit | password should be above 8 char')
                return redirect('forgotpassword')
        except:
            try:
                if len(userid)==10:
                    userid = request.POST['mobilenumber']
                    User.objects.get(username =userid )
                    #already an user
                    messages.success(request,'OTP has sent')
                    #1 = true
                    return render(request, 'lib/forgotpassword.html',{'mobilenumber':userid,'otpsign':1})
                else:
                    messages.success(request,'mobileNumber should have 10 digit')
                    return redirect('forgotpassword')
            except:
                #new user
                # 1 = false
                messages.success(request,'please enter register mobile number')
                return render(request, 'lib/forgotpassword.html',{'otpsign':0})

    return render(request, 'lib/forgotpassword.html')



def win(request):
    isloged = request.session.get('isloged',False)
    currentuser = request.user
    if isloged:
        Intz = pytz.timezone('Asia/Kolkata')
        now = datetime.now(Intz)
        nowTime = now.strftime('%I:%M:%S %p')
        nowDate = now.strftime('%d-%m-%Y')
        fullDate = now.strftime('%d/%m/%Y %I:%M:%S %p')
        authUser = user.objects.get(username=currentuser)
        # userWallet = wallet.objects.get(user = currentuser)
        # print(userWallet.walletBalance)
        if request.method == "POST":   
            joingroup = request.POST['joingroup']
            joinnumber = request.POST['joinnumber']
            contractmoney = request.POST['contractmoney']
            contractcount = request.POST['contractcount']
            totalcontractmoney = request.POST['totalcontractmoney']
            # wallet = authUser.walletBalance
            joingroup = group.objects.get(groupName=joingroup)
            # if authUser.walletBalance ==None:
            #     wallet = 0          
            if int(totalcontractmoney)<=int(wallet) and countdown():
                try:
                    creatgamedetails = gameDetails(
                    user = authUser, 
                    period = period(),
                    date = fullDate,
                    time = nowTime,
                    group = joingroup,
                    number = int(joinnumber),
                    contractMoney = int(contractmoney),
                    tickets = contractcount,
                    totalcontractMoney = int(totalcontractmoney),
                    )

                    creatgamedetails.save()
                    authUser.walletBalance=int(authUser.walletBalance)-int(totalcontractmoney)
                    authUser.save()
                    sucessbetmessage = 'Successfully bet on number:'+' '+joinnumber
                    messages.success(request,sucessbetmessage)
                    return redirect('win')
                except:
                    messages.success(request,'something went wrong! please try again')
                    return redirect('win')
            else:
                return redirect('win')
        rA = results.objects.filter(group='1',date = nowDate)
        rB = results.objects.filter(group='2',date = nowDate)
        rC = results.objects.filter(group='3',date = nowDate)
        rD = results.objects.filter(group='4',date = nowDate)
        tabAwinner = 0
        tabBwinner = 0
        tabCwinner = 0
        tabDwinner = 0
        listA  = rA[::-1]    
        listB  = rB[::-1]
        listC  = rC[::-1]
        listD  = rD[::-1]
        counta=0
        countb=0
        countc=0
        countd=0
        for i in listA:
            if counta==0:
                counta+=1
                tabAwinner = i.result
        for i in listB:
            if countb==0:
                countb+=1
                tabBwinner = i.result
        for i in listC:
            if countc==0:
                countc+=1
                tabCwinner = i.result
        for i in listD:
            if countd==0:
                countd+=1
                tabDwinner = i.result
        groupname = group.objects.all()
        Lotteryimages = lotteryimages.objects.all()
        return render(request, 'lib/win.html',{'lotteryimages':Lotteryimages,'userid':currentuser
        ,'resultgroupA':rA
        ,'resultgroupB':rB
        ,'resultgroupC':rC
        ,'resultgroupD':rD
        ,'tabA':tabAwinner
        ,'tabB':tabBwinner
        ,'tabC':tabCwinner
        ,'tabD':tabDwinner
        ,'tab0name':groupname[0]
        ,'tab1name':groupname[1]
        ,'tab2name':groupname[2]
        ,'tab3name':groupname[3]
        # ,'wallet':0 if authUser.walletBalance==None else authUser.walletBalance
        ,'GameTime':GameTime
        ,'ResultTime':ResultTime
        })
    else:
        messages.success(request,'First Login to access game !')
        return redirect('signin')
    
    
    
    
def bankcard(request):
    isloged = request.session.get('isloged',False)
    currentuser = request.user
    if isloged:
        authUser = user.objects.get(username=currentuser)
        if request.method == "POST":
            _ifsc = request.POST['ifsc']
            _actnum = request.POST['accountnumber']
            _recipientname = request.POST['recipientname']
            _upi = request.POST['upi']    
            if(_ifsc != '' and _actnum != '' and _recipientname !='' and _upi !=''):
                
                createbankdetails = bankDetails(user=authUser,ifsc=_ifsc,accountNumber=_actnum,recipientName=_recipientname)
                createupi = upiDetails(user = authUser,upi=_upi)
                createbankdetails.save()
                createupi.save()
                messages.success(request,'saved successfully')
                return redirect('bankcard')
            else:
                messages.success(request,'enter all field correctly')
                return redirect('bankcard')
        getbankdetails  = bankDetails.objects.filter(user =authUser )
        getupidetails = upiDetails.objects.filter(user = authUser )
        return render(request, 'lib/manage_bankcard.html'
                      ,{
                        # 'wallet':0 if authUser.walletBalance==None else authUser.walletBalance,
                        'bank':getbankdetails
                        ,'upi':getupidetails
                        ,'addbank':True if len(getbankdetails)==0 else False
                        })
    else:
        messages.success(request,'First Login to access game !')
        return redirect('signin')
    
    
    
    
def mybet(request):
    isloged = request.session.get('isloged',False)
    if isloged:
        # try:
        authUser = user.objects.get(username=request.user)
        _gd = gameDetails.objects.filter(user = authUser)
        return render(request, 'lib/mybet.html'
                       ,{'playedgame':_gd
                       ,'GameTime':GameTime
                       ,'ResultTime':ResultTime
                    #    ,'wallet': 0 if authUser.walletBalance==None else authUser.walletBalance
                        })
        # except:
        #     return render(request, 'lib/mybet.html')
    else:
        messages.success(request,'First Login to access game !')
        return redirect('signin')
    
    
    
def recharge(request):
    isloged = request.session.get('isloged',False)
    if isloged:
        authUser = user.objects.get(username=request.user)
        if request.method == "POST":   
            amount = request.POST['amount']
            DATA = {
                "amount": amount,
                "currency": "INR",
                "receipt": "receipt#1",
            }
            payment = client.order.create(data=DATA)
            order_id = payment["id"]
            print(order_id)
            return render(request, 'lib/recharge.html',{
                # 'wallet': 0 if authUser.walletBalance==None else authUser.walletBalance,
                "amount":amount,
                "api_key":config.API_KEY,
                "order_id":order_id
                })
        else:
            return render(request, 'lib/recharge.html')
    else:
        messages.success(request,'First Login to access game !')
        return redirect('signin')
    
    
def rechargeMoney(request):
    if request.method == "POST":   
        amount = request.POST['amount']
        client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))
        DATA = {
            "amount": amount,
            "currency": "INR",
            "receipt": "receipt#1",
        }
        client.order.create(data=DATA)
    pass
    
    
def withdraw(request):
    isloged = request.session.get('isloged',False)
    if isloged:
        authUser = user.objects.get(username=request.user)
        return render(request, 'lib/withdraw.html',{'wallet': 0 if authUser.walletBalance==None else authUser.walletBalance})
    else:
        messages.success(request,'First Login to access game !')
        return redirect('signin')
        