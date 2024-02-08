from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_view, name='index'),
    path('registration/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('wallet_balance/', views.wallet_balance_view, name='wallet_balance'),


]

#python manage.py makemigrations
#python manage.py migrate
#python manage.py runserver
