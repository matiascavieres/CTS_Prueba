from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta del admin
    path('api/users/', include('users.urls')),  # API de usuarios
    path('api/auth/', include('rest_framework.urls')),  # Ruta para autenticación con DRF
]
