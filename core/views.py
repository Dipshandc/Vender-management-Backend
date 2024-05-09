from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .permission import IsVendorOrReadOnly, IsCustomerOrReadOnly, IsAdminOrReadOnly
from .serializers import VendorSerializer,\
                        PurchaseOrderSerializer,\
                        HistoricalPerformanceSerializer,\
                        AcknowledgementSerializer,\
                        IssueDateSerializer,\
                        CustomUserSerializer

class CreateUserAPIView(APIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.user_type == "vendor":
                try:
                    vendor = Group.objects.get(name='Vendor')
                except Group.DoesNotExist:
                    return Response('Vendor group not found', status=status.HTTP_400_BAD_REQUEST)
                user.groups.add(vendor)
                user.save()
                vendor_contact_details = request.data.get("contact_details")
                vendor_address = request.data.get("address")
                Vendor.objects.create(name=user, contact_details=vendor_contact_details, address=vendor_address)
                return Response("Vendor account created", status=status.HTTP_201_CREATED)
            else:
                try:
                    customer = Group.objects.get(name='Customer')
                except Group.DoesNotExist:
                    return Response('Customer group not found', status=status.HTTP_400_BAD_REQUEST)
                user.groups.add(customer)
                user.save()
                return Response("Customer account created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsVendorOrReadOnly]

    def list(self, request, *args, **kwargs):
      queryset = self.filter_queryset(self.get_queryset())
      page = self.paginate_queryset(queryset)
      if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
      serializer = self.get_serializer(queryset, many=True)
      return Response(serializer.data)
    

class PurchaseOrderViewSet(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsCustomerOrReadOnly]


class HistoricalPerformanceView(APIView):
    serializer_class = HistoricalPerformanceSerializer
    permission_classes = [AllowAny]

    def get(self,request,pk):
      historical_performance = get_object_or_404(HistoricalPerformance,vendor=pk)
      serializer = self.serializer_class(historical_performance)
      return Response(serializer.data,status=status.HTTP_200_OK)

class IssueDateView(APIView):
   serializer_class = IssueDateSerializer
   permission_classes = [IsAdminOrReadOnly]


   def post(self,request,po_number):
      purchase_order = get_object_or_404(PurchaseOrder,po_number=po_number)
      purchase_order.status = 'informed'
      purchase_order.issue_date = timezone.now()
      purchase_order.save()
      return Response(status=status.HTTP_200_OK)  
  
class AcknowledgementView(APIView):
    serializer_class = AcknowledgementSerializer
    permission_classes = [IsVendorOrReadOnly]

    def post(self,request,po_number):
      purchase_order = get_object_or_404(PurchaseOrder,po_number=po_number)
      purchase_order.status = 'listed'
      purchase_order.acknowledgment_date = timezone.now()
      purchase_order.save()
      return Response(status=status.HTTP_200_OK)