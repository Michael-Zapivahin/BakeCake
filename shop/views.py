import datetime
import re
import requests
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from more_itertools import chunked

from order.models import Order
from .forms import CustomAuthenticationForm
from .models import Cake, Category, CustomUser
from .pay import pay
from BakeCake.settings import BITLY_AUTH_TOKEN

CASTOM_CAKE = {
    'Levels': ['не выбрано', '1', '2', '3'],
    'Forms': ['не выбрано', 'Круг', 'Квадрат', 'Прямоугольник'],
    'Toppings': ['не выбрано', 'Без топпинга', 'Белый соус', 'Карамельный', 'Кленовый', 'Черничный',
                 'Молочный шоколад', 'Клубничный'],
    'Berries': ['нет', 'Ежевика', 'Малина', 'Голубика', 'Клубника'],
    'Decors': ['нет', 'Фисташки', 'Безе', 'Фундук', 'Пекан', 'Маршмеллоу', 'Марципан'],
}

phone_number_regex = re.compile(r'^\+?[1-9]\d{1,14}$')


def is_valid_phone_number(phone_number):
    return phone_number_regex.match(phone_number) is not None


def create_order(results):
    levels = CASTOM_CAKE['Levels'][int(results["LEVELS"])]
    forms = CASTOM_CAKE['Forms'][int(results["FORM"])]
    topping = CASTOM_CAKE['Toppings'][int(results["TOPPING"])]
    berries = 'Без ягод'
    if "BERRIES" in results:
        berries = CASTOM_CAKE['Berries'][int(results["BERRIES"])]
    decor = 'Без декора'
    if "DECOR" in results:
        decor = CASTOM_CAKE['Decors'][int(results["DECOR"])]
    words = results["WORDS"]
    comment = results["COMMENTS"]
    name = results["NAME"]
    phone = results["PHONE"]
    email = results["EMAIL"]
    address = results["ADDRESS"]
    date_time_str = f'{results["DATE"]} {results["TIME"]}'
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    deliv_date = date_time_obj.date()
    deliv_time = date_time_obj.time()
    deliv_comment = results["DELIVCOMMENTS"]
    price = results["PRICE"]

    order = Order.objects.create(
        name=name,
        title='Кастомный тортец',
        price=price,
        phonenumber=phone,
        address=address,
        comment=comment,
        delivery_date=deliv_date,
        delivery_time=deliv_time,
        levels=levels,
        form=forms,
        topping=topping,
        berries=berries,
        decor=decor,
        inscription=words,
        deliv_comment=deliv_comment,
        email=email
    )
    return order


def add_user(results):
    try:
        user = User.objects.get(username=results["PHONE"])
        user.first_name = results["NAME"]
        user.email = results["EMAIL"]
        user.save()
    except User.DoesNotExist:
        user = CustomUser.objects.get_or_create(
            phone_number=results["PHONE"]
        )
        return user


def index(request):
    if "TOPPING" in request.GET:
        results = request.GET
        order = create_order(results)
        add = add_user(results)
        print('create_order')
        if create_order:
            price = order.price
            phone = order.phonenumber
            email = order.email
            title = order.title
            order_number = order.pk

            create_pay = pay(price, phone, email, title, order_number)

            print(create_pay["confirmation"])
            url = create_pay["confirmation"]["confirmation_url"]
            return redirect(url)
    return render(request, 'index.html')


def show_catalog(request, category_slug=None):
    columns_count = 2
    cakes = Cake.objects.all()
    category = None
    categories = Category.objects.all()
    products = Cake.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Cake.objects.filter(category=category)

    page_columns = list(chunked(cakes, columns_count))
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'page_columns': page_columns,
    }

    return render(request, template_name='catalog.html', context=context)


def show_agreement(request):
    return render(request, 'agreement.html')


def show_main_page(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/register.html', {'form': form})


def count_clicks(bitlink, token=BITLY_AUTH_TOKEN):
    api_endpoint = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(api_endpoint, headers=headers)
    response.raise_for_status()
    total_clicks = response.json()['total_clicks']
    return total_clicks


def clicks(request):
    clicks_quantity = 0
    if request.method == 'POST':
        bitlink = request.POST.get("bitlinky", False)
        clicks_quantity = count_clicks(bitlink)
    return render(request, 'count_clicks.html', {'clicks_quantity': clicks_quantity})


def create_detail_order(results):
    cake_pk = int(results["CAKE_PK"])
    cake = Cake.objects.get(pk=cake_pk)
    date_time_str = f'{results["date"]} {results["time"]}'
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    deliv_date = date_time_obj.date()
    deliv_time = date_time_obj.time()

    order = Order.objects.create(
        ready_cake=cake,
        title=results["TITLE"],
        name=results["NAME"],
        price=results["PRICE"],
        phonenumber=results["PHONE"],
        address=results["ADDRESS"],
        delivery_date=deliv_date,
        delivery_time=deliv_time,
        deliv_comment=results["DELIVCOMMENTS"],
        email=results["EMAIL"]
    )
    return order


def product_detail(request, pk):
    product = get_object_or_404(Cake, pk=pk)
    # category = product.category
    context = {
        'product': product,
        # 'category': category,
    }
    if request.POST:
        if "TITLE" in request.POST:
            results = request.POST
            order = create_detail_order(results)
            print('create_order')
            if create_order:
                price = order.price
                phone = order.phonenumber
                email = order.email
                title = order.title
                order_number = order.pk

                create_pay = pay(price, phone, email, title, order_number)
                url = create_pay["confirmation"]["confirmation_url"]
                return redirect(url)
    return render(request, 'detail.html', context)


def show_lk_page(request):
    user = request.user
    phonenumber = user.username
    orders = Order.objects.filter(phonenumber=phonenumber)
    if request.GET:
        user.first_name = request.GET['NAME']
        user.email = request.GET['EMAIL']
        user.save()
    context = {
        'user': user,
        'orders': orders,
    }
    return render(request, 'lk.html', context)


