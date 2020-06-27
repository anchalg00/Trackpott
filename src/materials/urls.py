from django.urls import path
from .view import index, get_material, excel_export
from .views import get_doc,documents_view,excel_export_doc
app_name = "materials"

urlpatterns = [
    path('', index, name="index"),
    path('../documentview', documents_view, name="documentview"),

    path('<int:id>', get_material, name="get_material"),
    path('excel_export', excel_export, name="excel_export"),
    path('excel_export_doc', excel_export_doc, name="excel_export_doc"),

    path('documentview/<int:id>', get_doc, name="get_doc"),


]
