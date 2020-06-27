from django.urls import path
from .view import index, transfer, get_project,items, get_project_item, transfer_report, pdf_report, pending_material_report, approval_request, approve_item
from .views import edit_proj
from .view import excel_export,missing_material_report
from .views import project_materials
app_name = "projects"

urlpatterns = [
    path('', index, name="index"),
    path('transfer', transfer, name="transfer"),
    path('<int:id>', get_project, name="get_project"),
    path('items/<int:id>', items, name="items"),
    path('item/<int:id>', get_project_item, name="get_project_item"),
    path('pending_material_report', pending_material_report, name="pending_material_report"),
    path('approval_request', approval_request, name="approval_request"),
    path('approve_item/<int:id>', approve_item, name="approve_item"),
    # path('reject_item/<int:id>', reject_item, name="reject_item"),
    path('edit/<int:id>/',edit_proj,name="edit_proj"),
    path('transfer_report', transfer_report, name="transfer_report"),
    path('pdf_report/<int:id>', pdf_report, name="pdf_report"),
    path('project-material/',project_materials,name="project_materials"),
    path('export_excel',excel_export,name="export_excel"),
    path('missing_material_report', missing_material_report,
         name="missing_material_report"),
]
