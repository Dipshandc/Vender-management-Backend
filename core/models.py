from django.db import models
import uuid
from django.core.validators import MinValueValidator

def generate_vendor_code():
  return str(uuid.uuid4())[:5]

class Vendor(models.Model):
    vendor_code = models.CharField(primary_key=True,max_length=6,default=generate_vendor_code)
    name = models.CharField(max_length=25,null=False,blank=False)
    contact_details = models.TextField(null=False,blank=False)
    address = models.TextField(null=False,blank=False)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(primary_key=True, max_length=6, default=generate_vendor_code)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    delivery_date = models.DateTimeField(null=False, blank=False)
    items = models.JSONField(null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('informed',),
        ('listed','Listed')
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0, "Rating cannot be negative")])
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"PO number: {self.po_number} - Vendor: {self.vendor}"

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(validators=[MinValueValidator(0.0, "Rate cannot be negative")])
    quality_rating_avg = models.FloatField(validators=[MinValueValidator(0.0, "Rating cannot be negative")])
    average_response_time = models.FloatField(validators=[MinValueValidator(0.0, "Time cannot be negative")])
    fulfillment_rate = models.FloatField(validators=[MinValueValidator(0.0, "Rate cannot be negative")])

    def __str__(self):
        return f"Performance for {self.vendor} on {self.date}"
