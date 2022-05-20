"""tests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

# import debug_toolbar

from app.views import *
from app.paginator_views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('__debug__/', include(debug_toolbar.urls)),
    
    path('', index),
    path('important', important),
    path('viewed', viewed),
    path('latest', latest),
    path('search', search),
    path('news/<int:pk>', news),                     # BEGIN
    path('news/<int:pk>/<str:title>', news),
    path('category/<int:pk>', category),
    path('category/<int:pk>/<str:title>', category), # END
    path('go/<int:pk>', go),

    path('paginator/index', paginator_index),
    path('paginator/important', paginator_important),
    path('paginator/viewed', paginator_viewed),
    path('paginator/latest', paginator_latest),
    path('paginator/search', paginator_search),
    path('paginator/category', paginator_category),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
