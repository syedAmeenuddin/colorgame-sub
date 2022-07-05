from django.contrib import admin
# from .models import lotteryimages
from .models import lotteryimages, user, bankDetails, upiDetails, gameDetails

# Register your models here.

admin.site.register(lotteryimages)
# Register your models here.
admin.site.register(gameDetails)
admin.site.register(user)
admin.site.register(bankDetails)
admin.site.register(upiDetails)