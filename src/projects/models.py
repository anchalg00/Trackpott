from django.db import models
from django.utils import timezone
from materials.models import Store
from django.conf import settings
from chart.models import Schedule
# Create your models here.


class Project(models.Model):
    receipt_number = models.CharField(max_length=32)
    contract_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=191, blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    schedule = models.ForeignKey(
        Schedule, null=True, blank=True, on_delete=models.SET_NULL)
    assigned_for = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


class ProjectItem(models.Model):
    quantity = models.IntegerField(default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    is_pending = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


class ProjectMissingItem(models.Model):
    quantity = models.IntegerField(default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


class ProjectActivity(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    weightage = models.FloatField(blank=False, null=False)
    schedule = models.ForeignKey(
        Schedule, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    revisor = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


class ProjectActivityPlan(models.Model):
    plan_year = models.CharField(max_length=4, blank=False, null=False)
    plan_month = models.CharField(max_length=3, blank=False, null=False)
    plan_value = models.FloatField()
    actual_value = models.FloatField()
    is_plan_fixed = models.BooleanField(default=False)
    project_activity = models.ForeignKey(
        ProjectActivity, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


class ProjectActivityPlanLog(models.Model):
    old_plan_value = models.FloatField()
    project_activity_plan = models.ForeignKey(
        ProjectActivityPlan, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


class ScheduleInfo(models.Model):
    schedule = models.ForeignKey(
        Schedule, null=True, blank=True, on_delete=models.SET_NULL)
    project_description = models.CharField(
        max_length=191, blank=True, null=True)
    project_date = models.DateField(blank=True, null=True)
    weekly_progress = models.CharField(max_length=191, blank=True, null=True)
    cummlative_progress = models.CharField(
        max_length=191, blank=True, null=True)
    variance = models.CharField(max_length=191, blank=True, null=True)
    progress_statistic = models.CharField(
        max_length=191, blank=True, null=True)
    procurement = models.CharField(max_length=191, blank=True, null=True)
    mdr = models.CharField(max_length=191, blank=True, null=True)
    fabrication = models.CharField(max_length=191, blank=True, null=True)
    installation = models.CharField(max_length=191, blank=True, null=True)
    reason_for_variance = models.CharField(
        max_length=191, blank=True, null=True)
    detailed_progress_for_week = models.CharField(
        max_length=191, blank=True, null=True)
    planned_progress_for_next_week = models.CharField(
        max_length=191, blank=True, null=True)
    area_of_concerns = models.CharField(max_length=191, blank=True, null=True)


class ScheduleDocument(models.Model):
    schedule = models.ForeignKey(
        Schedule, null=True, blank=True, on_delete=models.SET_NULL)
    file_url = models.FileField(upload_to='schedule_files/')
    created_at = models.DateTimeField(default=timezone.now)
