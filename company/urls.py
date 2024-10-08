from rest_framework.routers import SimpleRouter, DefaultRouter

from company.apps import CompanyConfig
from company.views import CompanyViewSet, ProductViewSet

app_name = CompanyConfig.name

router = SimpleRouter()

router.register(r'company', CompanyViewSet, basename='company')
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = []

urlpatterns += router.urls

