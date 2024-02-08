
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wallet.urls')),
    path('wallet_balance', include('wallet.urls')),
    path('login', include('wallet.urls')),
]
