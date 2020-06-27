from django import forms 
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from materials.models import Store
from chart.models import Schedule
from .models import Project, ProjectItem
from purchase_orders.models import PurchaseOrderItem
from users.models import Account


class UserRegisterForm(UserCreationForm):
	email= forms.EmailField()

	class Meta:
		model = User
		fields= ['username' , 'email', 'password1' ,'password2']

class ProjectForm(forms.ModelForm):
    receipt_number = forms.CharField(
        required=True, max_length="100", widget=forms.TextInput(attrs={'class': 'form-control'}))
    contract_name = forms.CharField(required=True, label='Name', max_length="100",
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    assigned_for = forms.CharField(required=True, label='Name', max_length="100",
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=False, label='address', max_length="191",
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, label='Description',
                                  max_length="100", widget=forms.TextInput(attrs={'class': 'form-control'}))
    delivery_date = forms.DateField(required=False, input_formats=[
                                    '%d-%m-%Y'], initial=None, label='Delivery Date', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ["receipt_number", "contract_name", "address",
                  "description", "delivery_date", "assigned_for"]
        exclude = ('schedule',)

    def clean_assigned_for(self):
        data = self.cleaned_data['assigned_for']
        print(self.request.user.username)
        if data == self.request.user.username:
            raise forms.ValidationError("You can't assign yourself!")
        else:
            try:
                user = Account.objects.get(username=data)
            except User.DoesNotExist:
                raise forms.ValidationError("User not found!")
        return user


class ItemModelChoieField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.item_name())


class ProjectItemForm(forms.ModelForm):
    quantity = forms.CharField(required=True, label='Item', max_length="100",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    item = ItemModelChoieField(queryset=Store.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ProjectItem
        fields = ["quantity", "item", "is_pending"]
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
            if int(int(actual_quantity) + int(self.instance.quantity)) < int(quantity):
                self.cleaned_data['is_pending'] = True
                # raise forms.ValidationError("Stock not available!")
        else:
            if quantity == '0':
                raise forms.ValidationError("Quantity should not be zero")
            if actual_quantity < int(quantity):
                self.cleaned_data['is_pending'] = True
                # raise forms.ValidationError("Stock not available!")