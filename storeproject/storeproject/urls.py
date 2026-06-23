from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Default Django admin (optional)
    path('admin/', admin.site.urls),

    # User website
    path('', include('storeapp.urls')),

    # Custom admin panel
    path('admin-panel/', include('adminpanel.urls')),
]

# Static and media files (development only)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)