from datetime import datetime
import random
from apscheduler.schedulers.background import BackgroundScheduler
from .models import lotteryimages, user, bankDetails, upiDetails, gameDetails, group, results
from django.contrib.auth.models import User
import pytz

def countdown():
    Intz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(Intz)
    m = now.strftime('%M')
    s = now.strftime('%S')
    m = 14-(int(m)%15)
    s = 60-int(s)
    if (int(s)<10):
        s = '0'+str(s)
    if int(m) <1:
        return False
    else:
        return True
def pri():
    contract_money=[12,120]
    ticket=[1,2,3]
    number = random.randint(0,9)
    _group = random.randint(1,4)
    ficontractmoney = random.choice(contract_money)
    fiticket = random.choice(ticket)
    ficontractamt = int(fiticket)*int(ficontractmoney)
    joingroup = group.objects.get(groupId=_group)
    gUser = User.objects.get(username='1111111111')
    authUser = user.objects.get(username = gUser)
    Intz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(Intz)
    nowTime = now.strftime('%I:%M:%S %p')
    nowDate = now.strftime('%Y-%m-%d')
    fullDate = now.strftime('%d/%m/%Y %I:%M:%S %p')
    hour= now.hour
    tmin = now.minute
    hor = int(hour) * 60
    _ur =  int(hor) + int(tmin)
    game = int(_ur)/3
    game = int(game+1)
    nowPeriod=str(game)
    if(len(nowPeriod)==1):
        nowPeriod='00'+nowPeriod
    if(len(nowPeriod)==2):
        nowPeriod='0'+nowPeriod
    perioddate = nowDate.replace('-','')
    nowPeriod = perioddate+nowPeriod
    try:
        
        if countdown():
            createGD = gameDetails(
                user = authUser, 
                period = nowPeriod,
                date = fullDate,
                time = nowTime,
                group = joingroup,
                number = number,
                contractMoney = ficontractmoney,
                tickets = fiticket,
                totalcontractMoney = ficontractamt,
                )
            createGD.save()
            print('game created')
        else:
            print('game Stoped! calculating Result')
    except:
        print('went wrong')
    
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(pri,'interval',seconds = 15)
    scheduler.start()
