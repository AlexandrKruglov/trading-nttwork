from django.contrib.auth.models import AbstractUser
from django.db import models

from company.models import NULLABLE, Company


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=30, verbose_name="имя")
    last_name = models.CharField(max_length=30, verbose_name="фамилия", **NULLABLE)
    email = models.EmailField(unique=True, verbose_name="email")
    phone = models.CharField(max_length=35, verbose_name="телефон", **NULLABLE)
    company = models.ForeignKey(Company, **NULLABLE, on_delete=models.CASCADE, verbose_name='из компании')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

