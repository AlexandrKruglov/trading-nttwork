from django.contrib import admin

from company.models import Company, Product


@admin.action(description="Удалить задолжность перед поставщиком")
def delete_debt(modeladmin, request, queryset):
    queryset.update(debt_supplier=0.00)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'supplier')
    list_filter = ('city',)
    actions = [delete_debt]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
