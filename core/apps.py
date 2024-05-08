from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'



    def ready(self):
        from .signals.handlers import  create_performance, update_purchase_order
        from .models import Vendor, PurchaseOrder
        from django.db.models.signals import post_save
        post_save.connect(create_performance, sender=Vendor)
        post_save.connect(update_purchase_order, sender=PurchaseOrder)
