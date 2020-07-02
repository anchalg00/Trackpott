from django import forms
from chart.models import Schedule
from .models import Store


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





class ProjectRegisterForm(forms.ModelForm):


    class Meta:
        model=Schedule
        fields= ['name','start_date','end_date','progress_schedule']


