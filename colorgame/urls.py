# """colorgame URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     login
# ]
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from ColorGameApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signin, name='signin'), 
    path('register/', views.register, name='register'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('win/', views.win, name='win'),
    path('win/bankcard/',views.bankcard,name='bankcard'),
    path('win/mybet/',views.mybet,name='mybet'),
    path('win/recharge/',views.recharge,name='recharge'),
    path('win/withdraw/',views.withdraw,name='withdraw'),
    path('win/recharge/success', views.recharge_success, name='recharge_success'),
    path('win/recharge/failure', views.recharge_failure, name='recharge_failure'),
    # path('win/payment_processing/',views.payment_processing,name='payment_processing'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)