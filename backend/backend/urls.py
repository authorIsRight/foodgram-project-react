from django.conf import settings
# удалить после развертывния в конейтнерах
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
]

# удалить после развертывния в конейтнерах
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
