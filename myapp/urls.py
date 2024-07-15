from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/get-bpm/', views.get_bpm, name='get_bpm'),
    path('api/get-bpm-from-session/', views.get_bpm_from_session, name='get_bpm_from_session'),
    path('api/submit-questions/', views.submit_questions, name='submit_questions'),
    re_path(r'^.*/$', TemplateView.as_view(template_name='index.html')),
]
