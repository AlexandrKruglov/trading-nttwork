from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from company.models import Company, Product
from company.paginators import CustomPagination


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class CompanySerializer(ModelSerializer):
    product = ProductSerializer(read_only=True, many=True, source='product_set',)

    def update(self, instance, validated_data):
        """"Запрет на изменения поля debt_supplier"""
        if 'debt_supplier' in validated_data:
            raise serializers.ValidationError({
                'debt_supplier': 'Вы не можете менять это поле. исключите его из запроса.',
            })

        return super().update(instance, validated_data)

    class Meta:
        model = Company
        fields = ['id', 'name', 'email', 'country', 'city', 'street', 'house', 'supplier',
                  'debt_supplier', 'network_object', 'number_in_supply_chain', 'product']
