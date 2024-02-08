
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from web3 import Web3
from django.db import models
from django.contrib.auth.models import User
import requests
# URL Binance Smart Chain
bsc_node_url = 'https://bsc-testnet.publicnode.com'
w3 = Web3(Web3.HTTPProvider(bsc_node_url))

# Модель кошелька
class Wallet(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=42)

    def __str__(self):
        return self.user.username

# Функция создания BSC кошелька
def create_bsc_wallet():
    if w3.is_connected():
        address = w3.eth.account.create().address
        print(address)
        return address
    else:
        print('Unable to connect to BSC network')

# Представление для регистрации пользователя
def registration_view(request):
    errors = []

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Проверка наличия пользователя с таким именем или email
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            errors.append('ошибка1')
        if len(password) < 8:
            errors.append('ошибка2')
        if not errors:
            # Создание пользователя
            user = User.objects.create_user(username=username, email=email, password=password)
            Wallet.objects.create(user=user, address=create_bsc_wallet())  # Создание кошелька для нового пользователя
            return redirect('login')

    return render(request, 'registration.html', {'errors': errors})


# Представление для входа пользователя
def login_view(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = authenticate(username=username, password=password)
        if user is not None and User.objects.filter(email=email).exists():
            login(request, user)
            return redirect('wallet_balance')
        else:
            errors.append('ошибка3')

    return render(request, 'login.html', {'errors': errors})

# Получение баланса BSC кошелька
def get_bsc_balance(address):
    if w3.is_address(address):
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return balance_eth
    else:
        raise ValueError('Invalid BSC address')


from django.contrib.auth.decorators import login_required

@login_required
def wallet_balance_view(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    balance = get_bsc_balance(wallet.address)

    # Получаем стоимость BNB в USD
    bnb_usd_price = get_bnb_price(request)

    # Вычисляем баланс в USD
    usd_balance = round(float(balance) * float(bnb_usd_price), 2)

    if not request.POST.get('csrfmiddlewaretoken'):
        return render(request, 'wallet_balance.html', {'balance': balance, 'usd_balance': usd_balance, 'address': wallet.address, 'username': user.username, 'email': user.email, 'password': user.password})
    return render(request, 'wallet_balance.html', {'balance': balance, 'usd_balance': usd_balance, 'address': wallet.address, 'username': user.username, 'email': user.email, 'password': user.password})
def get_bnb_price(request):
    import requests

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '01d8b7ef-7deb-4660-840f-9efd2e8ffb41',
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()

        if data['status']['error_code'] == 0:
            # Ищем BNB в данных
            bnb_data = next((coin for coin in data['data'] if coin['symbol'] == 'BNB'), None)

            if bnb_data:
                # Извлекаем стоимость BNB в USD и возвращаем ее
                bnb_usd_price = bnb_data['quote']['USD']['price']
                return bnb_usd_price
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return None



def start_view(request):
    return render(request, 'index.html')
