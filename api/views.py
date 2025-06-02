from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Comment
from .serializers import CommentSerializer

User = get_user_model()

# Create your views here.

# Permitir acesso sem autenticação para todas as views
class CommentListCreateView(generics.ListCreateAPIView):
    """
    GET: Lista todos os comentários
    POST: Cria um novo comentário
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]  # Sem autenticação necessária
    
    def perform_create(self, serializer):
        """Lógica customizada para criação de comentários"""
        # Verificar se foi enviado um user_id no request
        user_id = self.request.data.get('user_id')
        user = None
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass  # Usuário não encontrado, continua sem usuário
                
        serializer.save(user=user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retorna um comentário específico
    PUT/PATCH: Atualiza um comentário
    DELETE: Remove um comentário
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]  # Sem autenticação necessária

@api_view(['GET'])
@permission_classes([AllowAny])
def comment_stats(request):
    """Endpoint para estatísticas dos comentários"""
    total_comments = Comment.objects.count()
    comments_with_users = Comment.objects.filter(user__isnull=False).count()
    comments_without_users = Comment.objects.filter(user__isnull=True).count()
    
    return Response({
        'total_comments': total_comments,
        'comments_with_users': comments_with_users,
        'comments_without_users': comments_without_users,
        'percentage_with_users': round((comments_with_users / total_comments * 100), 2) if total_comments > 0 else 0
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def user_comments(request, user_id):
    """Lista todos os comentários de um usuário específico"""
    try:
        user = User.objects.get(id=user_id)
        comments = Comment.objects.filter(user=user)
        serializer = CommentSerializer(comments, many=True)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'comments': serializer.data,
            'total': comments.count()
        })
    except User.DoesNotExist:
        return Response(
            {'error': 'Usuário não encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
