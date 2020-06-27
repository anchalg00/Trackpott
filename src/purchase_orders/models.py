from django.db import models
from django.utils import timezone
from materials.models import Store
from django.conf import settings


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=32)
    vendor_name = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    address = models.CharField(max_length=191,blank=True,null=True)
    delivery_date = models.DateField(blank=True, null=True)
    PO_STATUS_CHOICE = (
        ('op', 'Open'),
        ('d', 'Delivered'),
    )
    po_status = models.CharField(
        max_length=2,
        choices=PO_STATUS_CHOICE,
        default='op',
    )
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL)


class PurchaseOrderItem(models.Model):
    quantity = models.IntegerField(default=0)
    item = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL)
