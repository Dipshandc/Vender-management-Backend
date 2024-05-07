from django.urls import path, include
from rest_framework import routers
from .views import VendorViewSet, PurchaseOrderViewSet, HistoricalPerformanceView, AcknowledgementView, IssueDateView
router = routers.SimpleRouter()
router.register('vendors', VendorViewSet)
router.register('purchase_orders',PurchaseOrderViewSet)

urlpatterns = [
    path('/', include(router.urls)),
    path('/vendors/<str:pk>/performance/',HistoricalPerformanceView.as_view(),name='performance'),
    path('/purchase_orders/<str:pk>/acknowledge/',AcknowledgementView.as_view(),name='acknowledgement'),
    path('/purchase_orders/<str:pk>/issue/',IssueDateView.as_view(),name='issue')
]
