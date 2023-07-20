from django.db import models
from django.utils import timezone

from shop.models import Cake


class Order(models.Model):
    ready_cake = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name='order_cakes', blank=True, null=True)
    title = models.CharField(
        'Название торта',
        max_length=90,
        blank=True,
        null=True
    )
    name = models.CharField(
        'Имя заказчика',
        max_length=20
    )
    phonenumber = models.CharField(
        'Номер телефона',
        max_length=15,
        blank=True,
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    comment = models.TextField(
        'Комментарий к заказу',
        blank=True
    )
    delivery_date = models.DateField(
        "Дата доставки",
        db_index=True,
        default=timezone.now
    )
    delivery_time = models.TimeField(
        "Время доставки",
        db_index=True,
        default=timezone.now
    )
    price = models.IntegerField(
        verbose_name="Стоимость торта",
        blank=True, null=True
    )
    levels = models.CharField(
        'Уровни торта',
        max_length=15,
        blank=True,
    )
    form = models.CharField(
        'Форма торта',
        max_length=15,
        blank=True,
    )
    topping = models.CharField(
        'Топпинг',
        max_length=50,
        blank=True,
    )
    berries = models.CharField(
        'Ягоды',
        max_length=50,
        blank=True,
    )
    decor = models.CharField(
        'Декор',
        max_length=90,
        blank=True,
    )
    inscription = models.CharField(
        'Надпись на торте',
        max_length=200,
        blank=True,
    )
    deliv_comment = models.TextField("Комментарий для курьера", blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    is_active = models.BooleanField('Активен ли заказ', default=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.name} {self.address}"
