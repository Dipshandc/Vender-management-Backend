from django.urls import path, include
from rest_framework import routers
from .views import VendorViewSet,\
                   PurchaseOrderViewSet,\
                   HistoricalPerformanceView,\
                   AcknowledgementView,\
                   IssueDateView,\
                   CreateUserAPIView
                   
                   
router = routers.SimpleRouter()
router.register('vendors', VendorViewSet)
router.register('purchase_orders',PurchaseOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vendors/<str:pk>/performance/',HistoricalPerformanceView.as_view(),name='performance'),
    path('purchase_orders/<str:po_number>/acknowledge/',AcknowledgementView.as_view(),name='acknowledgement'),
    path('purchase_orders/<str:po_number>/issue/',IssueDateView.as_view(),name='issue'),
    path('register/', CreateUserAPIView.as_view(), name='register'),
]
