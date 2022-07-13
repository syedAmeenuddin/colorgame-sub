from xml.dom.minidom import parseString
from django.shortcuts import redirect, render
from .models import lotteryimages, user, bankDetails, upiDetails, gameDetails, group, results, wallet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime
from django.conf import settings as config
# import razorpay
import pytz
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Import Payu from Paywix
from paywix.payu import Payu
payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

# Create Payu Object for making transaction
# The given arguments are mandatory
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)

from .scheduler import countdown, period, GameTime, ResultTime

# client = razorpay.Client(auth=(config.API_KEY, config._SECRET_KEY))

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
                    adduserwallet = wallet(
                        user=moveusertomodeluser
                        ,walletBalance=0
                    )
                    adduserwallet.save()
                    
                    # end
                    return render(request, 'lib/signin.html',{"apptype":"android"})
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
                messages.success(request,'OTP has initiated')
                return render(request, 'lib/register.html',{'mobilenumber':userid,'otpsign':1})

        
     
    return render(request, 'lib/register.html')



def signin(request):
    apptype = request.GET.get('apptype','')

    if request.method == "POST":
        userid = request.POST['mobilenumber']
        password = request.POST['password'] 
        if len(userid)==10 and len(password)>=8:
            try:
                User.objects.get(username =userid)
                user = authenticate(username=userid, password=password)
                if user is not None:
                    login(request,user)
                    isloged = True
                    request.session['userid'] = userid
                    request.session['isloged'] = isloged
                    return redirect('win')
                else:
                    messages.success(request,'entered password is incorrect !')
                    return render(request, 'lib/signin.html',{"apptype":apptype,'mobilenumber':userid})
            except:
                messages.success(request,'entered mobile number is not exist! please register or check ur number again')
                return render(request, 'lib/signin.html',{"apptype":apptype})
        else:
            messages.success(request,'mobile number 10 digits and password more than 8 characters should be entered')
            return render(request, 'lib/signin.html',{"apptype":apptype})
    else:
        
        if apptype.lower() == 'android':
            return render(request, 'lib/signin.html',{"apptype":apptype})
        else:
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
                    return render(request, 'lib/signin.html',{"apptype":"android"})
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
                    messages.success(request,'OTP has initiated')
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
    if isloged:
        try:
            Intz = pytz.timezone('Asia/Kolkata')
            now = datetime.now(Intz)
            nowTime = now.strftime('%I:%M:%S %p')
            nowDate = now.strftime('%d-%m-%Y')
            fullDate = now.strftime('%d/%m/%Y %I:%M:%S %p')
            authUser = user.objects.get(username=request.user)
            userWallet = wallet.objects.get(user = authUser)
            if request.method == "POST":   
                joingroup = request.POST['joingroup']
                joinnumber = request.POST['joinnumber']
                contractmoney = request.POST['contractmoney']
                contractcount = request.POST['contractcount']
                totalcontractmoney = request.POST['totalcontractmoney']
                joingroup = group.objects.get(groupName=joingroup)
                if int(totalcontractmoney)<=int(userWallet.walletBalance) and countdown():
                    try:
                        if(authUser != None):
                            gameDetails.objects.create( 
                                user = authUser, 
                                period = period(),
                                date = fullDate,
                                time = nowTime,
                                group = joingroup,
                                number = int(joinnumber),
                                contractMoney = int(contractmoney),
                                tickets = contractcount,
                                totalcontractMoney = int(totalcontractmoney))
                        else:
                            messages.success(request,'Session Expired')
                            return render(request, 'lib/signin.html',{"apptype":"android"})
                    except Exception as e:
                        print(request,e)
                        messages.success(request,e)
                        return redirect('win')

                    userWallet.walletBalance=int(userWallet.walletBalance)-int(totalcontractmoney)
                    userWallet.save()
                    sucessbetmessage = 'Successfully bet on number:'+' '+joinnumber
                    messages.success(request,sucessbetmessage)
                    return redirect('win')   

                else:
                    messages.success(request,'Bet failed')
                    return redirect('win')
            try:
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
                return render(request
                , 'lib/win.html'
                ,{'lotteryimages':Lotteryimages,'userid':request.user
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
                ,'wallet':userWallet.walletBalance
                ,'GameTime':GameTime
                ,'ResultTime':ResultTime
                })
            except:
                tabAwinner = 0
                tabBwinner = 0
                tabCwinner = 0
                tabDwinner = 0
                groupname = group.objects.all()
                Lotteryimages = lotteryimages.objects.all()
                return render(request, 'lib/win.html',{'lotteryimages':Lotteryimages,'userid':request.user
                ,'tab0name':groupname[0]
                ,'tab1name':groupname[1]
                ,'tab2name':groupname[2]
                ,'tab3name':groupname[3]
                ,'wallet':userWallet.walletBalance
                ,'tabA':tabAwinner
                ,'tabB':tabBwinner
                ,'tabC':tabCwinner
                ,'tabD':tabDwinner
                ,'GameTime':GameTime
                ,'ResultTime':ResultTime
                })
        except Exception as e:
            messages.success(request,e)
            return render(request, 'lib/signin.html',{"apptype":"android"})    
    else:
        messages.success(request,'First Login to access game !')
        return render(request, 'lib/signin.html',{"apptype":"android"})
    
    
