from django.urls import path, include
from .views import RegisterView, VerifyEmailView, ResetPasswordView, LoginView, AdminLoginView, GenerarGanadorView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin-login/', AdminLoginView.as_view(), name='admin-login'),
    path('generar-ganador/', GenerarGanadorView.as_view(), name='generar_ganador'),


    # path('/auth/', include('rest_framework.urls')),  # Ruta correcta de autenticación
]
