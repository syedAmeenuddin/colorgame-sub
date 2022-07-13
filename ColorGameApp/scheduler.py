from datetime import datetime, timedelta
import random
from django.conf import settings as config

from apscheduler.schedulers.background import BackgroundScheduler
from .models import lotteryimages, user, bankDetails, upiDetails, gameDetails, group, results
from django.contrib.auth.models import User

import pytz
GameTime = config.GAMETIME
ResultTime = config.RESULTTIME
def period():
    Intz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(Intz)
    nowDate = now.strftime('%Y-%m-%d')
    hour= now.hour
    tmin = now.minute
    hor = int(hour) * 60
    _ur =  int(hor) + int(tmin)
    game = int(_ur)/int(GameTime)
    game = int(game+1)
    nowPeriod=str(game)
    if(len(nowPeriod)==1):
        nowPeriod='00'+nowPeriod
    if(len(nowPeriod)==2):
        nowPeriod='0'+nowPeriod
    perioddate = nowDate.replace('-','')
    nowPeriod = perioddate+nowPeriod
    return nowPeriod
def countdown():
    print("function Count down triggered")
    Intz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(Intz)
    m = now.minute
    s = now.second
    if(s>0):
        m =  (GameTime - 1) - (m % GameTime)
    else:
        m = GameTime - (m % GameTime)
    mintsInSecs = m * 60
    if(s>0):
        s = 60 - s
    total_secs = mintsInSecs + s
    print("total Seconds")
    print(total_secs)
    if total_secs <= ResultTime:
        print(False)
        return False
    else:
        print(True)
        return True
def generate_taxnid():
    Intz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(Intz)
    fullDate = now.strftime('%Y/%m/%d/%I/%M/%S')
    taxid = fullDate.replace('/','')
    print('from generate')
    print(taxid)
    return taxid

def pri():
    contract_money=[12,120]
    ticket=[1,2,3]
    users = '3333333333'
    number = random.randint(0,9)
    _group = random.randint(1,4)
    ficontractmoney = random.choice(contract_money)
    fiticket = random.choice(ticket)
    ficontractamt = int(fiticket)*int(ficontractmoney)
    joingroup = group.objects.get(groupId=_group)
    gUser = User.objects.get(username=users)
    print(gUser)
    authUser = user.objects.get(username = gUser)
    
    try:
        Intz = pytz.timezone('Asia/Kolkata')
        now = datetime.now(Intz)
        nowTime = now.strftime('%I:%M:%S %p')
        fullDate = now.strftime('%d/%m/%Y %I:%M:%S %p')
        if countdown():
            createGD = gameDetails(
                user = authUser, 
                period = period(),
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
            _gd = gameDetails.objects.all().filter(user = authUser)
            print(_gd.count())
        else:
            print('game Stoped! calculating Result')
    except Exception as e:
        print(e)
        print('went wrong')
def calculateResult():
    print('job started')
    currentperiod = period()
    print('For Period' + currentperiod)
    bet_map = {}
    Intz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(Intz)
    print('At Time')
    print(now)
    nowTime = now.strftime('%I:%M:%S %p')
    nowDate = now.strftime('%d-%m-%Y')
    allgroups = group.objects.all()
    for _group in allgroups:
        bet_map[_group.groupName]={0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
        allgames = gameDetails.objects.filter(group = _group,period=currentperiod)
        for games in allgames:
            grp = bet_map[_group.groupName]
            prevvalue = grp[int(games.number)]
            prevvalue=int(prevvalue)+int(games.totalcontractMoney)
            grp[int(games.number)]=prevvalue
        _sortValue = sorted(bet_map[_group.groupName].items(), key=lambda x: x[1])
        minValue = _sortValue[0]
        #minValue = [1,0]
        
        # program for random result generate according to the minvalue
        finalresult = []
        for i in _sortValue:
            # i = [1,0] next loop i=[2,0]
            
            if i[1] == minValue[1]:
            # if 0 == 0
            #if minvalue amount 12 == _sortvalue amonut 12
                finalresult.append(i)
                
        # now generating the the res using random method
        res = random.choice(finalresult)       
        #end 
        print(f'group : {_group.groupName}..wonNUMBER {res[0]}... amount: {res[1]}')
        # print("Group"+_group.groupName)
        # print("result of Group")
        # print(res)
        createResult = results(result = res[0]
                               ,group=_group
                               ,period=currentperiod
                               ,date= nowDate
                               ,time=nowTime
                               )  
        createResult.save()
        gameDetails.objects.filter(group = _group,period=currentperiod).update(resultId=createResult)
        # getwinner = gameDetails.objects.filter(
        #     group=_group
        #     ,number=res[0]
        #     ,totalcontractMoney=res[1]
        #     )
        # print('get winner')
        # print(getwinner)
        # print(f'getwinner end of group : {_group}')
    # in Scheduler page need to implement this Logic --> after updating the result in gamedetails filter the gamedetails with current result 
    # and get the user who has won add x10 (10 is configurable) to the total contract amount eg (12 x 10) 120 plus in wallet 
    
    print("Full Map")
    print(bet_map)
    now = datetime.now(Intz)
    print('End Time')
    print(now)
        
def startJobMin():
    Intz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(Intz)
    n = int(GameTime)
    t = 60
    div = int(t/n)
    lst = []
    for i in range(0,div+1):
        lst.append(i*n);
    mins = now.minute
    for j in lst:
        if j > mins:
            bal_mins = lst[lst.index(j)] - mins
            B_I_S = (bal_mins * 60) -  now.second
            Total_secs = B_I_S - ResultTime
            print("First Job Going to Start This Time")
            print(now + timedelta(seconds=Total_secs))
            return now + timedelta(seconds=Total_secs)
def start():
    scheduler = BackgroundScheduler()
    gameTimeInSeconds = GameTime * 60
    print("Start method TRIGGERD")
    # calculateResult()
    scheduler.add_job(calculateResult, 'interval',seconds = gameTimeInSeconds ,start_date=startJobMin(), end_date='2040-08-05 23:47:05')
    scheduler.start()
def playgame():
    scheduler = BackgroundScheduler()
    scheduler.add_job(pri,'interval',seconds=10)
    scheduler.start()