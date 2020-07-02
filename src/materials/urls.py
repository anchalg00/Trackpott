from django.urls import path
from .view import index, get_material, excel_export
app_name = "materials"

urlpatterns = [
    path('', index, name="index"),
    path('<int:id>', get_material, name="get_material"),
    path('excel_export', excel_export, name="excel_export"),
]
