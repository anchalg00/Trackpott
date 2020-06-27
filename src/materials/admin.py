from django.contrib import admin

# Register your models here.
from .models import Requirement,Proj,Subproj,Document,Store,Progress

admin.site.register(Requirement)
admin.site.register(Proj)
admin.site.register(Subproj)
admin.site.register(Document)
admin.site.register(Store)
admin.site.register(Progress)


