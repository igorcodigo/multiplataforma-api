from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import (
    PasswordResetRequestView, 
    PasswordResetConfirmView, 
    EmailOrUsernameTokenObtainPairView,
    UserViewSet,
    UserLoginView,
    UserDetailsView,
    UserRegistrationView
)
from .forms import EmailOrUsernameAuthenticationForm

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/token/', EmailOrUsernameTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Autenticação tradicional baseada em sessão do Django com formulário personalizado
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        authentication_form=EmailOrUsernameAuthenticationForm
    ), name='login'),
    # API endpoints
    path('api/', include(router.urls)),
    
    # Endpoints para redefinição de senha
    path('api/password/reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Endpoint for user login
    path('api/login/', UserLoginView.as_view(), name='user_login'),

    # Endpoint to get user details by ID
    path('api/users/<int:pk>/', UserDetailsView.as_view(), name='user_details'),

    # Endpoint for user registration
    path('api/register/', UserRegistrationView.as_view(), name='user_register'),
    
    # Template para redefinição de senha (agora usando query parameters)
    path('reset-password/', 
         TemplateView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm_page'),
]
