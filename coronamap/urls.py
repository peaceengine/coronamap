from django.contrib import admin
from django.urls import path, include
from statements import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),    
    path('statements/', include('statements.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)