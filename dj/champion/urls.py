from django.urls import path, re_path
from . import views

app_name = 'champion'

urlpatterns = [
    path('', views.PublicLinkListView.as_view(), name='index'),
    path('<int:pk>/', views.LinkDetailView.as_view(), name='link_detail'),
    path('link/new/', views.LinkCreateView.as_view(), name='link_new'),
    path('link/<int:pk>/edit/', views.LinkUpdateView.as_view(), name='link_edit'),
    path('link/<int:pk>/delete/', views.LinkDeleteView.as_view(), name='link_delete'),
    re_path(r'authors/(?P<mvp_id>\d{7})/$', views.LinkListView.as_view(), name='link_list_per_author'),
]
