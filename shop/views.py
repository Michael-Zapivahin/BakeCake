import datetime
import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from more_itertools import chunked

from django.views.generic import TemplateView

from order.models import Order
from .backends import LoginBackend
from .forms import CustomLoginForm
from .models import Cake, Category, CustomUser

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

    Order.objects.create(
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


def add_user(results):
    try:
        user = CustomUser.objects.get(phone_number=results["PHONE"])
    except CustomUser.DoesNotExist:
        CustomUser.objects.create_user(
            phone_number=results["PHONE"],
            first_name=results["NAME"],
            email=results["EMAIL"],
        )
        return 'success'


def index(request):
    if "REG" in request.GET:
        if is_valid_phone_number(str(request.GET.get('REG'))):
            user_phone = request.GET['REG']
            # Проверяем, существует ли пользователь с таким номером телефона
            try:
                user = CustomUser.objects.get(phone_number=user_phone)
            except CustomUser.DoesNotExist:
                # Если пользователя нет, то создаем нового пользователя
                user = CustomUser.objects.create_user(
                    phone_number=user_phone,
                )
                user.save()
            else:
                form = CustomLoginForm(initial={'username': user_phone})
                user = form.get_user()
            user = authenticate(request, username=user_phone, backend=LoginBackend)
            if user is not None:
                # Авторизуем пользователя в системе
                login(request, user)
            return redirect('main')

    if "TOPPING" in request.GET:
        results = request.GET
        create_order(results)
        add_user(results)
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


def create_detail_order(results):
    cake_pk = int(results["CAKE_PK"])
    date_time_str = f'{results["date"]} {results["time"]}'
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    deliv_date = date_time_obj.date()
    deliv_time = date_time_obj.time()

    Order.objects.create(
        ready_cake=cake_pk,
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
            create_detail_order(results)
            return render(request, 'index.html')
    return render(request, 'detail.html', context)
