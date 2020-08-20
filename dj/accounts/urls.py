from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('login/', RedirectView.as_view(url='/accounts/github/login/'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
]
