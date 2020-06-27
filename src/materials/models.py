from django.db import models
from chart.models import Schedule
from django.conf import settings

# Create your models here.
class Requirement(models.Model):
    spool_details = models.CharField(max_length=100)
    drawing_no= models.CharField(max_length=100)
    line_no= models.CharField(max_length=100)
    spec= models.CharField(max_length=100)
    item= models.CharField(max_length=100)
    material= models.CharField(max_length=100)
    rating= models.CharField(max_length=100,blank=True,null=True)
    size1= models.IntegerField(blank=True,null=True)
    sch1=models.IntegerField(blank=True,null=True)
    size2=models.IntegerField(blank=True,null=True)
    sch2=models.IntegerField(blank=True,null=True)
    facing= models.CharField(max_length=100,blank=True,null=True)
    qty=models.IntegerField(blank=True,null=True)
    time_due = models.DateField(blank=True,null=True)
    remarks=models.CharField(max_length=100,blank=True,null=True)
    proj = models.ForeignKey(Schedule, on_delete=models.CASCADE,null = True,blank=True)

class Progress(models.Model):
    scurve = models.FileField(upload_to ='scurve/%Y/%m/%d',blank=True,null=True)
    progress_p = models.FloatField(blank=True,null=True)
    variance_p= models.FloatField(blank=True,null=True)
    remarks_p=models.CharField(max_length=100,blank=True,null=True)

    mdr_progress_m = models.FloatField(blank=True,null=True)
    variance_m= models.FloatField(blank=True,null=True)
    remarks_m=models.CharField(max_length=100,blank=True,null=True)

    procurement_progress_pp = models.FloatField(blank=True,null=True)
    variance_pp= models.FloatField(blank=True,null=True)
    remarks_pp=models.CharField(max_length=100,blank=True,null=True)

    eng_progress_ep = models.FloatField(blank=True,null=True)
    variance_ep= models.FloatField(blank=True,null=True)
    remarks_ep=models.CharField(max_length=100,blank=True,null=True)

    fab_progress_fp = models.FloatField(blank=True,null=True)
    variance_fp= models.FloatField(blank=True,null=True)
    remarks_fp=models.CharField(max_length=100,blank=True,null=True)

    install_progress_ip = models.FloatField(blank=True,null=True)
    variance_ip= models.FloatField(blank=True,null=True)
    remarks_ip=models.CharField(max_length=100,blank=True,null=True)
    proj = models.ForeignKey(Schedule, on_delete=models.CASCADE,null = True,blank=True)



class Store(models.Model):
    item_s = models.CharField(max_length=100)
    spec_s = models.CharField(max_length=100)
    material_s = models.CharField(max_length=100)
    rating_s = models.CharField(max_length=100, blank=True, null=True)
    size1_s = models.IntegerField(blank=True, null=True)
    sch1_s = models.IntegerField(blank=True, null=True)
    size2_s = models.IntegerField(blank=True, null=True)
    sch2_s = models.IntegerField(blank=True, null=True)
    facing_s = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.item_s)

    def item_name(self):
        return str(str(self.item_s)+' / '+str(self.spec_s)+' / '+str(self.material_s)+' / '+str(self.rating_s)+' / '+str(self.size1_s)+' / '+str(self.sch1_s)+' / '+str(self.size2_s)+' / '+str(self.sch2_s)+' / '+str(self.facing_s))


class Proj(models.Model):
    name =  models.CharField(max_length=100)
    due_date_proj = models.DateField(blank=True,null=True)


class Subproj(models.Model):
    name = models.CharField(max_length=100)
    days = models.IntegerField(blank=True , null = True)
    plan_date = models.DateField(blank=True,null=True)
    revision_date = models.DateField(blank=True,null=True)
    complete_date = models.DateField(blank=True,null=True)
    status= models.CharField(max_length=75,blank=True,null=True)
    remarks=models.TextField(max_length=200,blank=True,null=True)
    completed = models.BooleanField(blank=True,null=True)
    proj = models.ForeignKey(Proj, on_delete=models.CASCADE,)
    # is_subproj = models.BooleanField(blank=True,null=True)

class Document(models.Model):
    

    choices_roi = (
        ('IFA','IFA'),
        ('IFI' ,'IFI')
    )
    choices_ac = (
        ('CODE 1', 'CODE 1'),
        ('CODE 2' , 'CODE 2'),
        ('CODE 3','CODE 3'),
        ('RFI','RFI')

        )
    choices_status = (
        ('APPROVED','APPROVED'),
        ('REJECTED','REJECTED'),
        ('APPROVED WITH COMMENTS','APPROVED WITH COMMENTS'),
        ('RETAIN FOR INFORMATION','RETAIN FOR INFORMATION')
        )


    ADNOC_documentno = models.CharField(max_length=100)
    description = models.CharField(max_length=100,null = True,blank=True)
    revision= models.CharField(max_length=5,null = True,blank=True)
    due_date=models.DateField(blank=True,null=True)
    submission_date = models.DateField(blank=True,null=True)
    transmittal_number = models.CharField(max_length=100,null = True,blank=True)
    reason_of_issue = models.CharField(max_length = 3 , choices =choices_roi ,default= 'IFA' ,null = True)
    document = models.FileField(upload_to ='documents/%Y/%m/%d',blank=True)
    aprroval_date = models.DateField(blank=True,null = True)
    receipt_transmittalno = models.CharField(max_length=100,null = True,blank=True)
    view_response = models.FileField(max_length=100,null = True,blank=True)
    aprroval_code = models.CharField(choices=choices_ac,default='CODE 1', max_length=100,null = True)
    remarks =  models.CharField(max_length=100,null = True,blank=True)
    proj = models.ForeignKey(Schedule, on_delete=models.CASCADE ,null = True,blank=True)






