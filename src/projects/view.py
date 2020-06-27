from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from chart.models import Schedule
from django.contrib.auth.models import User
from .models import Project, ProjectItem,ProjectMissingItem
from .forms import ProjectForm, ProjectItemForm
from materials.models import Store
from datetime import datetime
from openpyxl import Workbook
from helpers.Render import Render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from purchase_orders.models import PurchaseOrderItem
from django.db import connection as conn


@login_required
def index(request):
    project_selected = Schedule.objects.filter(is_selected=True)
    selected_project = project_selected.first()
    id = Schedule.objects.filter(is_selected=True).first().id
    if id is not None:
        initial_id = 0
        form = ProjectForm(request.POST or None, request=request)
        if request.method == 'POST':
            if request.POST['_id'] == '0':
                if form.is_valid():
                    form_instance = form.save(commit=False)
                    form_instance.schedule_id = id
                    # form_instance.created_by_id = request.user.id
                    form_instance.save()
                    return redirect('projects:index')
            else:
                initial_id = request.POST['_id']
                project = Project.objects.get(pk=initial_id)
                form = ProjectForm(request.POST or None,
                                   instance=project, request=request)
                if form.is_valid():
                    form_instance = form.save(commit=False)
                    form_instance.save()
                    return redirect('projects:index')
        queryset_list = Project.objects.filter(
            schedule_id=id).order_by('receipt_number')
        if 'receipt_number' in request.GET and request.GET['receipt_number'] != '':
            queryset_list = queryset_list.filter(
                receipt_number__icontains=request.GET['receipt_number'])
        if 'name' in request.GET and request.GET['name'] != '':
            queryset_list = queryset_list.filter(
                schedule__name__icontains=request.GET['name'])
        context = {
            "projects": queryset_list,
            "schedule": Schedule.objects.get(id=id),
            "form": form,
            "initial_id": initial_id,
            'project_selected' : project_selected,
            'project_list_first': selected_project
        }
        return render(request, 'projects/manage_projects.html', context)
    else:
        return HttpResponse('<h1>Project is not selected</h1>')


@login_required
def get_project(request, id):
    project_selected = Schedule.objects.filter(is_selected=True)
    selected_project = project_selected.first()
    project = Project.objects.filter(id=id)
    return JsonResponse({"project": list(project.values()), "username": User.objects.filter(id=project[0].assigned_for_id).first().username})


@login_required
def transfer(request):
    project_selected = Schedule.objects.filter(is_selected=True)
    selected_project = project_selected.first()
    id = Schedule.objects.filter(is_selected=True).first().id
    if id is not None:
        initial_id = 0
        form = ProjectItemForm(request.POST or None)
        if request.method == 'POST':
            if request.POST['_id'] == '0':
                if form.is_valid():
                    form_instance = form.save(commit=False)
                    form_instance.project_id = id
                    form_instance.created_by_id = request.user.id
                    form_instance.save()
                    return redirect('projects:items', id=id)
            else:
                initial_id = request.POST['_id']
                project_item = ProjectItem.objects.get(pk=initial_id)
                form = ProjectItemForm(
                    request.POST or None, instance=project_item)
                if form.is_valid():
                    form.save()
                    return redirect('projects:items', id=id)
        context = {
            "project_items": ProjectItem.objects.filter(project_id=id).order_by('-id'),
            "form": form,
            "initial_id": initial_id,
            "project": Project.objects.get(id=id),
            'project_selected' : project_selected,
            'project_list_first': selected_project
        }
        return render(request, 'projects/manage_project_items.html', context)
    else:
        return HttpResponse('<h1>Project is not selected</h1>')


@login_required
def items(request, id):
    project_selected = Schedule.objects.filter(is_selected=True)
    selected_project = project_selected.first()
    initial_id = 0
    form = ProjectItemForm(request.POST or None)
    if request.method == 'POST':
        if request.POST['_id'] == '0':
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.project_id = id
                form_instance.created_by_id = request.user.id
                form_instance.save()
                return redirect('projects:items', id=id)
        else:
            initial_id = request.POST['_id']
            project_item = ProjectItem.objects.get(pk=initial_id)
            form = ProjectItemForm(request.POST or None, instance=project_item)
            if form.is_valid():
                form.save()
                return redirect('projects:items', id=id)
    project = Project.objects.get(id=id)
    context = {
        "project_items": ProjectItem.objects.filter(project_id=id).order_by('-id'),
        "form": form,
        "initial_id": initial_id,
        "schedule": Schedule.objects.get(id=project.schedule_id),
        "project": project,
        'project_selected' : project_selected,
        'project_list_first': selected_project
    }
    return render(request, 'projects/manage_project_items.html', context)


