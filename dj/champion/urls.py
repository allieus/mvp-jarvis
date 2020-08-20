from django.urls import path, re_path
from . import views

app_name = 'champion'

urlpatterns = [
    path('', views.PublicLinkListView.as_view(), name='index'),
    path('link/new/', views.LinkCreateView.as_view(), name='link_new'),
    re_path(r'authors/(?P<mvp_id>\d{7})/$', views.LinkListView.as_view(), name='link_list_per_author'),
]