def bankcard(request):
    isloged = request.session.get('isloged',False)
    if isloged:
        try:
            authUser = user.objects.get(username=request.user)
            userWallet = wallet.objects.get(user = authUser)
            if request.method == "POST":
                try:
                    editbank = request.POST['editbank']
                    
                except:
                    try:
                        _upi = request.POST['upi']
                        if(_upi !=''):
                            try:
                                upiDetails.objects.create(user = authUser,upi=_upi)
                                messages.success(request,'saved successfully')
                                return redirect('bankcard')
                            except:
                                messages.success(request,'something went wrong while saving your information. try again')
                                return redirect('bankcard')
                        else:
                            messages.success(request,'enter Upi field correctly')
                            return redirect('bankcard')
                    except:
                        _ifsc = request.POST['ifsc']
                        _actnum = request.POST['accountnumber']
                        _recipientname = request.POST['recipientname']
                        if(_ifsc != '' and _actnum != '' and _recipientname !=''):
                            try:
                                bankDetails.objects.create(
                                user=authUser
                                ,ifsc=_ifsc 
                                ,accountNumber=_actnum
                                ,recipientName=_recipientname
                                )
                                messages.success(request,'saved successfully')
                                return redirect('bankcard')
                            except:
                                messages.success(request,'something went wrong while saving your information. try again')
                                return redirect('bankcard')
                        else:
                            messages.success(request,'enter all field correctly')
                            return redirect('bankcard')

                    ## # check for anyone things UPI or Bank Details both are NOT Mandatory 
                    ## # check and insert which is provided with null
                    # validate UPI with regex in client Side (search in internet to validate UPI ID)
                    # change the UI to fill anyone bank details or UPI or create a seprate page for both
            else:            
                try:
                    try:
                        getbankdetails  = bankDetails.objects.filter(user =authUser )
                        return render(request, 'lib/manage_bankcard.html',
                                {
                                    'wallet':userWallet.walletBalance
                                    ,'bank':getbankdetails
                                    ,'addbank':True if len(getbankdetails)==0 else False
                                    })
                    except:
                        getupidetails = upiDetails.objects.filter(user = authUser )
                        return render(request, 'lib/manage_bankcard.html',
                                {
                                    'wallet':userWallet.walletBalance
                                    ,'upi':getupidetails
                                    ,'addbank':True if len(getupidetails)==0 else False
                                    })
                except:
                    return render(request, 'lib/manage_bankcard.html',{'wallet':userWallet.walletBalance
                    ,'addbank':True
                    }) 
        except:
            messages.success(request,'something went wrong. please login!')
            return render(request, 'lib/signin.html',{"apptype":"android"})
    else:
        messages.success(request,'First Login to access game !')
        return render(request, 'lib/signin.html',{"apptype":"android"})
       
def mybet(request):
    isloged = request.session.get('isloged',False)
    if isloged:
        try:
            authUser = user.objects.get(username=request.user)
            userWallet = wallet.objects.get(user = authUser)
            try:
                _gd = gameDetails.objects.filter(user = user.objects.get(username=request.user)).order_by('-group_id').reverse()
                # _gd = gameDetails.objects.all().reverse()
                return render(request, 'lib/mybet.html'
                            ,{'playedgame':_gd
                            ,'GameTime':GameTime
                            ,'ResultTime':ResultTime
                            ,'wallet':userWallet.walletBalance
                                })
            except Exception as e:
                messages.success(request,e)
                return render(request, 'lib/mybet.html',{'wallet':userWallet.walletBalance})
        except:
            messages.success(request,'something went wrong. please login!')
            return render(request, 'lib/signin.html',{"apptype":"android"})
        
    else:
        messages.success(request,'First Login to access game !')
        return render(request, 'lib/signin.html',{"apptype":"android"})
    
    
    
