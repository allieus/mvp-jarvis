from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path

urlpatterns = [
    path('djadmin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('champion/', include('champion.urls')),
    path('', RedirectView.as_view(pattern_name='champion:index'), name='root'),
]
