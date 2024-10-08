from django.db import models

NULLABLE = {"blank": True, "null": True}


class Company(models.Model):
    FACTORY = 'Завод'
    RETAIL_NETWORK = 'Розничная сеть'
    INDIVIDUAL_ENTREPRENEUR = 'Индивидуальный предприниматель'

    SALES_NETWORK_OBJECT = [
        (FACTORY, 'завод'),
        (RETAIL_NETWORK, 'розничная сеть'),
        (INDIVIDUAL_ENTREPRENEUR, 'индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=50, unique=True, verbose_name='название компании')
    email = models.EmailField(verbose_name='email', unique=True)
    country = models.CharField(max_length=30, verbose_name='страна')
    city = models.CharField(max_length=30, verbose_name='город', **NULLABLE)
    street = models.CharField(max_length=30, verbose_name='улица', **NULLABLE)
    house = models.CharField(max_length=10, verbose_name='дом', **NULLABLE)
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE, verbose_name='поставщик')
    debt_supplier = models.DecimalField(max_digits=20, decimal_places=2, default=0,
                                        verbose_name='задолжность перед поставщиком')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    network_object = models.CharField(
        max_length=50,
        choices=SALES_NETWORK_OBJECT,
        verbose_name="объект торговой сети")
    number_in_supply_chain = models.PositiveIntegerField(**NULLABLE, verbose_name='номер в цепочке поставок')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'компании'


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='название продукта')
    model = models.CharField(max_length=50, verbose_name="модель продукта", **NULLABLE)
    date_release = models.DateField(verbose_name='дата выхода на рынок')
    company = models.ForeignKey('Company',on_delete=models.SET_NULL, **NULLABLE, verbose_name='продукты')
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
