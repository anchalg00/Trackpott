from django.db import models
from django.utils import timezone
from materials.models import Store
from django.conf import settings
from chart.models import Schedule
# Create your models here.

class Project(models.Model):
    receipt_number = models.CharField(max_length=32)
    contract_name = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    address = models.CharField(max_length=191,blank=True,null=True)
    delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    schedule = models.ForeignKey(Schedule,null=True, blank=True, on_delete=models.SET_NULL)
    assigned_for = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL)


class ProjectItem(models.Model):
    quantity = models.IntegerField(default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    is_pending = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL)

class ProjectMissingItem(models.Model):
    quantity = models.IntegerField(default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)