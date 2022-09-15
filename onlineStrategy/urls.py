from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('', include('courses.urls')),
    path('', include('diagnostics.urls')),
    path('', include('method.urls')),
    path('', include('moderate.urls')),
    path('', include('route.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)