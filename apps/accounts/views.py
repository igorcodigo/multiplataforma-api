from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes, action
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
import random
import datetime
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .serializers import (
    CustomUserSerializer, 
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    PublicUserSerializer
)
from .models import CustomUser, PasswordResetCode

# Importar as funções de envio de email
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from email_service.password_reset import send_password_reset_email
from email_service.welcome_email import send_welcome_email

# Serializer personalizado para TokenObtainPair que permite login com e-mail
class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Extrair credenciais
        username = attrs.get('username')
        password = attrs.get('password')
        
        # Tentar autenticar com e-mail ou username
        UserModel = get_user_model()
        try:
            user = None
            # Verificar se é um e-mail
            if '@' in username:
                user = UserModel.objects.filter(email=username).first()
            else:
                user = UserModel.objects.filter(username=username).first()
            
            if user and user.check_password(password):
                # Se autenticado com sucesso, substituir o username para que o processo padrão funcione
                attrs['username'] = user.username
        except UserModel.DoesNotExist:
            pass
            
        # Continuar com a validação padrão
        return super().validate(attrs)

# View personalizada para TokenObtainPair que permite login com e-mail
class EmailOrUsernameTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailOrUsernameTokenObtainPairSerializer

#View para criar usuario com API REST usando Django rest framework
class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        # Enviar email de boas-vindas
        try:
            # Enviar email de boas-vindas
            send_welcome_email(
                email=user.email,
                name=user.first_name or "🥳",
            )
        except Exception as e:
            # Apenas registrar o erro, não impedir a criação do usuário
            print(f"Erro ao enviar email de boas-vindas: {str(e)}")

# Função para gerar código de 6 dígitos
def generate_reset_code():
    return ''.join(random.choices('0123456789', k=6))

# View para solicitar redefinição de senha
class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_user_model().objects.get(email=email)
            
            # Gerar código de 6 dígitos para redefinição
            reset_code = generate_reset_code()
            
            # Definir expiração para 24 horas
            expiry_time = timezone.now() + datetime.timedelta(hours=24)
            
            # Criar novo registro de código de reset
            PasswordResetCode.objects.create(
                user=user,
                email=email,
                code=reset_code,
                expires_at=expiry_time
            )
            
            # Construir a URL de redefinição
            frontend_url = getattr(settings, 'FRONTEND_URL', request.build_absolute_uri('/')[:-1])
            # Atualizar para usar o novo caminho com código
            reset_url = f"{frontend_url}/contas/reset-password/?email={email}&code={reset_code}"
            
            # Enviar email
            try:
                send_password_reset_email(email, reset_url)
                return Response(
                    {"detail": "Email de redefinição de senha enviado com sucesso."},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"detail": f"Erro ao enviar email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View para confirmar redefinição de senha
@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer
    authentication_classes = []  # Desativa a autenticação para este endpoint

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Senha redefinida com sucesso."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save()
        try:
            send_welcome_email(
                email=user.email,
                name=user.first_name or "🥳",
            )
        except Exception as e:
            print(f"Erro ao enviar email de boas-vindas: {str(e)}")

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

# Serializer for UserLoginView
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# View for user login and returning user ID
@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return Response({'user_id': user.id}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to get user details by ID
class UserDetailsView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,) # Or AllowAny, depending on requirements
    lookup_field = 'pk' # 'pk' is the default, but explicit is good

# View for User Registration
@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        # Optionally, send a welcome email here
        # try:
        #     send_welcome_email(
        #         email=user.email,
        #         name=user.full_name or user.username or "🥳",
        #     )
        # except Exception as e:
        #     print(f"Erro ao enviar email de boas-vindas: {str(e)}")

class PublicUserDetailsView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'pk'
