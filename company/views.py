from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from company.models import Company, Product
from company.paginators import CustomPagination
from company.serializers import CompanySerializer, ProductSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_fields = ('country',)
    pagination_class = CustomPagination

    def perform_create(self, serializer, *args, **kwargs):
        """" Присваиваем порядковый номер в цепочке поставок"""
        company = serializer.save()
        if company.network_object == 'Завод':
            company.number_in_supply_chain = 0
        else:
            company_supplier = company.supplier
            company_supplier_number_in_supply_chain = company_supplier.number_in_supply_chain
            company.number_in_supply_chain = company_supplier_number_in_supply_chain + 1
        company.save()


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ('company',)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Ссылка на компанию собственика продукта"""
        product = serializer.save()
        product.company = self.request.user.company
        product.save()
