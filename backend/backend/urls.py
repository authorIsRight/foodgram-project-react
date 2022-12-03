from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    path('admin/', admin.site.urls),
#тз    path('api/', include('api.urls', namespace='api')),
)