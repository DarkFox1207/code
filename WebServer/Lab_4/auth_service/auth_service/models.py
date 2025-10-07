from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Уже включает username и password по умолчанию
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'