@login_required
def get_project_item(request, id):
    project_selected = Schedule.objects.filter(is_selected=True)
    selected_project = project_selected.first()
    project_item = ProjectItem.objects.filter(id=id)
    return JsonResponse(serializers.serialize("json", project_item), safe=False)


@login_required
def transfer_report(request):
    project_selected = Schedule.objects.filter(is_selected=True)
    selected_project = project_selected.first()
    queryset_list = ProjectItem.objects.order_by('-id')
    if 'item_id' in request.GET and request.GET['item_id'] != '':
        queryset_list = queryset_list.filter(item_id=request.GET['item_id'])
    if 'from_date' in request.GET and request.GET['from_date'] != '':
        from_date = datetime.strptime(request.GET['from_date'], '%d-%m-%Y')
        if from_date:
            queryset_list = queryset_list.filter(created_at__gte=from_date)
    if 'to_date' in request.GET and request.GET['to_date'] != '':
        to_date = datetime.strptime(request.GET['to_date'], '%d-%m-%Y')
        if to_date:
            queryset_list = queryset_list.filter(created_at__lte=to_date)
    context = {
        'materials': Store.objects.all(),
        'items': queryset_list,
        'project_selected' : project_selected,
        'project_list_first': selected_project
    }
    if 'export' in request.GET and request.GET['export'] == 'excel':
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename={date}-material-transfer-report-trackpott.xlsx'.format(
            date=datetime.now().strftime('%Y-%m-%d'),
        )
        workbook = Workbook()

        # Get active worksheet/tab
        worksheet = workbook.active
        worksheet.title = 'Report - Material Transfer'

        # Define the titles for columns
        columns = [
            'Date of transfer',
            'Item Name',
            'Specification',
            'Material',
            'Quantity',
        ]
        row_num = 1

        # Assign the titles for each cell of the header
        for col_num, column_title in enumerate(columns, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = column_title

        # Iterate through all movies
        for qs in queryset_list:
            row_num += 1

            # Define the data for each cell in the row
            row = [
                qs.created_at,
                qs.item.item_s,
                qs.item.spec_s,
                qs.item.material_s,
                qs.quantity
            ]

            # Assign the data for each cell of the row
            for col_num, cell_value in enumerate(row, 1):
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.value = cell_value

        workbook.save(response)
        return response
    elif 'export' in request.GET and request.GET['export'] == 'pdf':
        return Render.render('projects/pdf_material_transfer_report.html', context)
    else:
        return render(request, 'projects/material_transfer_report.html', context)


@login_required
def pdf_report(request, id):
    project_selected = Schedule.objects.filter(is_selected=True)
    selected_project = project_selected.first()
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        return HttpResponse('<h1>Page not found!</h1>')

    project_items = ProjectItem.objects.filter(project_id=id)
    context = {
        'project': project,
        'project_items': project_items,
        'project_selected' : project_selected,
        'project_list_first': selected_project
    }
    return Render.render('projects/pdf_report.html', context)


@login_required
def pending_material_report(request):
    project_selected = Schedule.objects.filter(is_selected=True)
    selected_project = project_selected.first()
    queryset_list = ProjectItem.objects.filter(is_pending=True)
    if 'receipt_number' in request.GET and request.GET['receipt_number'] != '':
        queryset_list = queryset_list.filter(
            project__receipt_number=request.GET['receipt_number'])
    context = {
        "pending_items": queryset_list,
        'project_selected' : project_selected,
        'project_list_first': selected_project
    }
    if 'export' in request.GET and request.GET['export'] == 'pdf':
        return Render.render('projects/pdf_pending_material_report.html', context)
    else:
        return render(request, 'projects/pending_material_report.html', context)


@login_required
def approval_request(request):
    project_selected = Schedule.objects.filter(is_selected=True)
    selected_project = project_selected.first()
    queryset_list = ProjectItem.objects.filter(
        project__assigned_for_id=request.user.id, is_approved=False)
    context = {
        "pending_items": queryset_list,
        'project_selected' : project_selected,
        'project_list_first': selected_project
    }
    return render(request, 'projects/approval_request.html', context)


@login_required
def approve_item(request, id):
    try:
        _quantity = request.GET.get('quantity')
        print(_quantity)
        project_item = ProjectItem.objects.get(pk=id)
        qs_po = PurchaseOrderItem.objects.values('item_id').filter(purchase_order__po_status='d').filter(
            item_id=project_item.item_id).annotate(sum_quantity=Sum('quantity'))
        qs_project = ProjectItem.objects.values('item_id').filter(is_approved=True).filter(
            item_id=project_item.item_id).annotate(sum_quantity=Sum('quantity'))
        po_quantity = qs_po[0]['sum_quantity'] if qs_po is not None and qs_po else 0
        project_quantity = qs_project[0]['sum_quantity'] if qs_project is not None and qs_project else 0
        actual_quantity = int(po_quantity) - int(project_quantity)
        if project_item.quantity < int(_quantity):
            return render(request, 'projects/stock_not_available.html')
        if actual_quantity < int(_quantity):
            return render(request, 'projects/stock_not_available.html')
        else:
            if project_item.quantity > int(_quantity):
                project_quantity = int(project_item.quantity) - int(_quantity)
                ProjectMissingItem.objects.create(
                    quantity=project_quantity,
                    project_id=project_item.project_id,
                    item_id=project_item.item_id,
                    created_by_id=request.user.id
                )
            project_item.quantity = int(_quantity)
            project_item.is_pending = False
            project_item.is_approved = True
            project_item.save()
            return redirect('projects:approval_request')
    except ProjectItem.DoesNotExist:
        return HttpResponse('<h1>Item not found!</h1>')
# @login_required
# def reject_item(request, id):
#     project_selected = Schedule.objects.filter(is_selected=True)
#     selected_project = project_selected.first()
#     project_item = ProjectItem.objects.get(pk=id)
#     project_item.is_pending = False
#     project_item.is_approved = False
#     project_item.save()
#     return redirect('projects:approval_request')
    
@login_required
def excel_export(request):
    project_selected = Schedule.objects.filter(is_selected=True)
    selected_project = project_selected.first()
    queryset_list=[]
    materials=ProjectItem.objects.all()
    for element in materials:
        if element.project.schedule==selected_project and element.is_approved:
            queryset_list.append(element)
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={date}-material-report-trackpott.xlsx'.format(
        date=datetime.now().strftime('%Y-%m-%d'),
    )
    workbook = Workbook()

    # Get active worksheet/tab
    worksheet = workbook.active
    worksheet.title = 'Report - Materials'

    # Define the titles for columns
    columns = [
        'Item',
        'Specification',
        'Material',
        'Rating',
        'Size 1',
        'Schedule 1',
        'Size 2',
        'Schedule 2',
        'Facing',
        'Quantity'
    ]
    row_num = 1

    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    # Iterate through all movies
    for qs in queryset_list:
        row_num += 1

        # Define the data for each cell in the row
        row = [
            qs.item.item_s,
            qs.item.spec_s,
            qs.item.material_s,
            qs.item.rating_s,
            qs.item.size1_s,
            qs.item.sch1_s,
            qs.item.size2_s,
            qs.item.sch2_s,
            qs.item.facing_s,
            qs.quantity
        ]

        # Assign the data for each cell of the row
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    workbook.save(response)
    return response

@login_required
def missing_material_report(request):
    queryset_list = ProjectMissingItem.objects.all()
    if 'receipt_number' in request.GET and request.GET['receipt_number'] != '':
        queryset_list = queryset_list.filter(
            project__receipt_number=request.GET['receipt_number'])
    context = {
        "missing_items": queryset_list
    }
    if 'export' in request.GET and request.GET['export'] == 'pdf':
        return Render.render('projects/pdf_missing_material_report.html', context)
    else:
        return render(request, 'projects/missing_material_report.html', context)