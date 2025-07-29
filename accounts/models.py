from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=200, null=True, verbose_name="Имя")
    phone = models.CharField(max_length=200, null=True, verbose_name="Телефон")
    email = models.CharField(max_length=200, null=True, verbose_name="Email")
    profile_pic = models.ImageField(default="profiles/default.jpg", null=True, blank=True, verbose_name="Фото профиля")
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата регистрации")

    def __str__(self):
        if self.name:
            return str(self.name)
        elif self.user:
            return str(self.user)
        return "Неизвестный клиент"


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    price = models.FloatField(null=True, verbose_name="Цена")

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('В ожидании', 'В ожидании'),
        ('В работе', 'В работе'),
        ('Готов', 'Готов'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, verbose_name="Клиент")
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name="Изделие")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата создания")
    status = models.CharField(max_length=200, null=True, choices=STATUS, default='В ожидании', verbose_name="Статус заказа")
    note = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.product} - {self.customer}"
