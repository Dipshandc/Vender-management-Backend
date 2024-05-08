from django.utils import timezone
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer, AcknowledgementSerializer, IssueDateSerializer
class VendorViewSet(ModelViewSet):
  queryset = Vendor.objects.all()
  serializer_class = VendorSerializer


class PurchaseOrderViewSet(ModelViewSet):
  queryset = PurchaseOrder.objects.all()
  serializer_class = PurchaseOrderSerializer


class HistoricalPerformanceView(APIView):
  serializer_class = HistoricalPerformanceSerializer

  def get(self,request,pk):
    historical_performance = get_object_or_404(HistoricalPerformance,vendor=pk)
    serializer = self.serializer_class(historical_performance)
    return Response(serializer.data,status=status.HTTP_200_OK)

class IssueDateView(APIView):
  serializer_class = IssueDateSerializer

  def post(self,request,po_number):
    purchase_order = get_object_or_404(PurchaseOrder,po_number=po_number)
    purchase_order.status = 'informed'
    purchase_order.issue_date = timezone.now()
    purchase_order.save()
    return Response(status=status.HTTP_200_OK)  
  
class AcknowledgementView(APIView):
  serializer_class = AcknowledgementSerializer

  def post(self,request,po_number):
    purchase_order = get_object_or_404(PurchaseOrder,po_number=po_number)
    purchase_order.status = 'listed'
    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save()
    return Response(status=status.HTTP_200_OK)