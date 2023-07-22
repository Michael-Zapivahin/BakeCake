from django.db import models


class CustomUser(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.phone_number


class Client(models.Model):
    telegram_id = models.IntegerField(unique=True)
    nik_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="UserName"
    )

    def __str__(self):
        return f"{self.nik_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Category(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Категория торта",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Cake(models.Model):
    # Модель для добавления тортов через админку для каталога
    name = models.CharField('Название', max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cakes', blank=True, null=True)
    price = models.IntegerField(
        verbose_name="Стоимость торта"
    )
    image = models.ImageField(
        'картинка'
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True, null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Торт"
        verbose_name_plural = "Торты"
