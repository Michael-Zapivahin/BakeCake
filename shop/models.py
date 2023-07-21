from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **kwargs):
        if not phone_number:
            raise ValueError('Phone number must be set.')

        user = self.model(
            phone_number=phone_number,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **kwargs)


class CustomUser(AbstractBaseUser):
    phone_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name',  'email']

    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        return f"{self.first_name} {self.email}"


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
    # levels = 0
    # form = 0
    # topping = 0
    # berries = 0
    # decor = 0
    # inscription = 0
    # img = 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Торт"
        verbose_name_plural = "Торты"


