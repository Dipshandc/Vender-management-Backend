from django.db.models.signals import post_save
from django.contrib.auth.models import User 
from django.dispatch import receiver
from ..models import Vendor, HistoricalPerformance, PurchaseOrder
from django.utils import timezone
 
 
@receiver(post_save, sender=Vendor)
def create_vendor_performance(sender, instance, created, **kwargs):
 if created:
   HistoricalPerformance.objects.create(vendor=instance)


@receiver(post_save, sender=PurchaseOrder)
def update_purchase_order(sender, instance, created, **kwargs):
  performance = HistoricalPerformance.objects.get(vendor=instance.vendor)

  if instance.status == 'listed':
    #for calculating average response time
    issue_date=instance.issue_date
    acknowledgment_date = instance.acknowledgment_date 
    difference = ((acknowledgment_date - issue_date).total_seconds() / 60)
    if performance.average_response_time is None:
      performance.average_response_time = round(difference,2)
    else:
      average_response_time = (performance.average_response_time + difference)/2
      performance.average_response_time = round(average_response_time,2)
    performance.save()


  elif instance.status == 'completed':
    #for calculating on time delivery rate
    total_completed_order = PurchaseOrder.objects.filter(vendor=instance.vendor,status='completed').count()
    total_on_time_completed_order = PurchaseOrder.objects.filter(vendor=instance.vendor,status='completed',delivery_date__gte=timezone.now()).count()
    print(total_completed_order,total_on_time_completed_order)
    on_time_delivery_rate = (total_on_time_completed_order/total_completed_order)*100
    print(on_time_delivery_rate)
    performance.on_time_delivery_rate = round(on_time_delivery_rate,2)
    
    #for calculating Quality rating average
    if performance.quality_rating_avg is None:
      performance.quality_rating_avg = round(instance.quality_rating,2)
    else:
      quality_rating_avg = ((performance.quality_rating_avg + instance.quality_rating)/2)
      performance.quality_rating_avg = round(quality_rating_avg,2)
    performance.save()

  else:
    #for calculating fulfillment rate
    total_order = PurchaseOrder.objects.filter(vendor=instance.vendor).count()
    total_completed_order = PurchaseOrder.objects.filter(vendor=instance.vendor).filter(status='completed').count()
    fulfillment_rate = ((total_completed_order/total_order)*100)
    performance.fulfillment_rate = round(fulfillment_rate,2)
    performance.save()


