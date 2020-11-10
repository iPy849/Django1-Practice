from django.urls import path
from . import views

app_name='birthday'
urlpatterns = [
    path('', views.index, name='index'),
    path('conf', views.conf, name='conf')
]