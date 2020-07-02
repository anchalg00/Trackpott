from django.urls import path
from .view import *
app_name = "projects"

urlpatterns = [
    path('', index, name="index"),
    path('transfer', transfer, name="transfer"),
    path('<int:id>', get_project, name="get_project"),
    path('items/<int:id>', items, name="items"),
    path('item/<int:id>', get_project_item, name="get_project_item"),
    path('pending_material_report', pending_material_report,
         name="pending_material_report"),
    path('missing_material_report', missing_material_report,
         name="missing_material_report"),
    path('approval_request', approval_request, name="approval_request"),
    path('approve_item/<int:id>', approve_item, name="approve_item"),
    path('transfer_report', transfer_report, name="transfer_report"),
    path('pdf_report/<int:id>', pdf_report, name="pdf_report"),

    path('project_activity/<int:id>', get_project_activity,
         name="get_project_activity"),

    path('update_project_activity_plan', update_project_activity_plan,
         name="update_project_activity_plan"),
    path('excel_activity', excel_activity, name="excel_activity"),
    path('get_project_activity_plan_by_year_month', get_project_activity_plan_by_year_month,
         name="get_project_activity_plan_by_year_month"),
    path('project_activity', project_activity, name="project_activity"),
    path('create_activity', create_activity, name="create_activity"),
    path('edit_activity', edit_activity, name="edit_activity"),
    path('plans/<int:id>', plans, name="plans"),
    path('set_plan_fixed/<int:id>', set_plan_fixed, name="set_plan_fixed"),
    path('update_revisor/<int:id>', update_revisor, name="update_revisor"),
    path('get_project_activity_plan/<int:id>',
         get_project_activity_plan, name="get_project_activity_plan"),
    path('revise_plans', revise_plans, name="revise_plans"),
    path('revised_plan_report', revised_plan_report, name="revised_plan_report"),
    path('revise_plan/<int:id>', revise_plan, name="revise_plan"),
    path('chart_report', chart_report, name="chart_report"),
    path('edit_schedule_info', edit_schedule_info, name="edit_schedule_info"),
]
