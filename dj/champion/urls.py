from django.urls import path
from . import views

app_name = 'champion'

urlpatterns = [
    path('', views.LinkListView.as_view(), name='index'),
    path('link/new/', views.LinkCreateView.as_view(), name='link_new'),
]
