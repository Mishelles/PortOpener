from django.db import models
from django.contrib.auth.models import User


# Расширяем встроенную модель пользователя
class AccessToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=30, blank=True)
    token_expiration_datetime = models.DateTimeField(blank=True)


# Храним записи об ip_адресах
class IpRecord(models.Model):
    class Meta:
        app_label = 'main'
        verbose_name = 'Запись об ip-адресе'
        verbose_name_plural = 'Записи об ip-адресах'

    ip_address = models.CharField(max_length=15)
    datetime = models.DateTimeField(auto_now_add=True)
