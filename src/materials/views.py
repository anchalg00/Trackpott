from django.shortcuts import render, redirect, render_to_response
from .forms import ProjectRegisterForm, StoreRegisterForm
from django.views.generic import ListView, CreateView, TemplateView
from .models import Store
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from datetime import date
# from fpdf import FPDF
from django.urls import reverse
from django.http import HttpResponseRedirect
from io import BytesIO
from django.core.files import File
from django.contrib import messages
from chart.models import Schedule
# from .utils import render_to_pdf
# from .forms import UploadFileForm

# from chartit import DataPool, Chart, PivotDataPool, PivotChart
# Create your views here.


@login_required()
def register_store_view(request, *args, **kwargs):
    project_selected = Schedule.objects.filter(
        added_by=request.user, is_selected=True)
    selected_project = project_selected.first()

    object_list = Store.objects.filter()

    if request.method == 'POST':
        form1 = StoreRegisterForm(request.POST, request.FILES)
        if form1.is_valid():
            obj = form1.save()
            obj.save()

            messages.success(request, 'Report generated')

            return HttpResponseRedirect(reverse('Store', args=()))
    else:
        form1 = StoreRegisterForm()
    return render(request, "materials/listviewStore.html", {'form1': form1, 'object_list': object_list, 'project_list_first': selected_project})



# class table_view(ListView):
# 	template_name="materials/listview.html"
# 	queryset = Requirement.objects.all()

# 	if request.method=='POST':
# 			form = MaterialRegisterForm(request.POST)
# 			if form.is_valid():
# 				form.save()
# 				username=form.cleaned_data.get('username');

# 				return redirect('RequirementList')
# 	else:
# 		form=MaterialRegisterForm()
# 	return render(request,"materials/listview.html",{'form':form })


@login_required()
def subproject_view(request, page_id):
    obj = Proj.objects.get(id=page_id)

    SubprojectFormset = modelformset_factory(
        Subproj, fields=('name', 'plan_date', 'complete_date'))
    # ACTIVITES FORMSET
    if request.method == 'POST':
        # formset = SubprojectFormset(request.POST , queryset=Subproj.objects.filter(proj_id =obj.id , is_subproj = False))
        formset = SubprojectFormset(
            request.POST, queryset=Subproj.objects.filter(proj_id=obj.id))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.proj_id = obj.id
                # instance.is_subproj = False
                instance.save()
            return redirect('pagedetail', page_id=obj.id)
    # formset = SubprojectFormset(queryset=Subproj.objects.filter(proj_id=obj.id , is_subproj=False))
    formset = SubprojectFormset(
        queryset=Subproj.objects.filter(proj_id=obj.id))
    # SUBPROJECT FORMSET

    # if request.method == 'POST':
    # 	formset2 = SubprojectFormset(request.POST , queryset=Subproj.objects.filter(proj_id =obj.id , is_subproj=True))
    # 	if formset2.is_valid():
    # 		instances2 = formset2.save(commit = False)
    # 		for instance2 in instances2:
    # 			instance2.proj_id = obj.id
    # 			instance2.is_subproj = True
    # 			instance2.save()
    # 		return redirect('pagedetail',page_id=obj.id)
    # formset2 = SubprojectFormset(queryset=Subproj.objects.filter(proj_id=obj.id, is_subproj=True))

    # sales = DataPool(
    #    series=
    #     [{'options': {
    #     #    'source': SalesReport.objects.all()},
    #     'source': Subproj.objects.filter(proj_id = obj.id)},
    #     #'source': SalesReport.objects.filter(sales__lte=10.00)},
    #         'terms': [{'name': 'name',
    #         'days': 'days'}]
    #         },
    #     ])

    # cht = Chart(
    #    	datasource = sales,
    #     series_options =
    #       [{'options':{
    #           'type': 'column',
    #           'stacking': False},
    #         'terms':{
    #           'name': [
    #             'days']
    #         }}],
    #     chart_options =
    #       {'title': {
    #            'text': 'Activity Days'},
    #        'xAxis': {
    #            'title':{'text': 'Activity name'}},
    #        'yAxis': {
    #            'title': {'text': 'Number of days'}},
    #        })

    # qs = Subproj.objects.filter(proj_id = obj.id)

    # import plotly.figure_factory as ff
    # from plotly.offline import plot

    # df = [dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
    #       dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
    #       dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')]

    # fig = ff.create_gantt(df)
    # figure = plot(fig)

    context = {
        "object": obj,
        'formset': formset,
        # 'chart_list' : cht,
        # 'qs':qs,
        # 'graph':figure,
        # 'formset2': formset2
    }
    return render_to_response('materials/create_subproject.html', context)
    # return render(request,"materials/create_subproject.html",context)