# def recharge(request):
#     isloged = request.session.get('isloged',False)
#     if isloged:
#         authUser = user.objects.get(username=request.user)
#         userWallet = wallet.objects.get(user = user.objects.get(username=request.user))
#         if request.method == "POST": 
#             amount = request.POST['amount']  
#             if amount!='':
#                 DATA = {
#                     "amount": amount,
#                     "currency": "INR",
#                     "receipt": "receipt#1",
#                 }
#                 payment = client.order.create(data=DATA)
#                 order_id = payment["id"]
#                 return render(request, 'lib/recharge.html',{
#                     'wallet':userWallet.walletBalance
#                     ,"amount":amount,
#                     "api_key":config.API_KEY,
#                     "order_id":order_id
#                     })
#             else:
#                 messages.success(request,'enter amount to recharge!')
#                 return redirect('recharge')
    #     else:
    #         return render(request, 'lib/recharge.html',{'wallet':userWallet.walletBalance})
    # else:
    #     messages.success(request,'First Login to access game !')
    #     return render(request, 'lib/signin.html',{"apptype":"android"})
def recharge(request):
    isloged = request.session.get('isloged',False)
    if isloged:
        authUser = user.objects.get(username=request.user)
        userWallet = wallet.objects.get(user = user.objects.get(username=request.user))
        if request.method == "POST":
            amount = request.POST['amount']
            data = {
            'amount': amount, 
            'firstname': 'ColorGame',
            'email': 'ColorGame@gmail.com',
            'phone': request.user,
            'productinfo': 'ColorGame', 
            'lastname': 'ColorGame',
            'address1': 'ColorGame',
            'address2': 'ColorGame',
            'city': 'ColorGame',  
            'state': 'ColorGame', 
            'country': 'ColorGame',
            'zipcode': 'ColorGame', 
            'udf1': '', 
            'udf2': '', 
            'udf3': '', 
            'udf4': '', 
            'udf5': ''        
            } 
            # need to generate and add tanx id as date time now (eg:20220712093056)
            # need to create method for widthraw money (payout with payu gateway)
            # need to razor recharge and withdraw method 
            # in Scheduler page need to implement this Logic --> after updating the result in gamedetails filter the gamedetails with current result 
            # and get the user who has won add x10 (10 is configurable) to the total contract amount eg (12 x 10) 120 plus in wallet 
            # and add withdraw with minum amount to withdraw logic (configurable) eg(user should have min 1000 rupees to withdraw in wallet) 
            # and initiate the trigger withdraw with payu and razor (for backup) 
            data.update({"txnid": "20220712093056"})
            payu_data = payu.transaction(**data)
            return render(request, 'lib/payment_processing.html',{"posted":payu_data})
        else:
            return render(request, 'lib/recharge.html',{'wallet':userWallet.walletBalance})

    else:
        messages.success(request,'First Login to access game !')
        return render(request, 'lib/signin.html',{"apptype":"android"})
@csrf_exempt
def recharge_success(request):
    # allow only post method else redirect to win page 
    # 20220712093056 cross check the tranx id and redirect to success html page with recharged amount 
    # and add the rechargesd amount in the user wallet
    # else if transx id didnt match redirect to win page 

    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return JsonResponse(response)
@csrf_exempt
def recharge_failure(request):

    # allow only post method else redirect to win page 
    # 20220712093056 cross check the tranx id and redirect to failed html page with tried to recharge amount 
    # else if transx id didnt match redirect to win page 

    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return JsonResponse(response)




# implement a dummy method to keep the session trigger method using ajax in win 
 
# design a new ecommerce page for payu and razor pay bank verfication 
# with dummy logic and pay button.

# please checkout all the comment in this and scheduler py page and method s































def withdraw(request):
    isloged = request.session.get('isloged',False)
    if isloged:
        authUser = user.objects.get(username=request.user)
        userWallet = wallet.objects.get(user = authUser)
        if request.method =="POST":
            amount = request.POST['amount']
            if amount!='':
                if int(amount) > int(userWallet.walletBalance):
                    messages.success(request,'enter valid wallet amount to withdraw !')
                    return redirect('withdraw')
                else:
                    userWallet.walletBalance=int(userWallet.walletBalance)-int(amount)
                    userWallet.save()
                    messages.success(request,'Amount has *withdrew successfully*')
                    return redirect('withdraw')
            else:
                messages.success(request,'enter amount to withdraw!')
                return redirect('withdraw')
        return render(request, 'lib/withdraw.html',{
            'wallet':userWallet.walletBalance
            })
    else:
        messages.success(request,'First Login to access game !')
        return render(request, 'lib/signin.html',{"apptype":"android"})












# def rechargeMoney(request):
#     if request.method == "POST":   
#         amount = request.POST['amount']
#         client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))
#         DATA = {
#             "amount": amount,
#             "currency": "INR",
#             "receipt": "receipt#1",
#         }
#         client.order.create(data=DATA)
#     pass
    
  