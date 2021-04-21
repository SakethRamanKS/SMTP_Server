from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',TemplateView.as_view(template_name = 'hello.html')),
    path('login/', views.signup, name = 'signup')
]
