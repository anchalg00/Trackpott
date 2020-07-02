from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseModelFormSet
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from materials.models import Store
from chart.models import Schedule
from .models import Project, ProjectItem, ProjectActivity, ProjectActivityPlan, ProjectActivityPlanLog, ScheduleInfo, ScheduleDocument
from purchase_orders.models import PurchaseOrderItem
import datetime


def year_choices():
    return tuple([(r, r) for r in range(2001, datetime.date.today().year+5)])


def current_year():
    return datetime.date.today().year


def month_to_num(shortMonth):
    return{
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12}[shortMonth]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


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
        if data == self.request.user.username:
            raise forms.ValidationError("You can't assign yourself!")
        else:
            try:
                user = User.objects.get(username=data)
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


class ProjectActivityForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Name', max_length="100",
                           widget=forms.TextInput(attrs={'class': 'form-control form-name'}))
    weightage = forms.FloatField(required=True, label='Weightage', widget=forms.TextInput(
        attrs={'class': 'form-control form-weightage'}))

    class Meta:
        model = ProjectActivity
        fields = ["name", "weightage"]
        exclude = ('created_at',)


class ProjectActivityFormSet(BaseModelFormSet):
    def clean(self):
        sum_weightage = 0
        for form in self.forms:
            name = form.cleaned_data.get('name')
            weightage = form.cleaned_data.get('weightage')
            if weightage is not None:
                sum_weightage = int(weightage) + int(sum_weightage)
            if name is None:
                raise forms.ValidationError("Activity name is required")
            if weightage is None:
                raise forms.ValidationError("Weightage is required")
        if sum_weightage != 100:
            raise forms.ValidationError(
                "Sum of weightage should be 100, and Current total weightage is "+str(sum_weightage))


class ProjectActivityPlanForm(forms.ModelForm):
    PM_STATUS_CHOICE = (
        ('Jan', 'January'),
        ('Feb', 'February'),
        ('Mar', 'March'),
        ('Apr', 'April'),
        ('May', 'May'),
        ('Jun', 'June'),
        ('Jul', 'July'),
        ('Aug', 'August'),
        ('Sep', 'September'),
        ('Oct', 'October'),
        ('Nov', 'November'),
        ('Dec', 'December'),
    )
    plan_month = forms.CharField(required=True, widget=forms.Select(
        choices=PM_STATUS_CHOICE, attrs={'class': 'form-control'}))
    plan_value = forms.FloatField(required=True, label='Weightage', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    actual_value = forms.FloatField(required=True, label='Actual Value', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    plan_year = forms.CharField(required=True, label='Plan year', widget=forms.Select(
        attrs={'class': 'form-control'}))

    class Meta:
        model = ProjectActivityPlan
        fields = ["plan_month", "plan_value",
                  "plan_year", "actual_value"]
        exclude = ('created_at',)

    def __init__(self, *args, **kwargs):
        self.project_activity_id = kwargs.pop('project_activity_id', None)
        self._plan_years = kwargs.pop('plan_year_options', tuple('',))
        self.schedule_start_date = kwargs.pop('schedule_start_date', None)
        self.request = kwargs.pop('request', None)
        super(ProjectActivityPlanForm, self).__init__(*args, **kwargs)
        self.fields['plan_year'].widget.choices = self._plan_years

    def clean(self):
        plan_year = self.cleaned_data.get("plan_year")
        plan_month = self.cleaned_data.get("plan_month")
        schedule_start_year = datetime.datetime.strptime(
            str(self.schedule_start_date), "%Y-%m-%d").year
        schedule_start_month = datetime.datetime.strptime(
            str(self.schedule_start_date), "%Y-%m-%d").month
        if int(plan_year) <= int(schedule_start_year) and int(month_to_num(plan_month)) < int(schedule_start_month):
            raise forms.ValidationError(
                str(plan_year)+'-'+str(plan_month)+" is not under in schedule started date!")
        if self.instance.id is None:
            project_activity_plan = ProjectActivityPlan.objects.filter(
                project_activity_id=self.project_activity_id, plan_month=plan_month, plan_year=plan_year).count()
            if project_activity_plan > 0:
                raise forms.ValidationError(
                    str(plan_year)+'-'+str(plan_month)+" plan is already exists!")
        else:
            project_activity_plan = ProjectActivityPlan.objects.filter(
                project_activity_id=self.project_activity_id, plan_month=plan_month, plan_year=plan_year).exclude(id=self.instance.id).count()
            if project_activity_plan > 0:
                raise forms.ValidationError(
                    str(plan_year)+'-'+str(plan_month)+" plan is already exists!")
            project_activity_plan = ProjectActivityPlan.objects.get(
                id=self.instance.id)
            if project_activity_plan.is_plan_fixed == True:
                ProjectActivityPlanLog.objects.create(
                    old_plan_value=project_activity_plan.plan_value,
                    project_activity_plan_id=project_activity_plan.id,
                    created_by_id=self.request.user.id
                )


class ScheduleInfoForm(forms.ModelForm):
    project_description = forms.CharField(
        required=True, label='Project Description', widget=forms.TextInput(attrs={'class': 'form-control'}))
    project_date = forms.DateField(required=False, input_formats=[
        '%d-%m-%Y'], initial=None, label='Project Date', widget=forms.DateInput(attrs={'class': 'form-control'}, format="%d-%m-%Y"))
    weekly_progress = forms.CharField(
        required=True, label='Weekly Progress', widget=forms.TextInput(attrs={'class': 'form-control'}))
    cummlative_progress = forms.CharField(
        required=True, label='Cummlative Progress', widget=forms.TextInput(attrs={'class': 'form-control'}))
    variance = forms.CharField(required=True, label='Variance', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    progress_statistic = forms.CharField(
        required=True, label='Progress Statistic', widget=forms.TextInput(attrs={'class': 'form-control'}))
    procurement = forms.CharField(required=True, label='Procurement', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    mdr = forms.CharField(required=True, label='MDR', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    fabrication = forms.CharField(required=True, label='Fabrication', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    installation = forms.CharField(
        required=True, label='Installation', widget=forms.TextInput(attrs={'class': 'form-control'}))
    reason_for_variance = forms.CharField(
        required=True, label='Reason for Variance', widget=forms.TextInput(attrs={'class': 'form-control'}))
    detailed_progress_for_week = forms.CharField(
        required=True, label='Detailed Progress for Week', widget=forms.TextInput(attrs={'class': 'form-control'}))
    planned_progress_for_next_week = forms.CharField(
        required=True, label='Planned Progress for Next Week', widget=forms.TextInput(attrs={'class': 'form-control'}))
    area_of_concerns = forms.CharField(
        required=True, label='Area of Concerns', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ScheduleInfo
        fields = ["project_description", "project_date", "weekly_progress", "cummlative_progress", "variance", "progress_statistic", "procurement", "mdr",
                  "fabrication", "installation", "reason_for_variance", "detailed_progress_for_week", "planned_progress_for_next_week", "area_of_concerns", ]

class ScheduleDocumentForm(forms.ModelForm):
    file_url = forms.FileField()

    class Meta:
        model = ScheduleDocument
        fields = ('file_url',)
        exclude = ('created_at',)