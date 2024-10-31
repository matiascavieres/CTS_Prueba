from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import redirect
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserSerializer
from .tasks import enviar_correo_verificacion, enviar_ganador_por_correo
import uuid

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Desactivar hasta verificar
            user.verification_token = uuid.uuid4()  # Generar token
            user.save()

            # Enviar correo de verificación como tarea asincrónica
            enviar_correo_verificacion.delay(user.email, str(user.verification_token))
            return Response(
                {'message': 'Registro exitoso. Revisa tu correo para activarlo.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request, token):
        user = User.objects.filter(verification_token=token).first()
        if user:
            user.is_active = True
            user.save()
            return redirect(f'http://localhost:8080/reset-password/{token}/')
        return Response({'error': 'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, token):
        user = User.objects.filter(verification_token=token).first()
        if not user:
            return Response({'error': 'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        if password:
            user.set_password(password)
            user.verification_token = None  # Invalidar token
            user.save()
            return Response({'message': '¡Contraseña actualizada exitosamente!'}, status=status.HTTP_200_OK)

        return Response({'error': 'Debe proporcionar una contraseña.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                return Response({"error": "Usuario no activo, verifica tu correo"}, status=403)

            return Response(
                {"message": "Login exitoso", "is_staff": user.is_staff},
                status=200
            )
        return Response({"error": "Credenciales inválidas"}, status=401)


class GenerarGanadorView(APIView):
    def get(self, request):
        # Ejecutar la tarea asincrónica para seleccionar un ganador
        enviar_ganador_por_correo.delay()
        return Response(
            {"message": "El sorteo está en proceso. Pronto se enviará el correo al ganador."},
            status=200
        )

class AdminLoginView(APIView):
    def post(self, request):
        print("Print del request data:", request.data)
        username = request.data.get('username')
        password = request.data.get('password')

        # Autenticar al usuario con username y password
        user = authenticate(username=username, password=password)

        if user is not None:
            # Verificar si es un usuario administrador (staff)
            if user.is_staff:
                return Response(
                    {"message": "Bienvenido, administrador", "is_staff": True},
                    status=200
                )
            else:
                # Responder si es un usuario normal
                return Response(
                    {"message": "Login exitoso", "is_staff": False},
                    status=200
                )

        return Response(
            {"error": "Credenciales inválidas"},
            status=401
        )    

# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from .serializers import UserSerializer
# from .tasks import enviar_correo_verificacion
# import uuid
# from django.contrib.auth import get_user_model, authenticate
# from django.shortcuts import get_object_or_404
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from django.shortcuts import redirect
# import uuid
# from .models import CustomUser


# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             user.is_active = False  # Desactivar cuenta hasta que se verifique
#             user.verification_token = uuid.uuid4()  # Generar un token de verificación
#             user.save()

#             enviar_correo_verificacion.delay(user.email, str(user.verification_token))
#             return Response({'message': 'Registro exitoso. Revisa tu correo para activarlo.'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User = get_user_model()

# class VerifyEmailView(APIView):
#     def get(self, request, token):
#         user = User.objects.filter(verification_token=token).first()
#         if user:
#             user.is_active = True
#             user.save()
#             # Redirige al frontend para actualizar la contraseña
#             return redirect(f'http://localhost:8080/reset-password/{token}/')
#         return Response({'error': 'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)
    
# class ResetPasswordView(APIView):
#     def post(self, request, token):
#         user = User.objects.filter(verification_token=token).first()
#         if not user:
#             return Response({'error': 'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)

#         password = request.data.get('password')
#         if password:
#             user.set_password(password)
#             user.verification_token = None  # Invalida el token
#             user.save()
#             return Response({'message': '¡Contraseña actualizada exitosamente!'}, status=status.HTTP_200_OK)

#         return Response({'error': 'Debe proporcionar una contraseña.'}, status=status.HTTP_400_BAD_REQUEST)
    
# class LoginView(APIView):
#     def post(self, request):
#         print("Print del request data:", request.data)
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Autenticar al usuario con username y password
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             if not user.is_active:
#                 return Response(
#                     {"error": "Usuario no activo, verifica tu correo"},
#                     status=403
#                 )

#             # Verificar si es un usuario administrador (staff)
#             if user.is_staff:
#                 return Response(
#                     {"message": "Bienvenido, administrador", "is_staff": True},
#                     status=200
#                 )
#             else:
#                 # Responder si es un usuario normal
#                 return Response(
#                     {"message": "Login exitoso", "is_staff": False},
#                     status=200
#                 )

#         return Response(
#             {"error": "Credenciales inválidas"},
#             status=401
#         )    
