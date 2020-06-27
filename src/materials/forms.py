from django import forms

from .models import Requirement,Proj,Document,Store,Progress
from chart.models import Schedule



class MaterialRegisterForm(forms.ModelForm):


	class Meta:
		model=Requirement
		fields= ['spool_details' , 'drawing_no', 'line_no' ,'spec',
    "item",
    "material",
    "rating",
    "size1" ,
    "sch1",
    "size2",
    "sch2",
    "facing",
    "qty",
    "time_due",
    "remarks"]

class MaterialForm(forms.ModelForm):
    item_s = forms.CharField(required=True,label='Item',max_length="100",widget=forms.TextInput(attrs={'class': 'form-control'}))
    spec_s = forms.CharField(required=False,label='Spec',max_length="100",widget=forms.TextInput(attrs={'class': 'form-control'}))
    material_s = forms.CharField(required=True,label='Material',max_length="100",widget=forms.TextInput(attrs={'class': 'form-control'}))
    rating_s = forms.CharField(required=False,label='',max_length="100",widget=forms.TextInput(attrs={'class': 'form-control'}))
    size1_s = forms.IntegerField(required=True,label='',widget=forms.TextInput(attrs={'class': 'form-control'}))
    sch1_s = forms.IntegerField(required=False,label='',widget=forms.TextInput(attrs={'class': 'form-control'}))
    size2_s = forms.IntegerField(required=False,label='',widget=forms.TextInput(attrs={'class': 'form-control'}))
    sch2_s = forms.IntegerField(required=False,label='',widget=forms.TextInput(attrs={'class': 'form-control'}))
    facing_s = forms.CharField(required=True,label='',max_length="100",widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model=Store
        fields = ["item_s","spec_s","material_s","rating_s","size1_s","sch1_s","size2_s","sch2_s","facing_s"]

    def clean(self):
        rating = self.cleaned_data.get("rating_s")
        sch1 = self.cleaned_data.get("sch1_s")
        if rating is None:
            if sch1 is None:
                raise forms.ValidationError("Schedule 1 field is required!")
        if sch1 is None:
            if rating is None:
                raise forms.ValidationError("Rating field is required!")

class ProgressRegisterForm(forms.ModelForm):


    class Meta:
        model=Progress
        fields= ['progress_p','variance_p','remarks_p',
        'mdr_progress_m','variance_m','remarks_m',
        'procurement_progress_pp', 'variance_pp','remarks_pp',
        'eng_progress_ep', 'variance_ep', 'remarks_ep',
        'fab_progress_fp', 'variance_fp','remarks_fp',
         'install_progress_ip', 'variance_ip' , 'remarks_ip']

class StoreRegisterForm(forms.ModelForm):



    class Meta:
        model=Store
        fields= ["item_s",'spec_s',
                "material_s",
                "rating_s",
                "size1_s" ,
                "sch1_s",
                "size2_s",
                "sch2_s",
                "facing_s",
            ]



class DocumentRegisterForm(forms.ModelForm):
    choices_roi = (
        ('IFA','IFA'),
        ('IFI' ,'IFI')
    )
    choices_ac = (
    ('CODE 1', 'CODE 1'),
    ('CODE 2' , 'CODE 2'),
    ('CODE 3','CODE 3'),
    ('RFI','RFI')

    )
    ADNOC_documentno = forms.CharField(required=True,label='',max_length="100",widget=forms.TextInput(attrs={'class': 'form-control', 'cols':10}))
    description = forms.CharField(required=False,label='',widget=forms.TextInput(attrs={'class': 'form-control'}))
    revision = forms.CharField(required=False ,label='',widget=forms.TextInput(attrs={'class': 'form-control'}))
    due_date = forms.DateField(required=True,label='',widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
    submission_date = forms.DateField(required=True,label='',widget=forms.TextInput(attrs={'class': 'form-control','type':'date'}))
    transmittal_number = forms.CharField(required=True,label='',max_length="100",widget=forms.TextInput(attrs={'class': 'form-control'}))
    reason_of_issue = forms.CharField(widget=forms.Select( choices=choices_roi, attrs={'class': 'form-control' }))
    document = forms.FileField(required=False,label='',widget=forms.FileInput())
    aprroval_date = forms.DateField(required=False,input_formats=['%d-%m-%Y'],label='',widget=forms.TextInput(attrs={'class': 'form-control','type':'date'}))
    receipt_transmittalno = forms.CharField(required=False,label='',max_length="100",widget=forms.TextInput(attrs={'class': 'form-control'}))
    view_response = forms.FileField(required=False,label='',widget=forms.FileInput())
    aprroval_code = forms.CharField(widget=forms.Select( choices=choices_ac, attrs={'class': 'form-control' }))
    remarks = forms.CharField(required=False,label='',max_length="100",widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model=Document
        fields= ['ADNOC_documentno',
                 'description',
                'revision',
                'due_date',
                'submission_date',
                'transmittal_number',
                'reason_of_issue',
                'document',
                'aprroval_date',
                'receipt_transmittalno',
                'view_response',
                'aprroval_code',
                'remarks']
        

    def __init__(self, *args, **kwargs):
        super(DocumentRegisterForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['ADNOC_documentno'].widget.attrs['style'] = 'width:130px;'
        self.fields['revision'].widget.attrs['style'] = 'width:70px;'
        self.fields['due_date'].widget.attrs['style'] = 'width:155px;'
        self.fields['reason_of_issue'].widget.attrs['style'] = 'width:75px;'
        self.fields['document'].widget.attrs['style'] = 'width:95px;'
        self.fields['view_response'].widget.attrs['style'] = 'width:95px;'
        self.fields['aprroval_date'].widget.attrs['style'] = 'width:155px;'
        self.fields['submission_date'].widget.attrs['style'] = 'width:155px;'
        self.fields['aprroval_code'].widget.attrs['style'] = 'width:105px;'







class ProjectRegisterForm(forms.ModelForm):

    progress_schedule = forms.FloatField(required=False,label='Progress')
    class Meta:
        model=Schedule
        fields= ['name','contractor_name','start_date','end_date','progress_schedule']


