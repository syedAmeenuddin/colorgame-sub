from django.contrib import admin
# from .models import lotteryimages
from .models import user, bankDetails, upiDetails, gameDetails, group, results, wallet

# Register your models here.

# admin.site.register(lotteryimages)
# Register your models here.
admin.site.register(gameDetails)
admin.site.register(user)
admin.site.register(bankDetails)
admin.site.register(upiDetails)
admin.site.register(group)
admin.site.register(results)
admin.site.register(wallet)