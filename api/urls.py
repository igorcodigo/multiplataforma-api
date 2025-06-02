from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Endpoints principais dos comentários
    path('comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    
    # Endpoints adicionais
    path('comments/stats/', views.comment_stats, name='comment-stats'),
    path('users/<int:user_id>/comments/', views.user_comments, name='user-comments'),
]
