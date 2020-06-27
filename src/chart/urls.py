from django.conf.urls import url
from .views import TaskView
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^(?P<s_id>\d+)/$', TemplateView.as_view(template_name='gantt.html'), name='ganttchart'),
    url(r'^task/(?P<schedule_id>\d+)/$', TaskView.as_view())
]
