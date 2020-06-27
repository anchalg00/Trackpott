from django.urls import path
from .views import index, get_purchase_order, items, get_purchase_order_item, report, addition_report, pdf_report
app_name = "purchase_orders"

urlpatterns = [
    path('', index, name="index"),
    path('<int:id>', get_purchase_order, name="get_purchase_order"),
    path('items/<int:id>', items, name="items"),
    path('item/<int:id>', get_purchase_order_item, name="get_purchase_order_item"),
    path('report', report, name="report"),
    path('addition_report', addition_report, name="addition_report"),
    path('pdf_report/<int:id>', pdf_report, name="pdf_report"),
]
