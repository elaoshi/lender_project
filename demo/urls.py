"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from demo.settings import MEDIA_ROOT, MEDIA_URL
from lenders.views import LenderView, LenderDetailView
from lenders.views.lenderDumps import LenderDumpView
from lenders.views.lenderUpload import LenderUploadView

schema_view = get_schema_view(
   openapi.Info(
      title="Eric API",
      default_version='v1',
      description="Eric API"
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('lender',LenderView.as_view(), name='lender-list'),
    path('lender/<int:pk>', LenderDetailView.as_view(), name='lender-detail'),
    path('lender/dump',LenderDumpView.as_view(), name='lender-dump'),
    path('lender/upload',LenderUploadView.as_view(), name='lender-bulk-upload'),

    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
