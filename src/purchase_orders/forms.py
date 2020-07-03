from django import forms
from django.db.models import Sum
from .models import PurchaseOrder, PurchaseOrderItem
from materials.models import Store
from projects.models import ProjectItem
from django.db import connection as conn


class PurchaseOrderForm(forms.ModelForm):
    po_number = forms.CharField(required=True, max_length="100", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    vendor_name = forms.CharField(required=False, max_length="50", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    address = forms.CharField(required=False, max_length="191", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    delivery_date = forms.DateField(required=True, input_formats=[
                                    '%d-%m-%Y'], label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    po_status = forms.CharField(required=True, label='PurchaseOrder',
                                max_length="100", widget=forms.TextInput(attrs={'class': 'form-control'}))
    PO_STATUS_CHOICE = (
        # ('', '~~ Select ~~'),
        ('op', 'Open'),
        ('d', 'Delivered'),
    )
    po_status = forms.CharField(widget=forms.Select(
        choices=PO_STATUS_CHOICE, attrs={'class': 'form-control'}))

    class Meta:
        model = PurchaseOrder
        fields = ["po_number", "vendor_name",
                  "delivery_date", "address", "po_status"]


class ItemModelChoieField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.item_name())


class PurchaseOrderItemForm(forms.ModelForm):
    quantity = forms.CharField(required=True, label='Item', max_length="100",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    item = ItemModelChoieField(queryset=Store.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = PurchaseOrderItem
        fields = ["quantity", "item"]
        exclude = ('created_at',)

    def clean(self):
        quantity = self.cleaned_data.get("quantity")
        qs_po = PurchaseOrderItem.objects.values('item_id').filter(purchase_order__po_status='d').filter(
            item_id=self.cleaned_data.get('item').id).annotate(sum_quantity=Sum('quantity'))
        qs_project = ProjectItem.objects.values('item_id').filter(is_approved=True).filter(
            item_id=self.cleaned_data.get('item').id).annotate(sum_quantity=Sum('quantity'))
        po_quantity = qs_po[0]['sum_quantity'] if qs_po is not None and qs_po else 0
        project_quantity = qs_project[0]['sum_quantity'] if qs_project is not None and qs_project else 0
        actual_quantity = int(po_quantity) - int(project_quantity)
        if self.instance.id is not None:
            if int(actual_quantity) == 0 and int(self.instance.quantity) > int(quantity):
                raise forms.ValidationError("Stock already dispatched!")
            if abs(int(actual_quantity) - int(self.instance.quantity)) > int(quantity):
                raise forms.ValidationError("Stock already dispatched!")
