from django.db import models


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


class CustomCake(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cakes')
    price = models.IntegerField(
        verbose_name="Стоимость торта"
    )

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Торт"
        verbose_name_plural = "Торты"


