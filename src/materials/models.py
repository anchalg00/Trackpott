from django.db import models
from django.conf import settings
# Create your models here.


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
