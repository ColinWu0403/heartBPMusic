from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/get-bpm/', views.get_bpm, name='get_bpm'),
    re_path(r'^.*/$', TemplateView.as_view(template_name='index.html')),

]
