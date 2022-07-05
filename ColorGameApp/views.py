from django.shortcuts import redirect, render
from .models import lotteryimages, user, bankDetails, upiDetails, gameDetails
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime
import pytz
def register(request):
    if request.method == "POST":
        userid = request.POST['mobilenumber']
        password = request.POST['password']
        if len(userid)==10 and len(password)>=8:
            try:
                registeruser = User.objects.create_user(userid,None,password)
                registeruser.save()
                messages.success(request,'successfully registered')
                # moving auth User to user model
                authUser = User.objects.get(username=userid)
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

    return render(request, 'lib/register.html')

def signin(request):
    if request.method == "POST":
        userid = request.POST['mobilenumber']
        password = request.POST['password'] 
        if len(userid)==10 and len(password)>=8:
            user = authenticate(username=userid, password=password)
            if user is not None:
                login(request,user)
                isloged = True
                request.session['userid'] = userid
                request.session['isloged'] = isloged
                return redirect('win')

            else:
                messages.success(request,'entered mobile number or password was incorrect !')
                return redirect('signin')
        
        else:
            messages.success(request,'entered mobile number and password ! to login')
            return redirect('signin')

    return render(request, 'lib/signin.html')
def forgotpassword(request):
    if request.method == "POST":
        userid = request.POST['mobilenumber']
        newpassword = request.POST['password'] 
        if len(userid)==10 and len(newpassword)>=8:
            try:
                changepass = User.objects.get(username=userid)
                changepass.set_password(newpassword)
                changepass.save()
                messages.success(request,'password updated successfully')
                return redirect('signin')
            except:
                messages.success(request,'enter registered moobile number!!! and change password')
                return redirect('forgotpassword')
        else:
            messages.success(request,'entered mobile number and new password ! to reset password')
            return redirect('forgotpassword')

    return render(request, 'lib/forgotpassword.html')
def win(request):
    isloged = request.session.get('isloged',False)
    currentuser = request.user
    print(currentuser)
    if isloged:
        Intz = pytz.timezone('Asia/Kolkata')
        now = datetime.now(Intz)
        nowTime = now.strftime('%I:%M:%S %p')
        nowDate = now.strftime('%Y-%m-%d')
        fullDate = now.strftime('%d/%m/%Y %I:%M:%S %p')
        authUser = user.objects.get(username=currentuser)
        if request.method == "POST":   
            joingroup = request.POST['joingroup']
            joinnumber = request.POST['joinnumber']
            contractmoney = request.POST['contractmoney']
            contractcount = request.POST['contractcount']
            totalcontractmoney = request.POST['totalcontractmoney']
            hour= now.hour
            tmin = now.minute
            hor = int(hour) * 60
            _ur =  int(hor) + int(tmin)
            game = int(_ur)/15
            game = int(game+1)
            nowPeriod=str(game)
            print(len(nowPeriod))
            if(len(nowPeriod)==1):
                nowPeriod='00'+nowPeriod
            if(len(nowPeriod)==2):
                nowPeriod='0'+nowPeriod
            gamePeriod = nowDate+nowPeriod
            gamePeriod = gamePeriod.replace('-', '')
            wallet = authUser.walletBalance
            if authUser.walletBalance ==None:
                wallet = 0                
            if int(totalcontractmoney)<=int(wallet):
                try:
                    creatgamedetails = gameDetails(
                    user = authUser, 
                    period = gamePeriod,
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
                    return redirect('win')
                except:
                    messages.success(request,'something went wrong! please try again')
                    return redirect('win')
            else:
                return redirect('win')
            
        _gdA = gameDetails.objects.filter(user = authUser,group='A')
        _gdB = gameDetails.objects.filter(user = authUser,group='B')
        _gdC = gameDetails.objects.filter(user = authUser,group='C')
        _gdD = gameDetails.objects.filter(user = authUser,group='D')
        
        Lotteryimages = lotteryimages.objects.all()
        return render(request, 'lib/win.html',{'lotteryimages':Lotteryimages,'userid':currentuser
        ,'playedgameA':_gdA
        ,'playedgameB':_gdB
        ,'playedgameC':_gdC
        ,'playedgameD':_gdD
        ,'wallet':0 if authUser.walletBalance==None else authUser.walletBalance
        })
    else:
        messages.success(request,'First Login to access game !')
        return redirect('signin')
def bankcard(request):
    isloged = request.session.get('isloged',False)
    if isloged:
        authUser = user.objects.get(username=request.user)
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
                print('null')
        
        return render(request, 'lib/manage_bankcard.html',{'wallet':0 if authUser.walletBalance==None else authUser.walletBalance})
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
                       ,'wallet': 0 if authUser.walletBalance==None else authUser.walletBalance})
        # except:
        #     return render(request, 'lib/mybet.html')
    else:
        messages.success(request,'First Login to access game !')
        return redirect('signin')