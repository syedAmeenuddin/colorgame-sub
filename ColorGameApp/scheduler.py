from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import lotteryimages, user, bankDetails, upiDetails, gameDetails
from django.contrib.auth.models import User
import pytz
def pri():
    gUser = User.objects.get(username='1111111111')
    authUser = user.objects.get(username = gUser)
    Intz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(Intz)
    nowTime = now.strftime('%I:%M:%S %p')
    nowDate = now.strftime('%Y-%m-%d')
    fullDate = now.strftime('%d/%m/%Y %I:%M:%S %p')
    createGD = gameDetails(
                user = authUser, 
                period = 'azureport2022',
                date = fullDate,
                time = nowTime,
                group = 'A',
                number = 6,
                contractMoney = 12,
                tickets = 1,
                totalcontractMoney = 12,
                )
    createGD.save()
    print(createGD.user)
    print(createGD.period)
    
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(pri,'interval',seconds = 59)
    scheduler.start()
