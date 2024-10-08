from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from company.models import Company, Product
from users.models import User


class TestCompany(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.company = Company.objects.create(
            name="завод",
            email="factory@mail.ru",
            country="РФ",
            debt_supplier='5.05',
            network_object="Завод",
        )
        self.product = Product.objects.create(
            name=" tv",
            date_release="2024-10-05",
            company=self.company,
            price='10.01',
        )

    def test_retrieve_company(self):
        """ Тестирование просмотра компании """

        url = reverse("company:company-detail", args=(self.company.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.company.name)
        self.assertEqual(data.get("email"), self.company.email)
        self.assertEqual(data.get("country"), self.company.country)
        self.assertEqual(data.get("debt_supplier"), self.company.debt_supplier)

    def test_company_list(self):
        """Тестируем вывод списка компаний."""

        response = self.client.get('/company/company/')
        data = response.json()
        results = {"count": 1,
                   "next": None,
                   "previous": None,
                   "results": [
                       {
                           "id": self.company.pk,
                           "name": self.company.name,
                           "email": self.company.email,
                           "country": self.company.country,
                           "city": None,
                           "street": None,
                           "house": None,
                           "supplier": None,
                           "debt_supplier": self.company.debt_supplier,
                           "network_object": self.company.network_object,
                           "number_in_supply_chain": None,
                           "product": [
                               {
                                   "id": self.product.pk,
                                   "name": self.product.name,
                                   "model": None,
                                   "date_release": self.product.date_release,
                                   "price": self.product.price,
                                   "company": self.company.pk
                               }]}]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.all().count(), 1)
        self.assertEqual(data, results)


    def test_company_create(self):
        """Тестируем создание компании."""
        data = {
            "name": "test_create",
            "email": "test@mail.ru",
            "country": "РФ",
            "debt_supplier": 5.05,
            "network_object": "Завод",
        }
        response = self.client.post('/company/company/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.all().count(), 2)

    def test_company_update(self):
        """Тестируем изменение компании."""

        url = reverse("company:company-detail", args=(self.company.pk,))
        data = {
            "email": "myfactory@mail.ru",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), "myfactory@mail.ru")

    def test_company_update_prohibition_actions(self):
        """Тестируем запрет на изменение задолжности компании."""

        url = reverse("company:company-detail", args=(self.company.pk,))
        data = {
            "debt_supplier": 10.05,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_company_delete(self):
        """Тестируем удаление компании."""

        url = reverse("company:company-detail", args=(self.company.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.all().count(), 0)


    def test_retrieve_product(self):
        """ Тестирование просмотра продукта """

        url = reverse("company:product-detail", args=(self.product.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.product.name)
        self.assertEqual(data.get("date_release"), self.product.date_release)
        self.assertEqual(data.get("company"), self.product.company.pk)
        self.assertEqual(data.get("price"), self.product.price)

    def test_product_list(self):
        """Тестируем вывод списка продуктов."""

        response = self.client.get('/company/product/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.all().count(), 1)


    def test_product_create(self):
        """Тестируем создание продукта."""
        data = {
            "name": "test_create",
            "date_release": "2024-10-05",
            "company": self.company.pk,
            "price": 5.05,
        }
        response = self.client.post('/company/product/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.all().count(), 2)

    def test_product_update(self):
        """Тестируем изменение продукта."""

        url = reverse("company:product-detail", args=(self.product.pk,))
        data = {
            "price": 10.25,
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("price"), '10.25')



    def test_product_delete(self):
        """Тестируем удаление продукта."""

        url = reverse("company:product-detail", args=(self.product.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.all().count(), 0)
