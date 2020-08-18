# from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('champion/', include('champion.urls')),
    path('', RedirectView.as_view(pattern_name='champion:index')),
]
