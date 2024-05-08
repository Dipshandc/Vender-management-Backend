from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'



    def ready(self):
        from .signals.handlers import  create_vendor_and_performance, update_purchase_order
        from .models import CustomUser, PurchaseOrder
        from django.db.models.signals import post_save
        post_save.connect(create_vendor_and_performance, sender=CustomUser)
        post_save.connect(update_purchase_order, sender=PurchaseOrder)
