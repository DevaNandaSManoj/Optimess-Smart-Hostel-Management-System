"""
URL configuration for optimess project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.core.management import call_command
from django.http import HttpResponse


def setup_db_view(request):
    try:
        call_command('migrate', interactive=False)
        call_command('loaddata', 'datadump.json')
        return HttpResponse("✅ Database Migrated and 1,464 Records Loaded Successfully!")
    except Exception as e:
        return HttpResponse(f"❌ Setup Exception: {str(e)}", status=500)


urlpatterns = [
    path('setup-db/', setup_db_view, name='setup_db'),
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('accounts.urls')),
    path('', include('food.urls')),
    path('', include('leave.urls')),
    path('warden/', include('warden.urls')),
    path('adminapp/', include('adminapp.urls')),
    path('mess_manager/', include('mess_manager.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
