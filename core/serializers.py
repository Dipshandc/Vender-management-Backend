from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(ModelSerializer):
  vendor_code = serializers.CharField(read_only=True)

  class Meta:
    model = Vendor
    fields = ['vendor_code','name','contact_details','address']


class PurchaseOrderSerializer(ModelSerializer):
  po_number = serializers.CharField(read_only=True)
  order_date = serializers.CharField(read_only=True)

  class Meta:
    model = PurchaseOrder
    fields = ['po_number','vendor','order_date','delivery_date','items','quantity','status','quality_rating','issue_date','acknowledgment_date']


class HistoricalPerformanceSerializer(ModelSerializer):
  date = serializers.CharField(read_only=True)
  on_time_delivery_rate = serializers.CharField(read_only=True)
  quality_rating_avg = serializers.CharField(read_only=True)
  quality_rating_avg = serializers.CharField(read_only=True)
  fulfillment_rate = serializers.CharField(read_only=True)

  class Meta:
    model = HistoricalPerformance
    fields = ['vendor','date','average_response_time','on_time_delivery_rate','quality_rating_avg','quality_rating_avg','fulfillment_rate']


class AcknowledgementSerializer(ModelSerializer):
  class Meta:
    model = PurchaseOrder
    fields = []

class IssueDateSerializer(ModelSerializer):
  class Meta:
    model = PurchaseOrder
    fields = []