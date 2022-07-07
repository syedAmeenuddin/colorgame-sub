from datetime import datetime
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class lotteryimages(models.Model):
    lotteryimage1 = models.ImageField(upload_to='ColorGameApp/images/', blank=True)
    lotteryimage2 = models.ImageField(upload_to='ColorGameApp/images/', blank=True)
    lotteryimage3 = models.ImageField(upload_to='ColorGameApp/images/', blank=True)
    lotteryimage4 = models.ImageField(upload_to='ColorGameApp/images/', blank=True)
    lotteryimagegif1 = models.ImageField(upload_to='ColorGameApp/images/', blank=True)
    lotteryimagegif2 = models.ImageField(upload_to='ColorGameApp/images/', blank=True)
    lotteryimagegif3 = models.ImageField(upload_to='ColorGameApp/images/', blank=True)
    lotteryimagegif4 = models.ImageField(upload_to='ColorGameApp/images/', blank=True)


class user(models.Model):
    userId = models.AutoField(primary_key=True,blank=True)
    username =  models.ForeignKey(User,on_delete=models.CASCADE,blank=True,max_length=10,null=True)
    walletBalance = models.CharField(max_length = 7,blank=True,null=True)
    
    def __str__(self):
        return str(self.username)
class bankDetails(models.Model):
    bankId = models.AutoField(primary_key=True,blank=True)
    user = models.ForeignKey(user,on_delete=models.CASCADE,blank=True,max_length=10,null=True)
    ifsc = models.CharField(blank=True,max_length=20)
    accountNumber = models.CharField(blank=True,max_length=20)
    recipientName = models.CharField(blank=True,max_length=50)
    def __str__(self):
        return str(self.user)
class upiDetails(models.Model):
    upiId = models.AutoField(primary_key=True,blank=True)
    user = models.ForeignKey(user,on_delete=models.CASCADE,blank=True,max_length=10,null=True)
    upi = models.CharField(blank=True,max_length=50)
    def __str__(self):
        return str(self.user)
class group(models.Model):
    groupId = models.AutoField(primary_key=True,blank=False)
    groupName = models.CharField(max_length=10, blank=False)
    def __str__(self):
        return str(self.groupName)
class results(models.Model):
    resultId =  models.AutoField(primary_key=True,blank=False)
    group = models.ForeignKey(group,blank=True,on_delete=models.CASCADE)
    result = models.CharField(blank=True,max_length=100)
    period =models.CharField(blank=True,max_length=50)
    date = models.CharField(blank=True,max_length=100)
    time = models.CharField(blank=True,max_length=100)
    def __str__(self):
        return str(self.result)
class gameDetails(models.Model):
    gameId = models.AutoField(primary_key=True,blank=True)
    resultId = models.ForeignKey(results,blank=True,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(user,on_delete=models.CASCADE,blank=True,max_length=10)
    period =models.CharField(blank=True,max_length=50)
    date = models.CharField(blank=True,max_length=100)
    time = models.CharField(blank=True,max_length=100)
    group = models.ForeignKey(group,blank=True,on_delete=models.CASCADE,null=True)
    number = models.CharField(blank=True,max_length=5)
    contractMoney = models.CharField(blank=True,max_length=7)
    tickets = models.CharField(blank=True,max_length=5)
    totalcontractMoney = models.CharField(blank=True,max_length=7)
    def __str__(self):
        return str(self.period)
