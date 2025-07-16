"""
URL configuration for airport_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import airport_backend.urls
import user.urls
import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/airport/", include(airport_backend.urls), name="airport"),
    path("api/user/", include(user.urls), name="user"),
    path('__debug__/', include(debug_toolbar.urls)),
]
