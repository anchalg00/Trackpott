"""trackpot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from projects.views import register_view
from projects.views import home_view, en_upload_SG_view
from django.contrib.auth import views as auth_views
from materials.views import register_store_view
from django.conf.urls import url
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from django.conf.urls.static import static
from chart.views import TaskView
from django.contrib.auth.decorators import login_required
from users.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),


    path('materials/',include('materials.urls')),
    path('purchase_orders/',include('purchase_orders.urls')),
    path('projects/',include('projects.urls')),




    # path('logout/',auth_views.LogoutView.as_view(template_name= 'users/logout.html'), name='logout'),
    # path('registerSpools/',register_spools_view , name='registerSpools'),
    # re_path(r'^(?P<page_id>[0-9]+)/$', subproject_view, name='pagedetail'),
    re_path('chart/', include('chart.urls'), name='ganttchart'),
    re_path(r'^task/(?P<schedule_id>\d+)/$',
            login_required(TaskView.as_view()), name='gchart'),
    re_path('storeview/', register_store_view, name='Store'),

    # url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    #  url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})

    #path('registerProject/',complete_project_view , name='Projectlist'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'media/(?P<path>.*)$',
                serve, {'document_root': settings.MEDIA_ROOT, }),
    ]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^media/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#     ]
