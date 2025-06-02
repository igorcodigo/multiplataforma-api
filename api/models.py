from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    # Campo obrigatório do comentário
    comment = models.TextField(verbose_name="Comentário")
    
    # Email obrigatório
    email = models.EmailField(verbose_name="Email")
    
    # Nome completo obrigatório
    full_name = models.CharField(max_length=200, verbose_name="Nome Completo")
    
    # Data do comentário (auto-gerada)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data do Comentário")
    
    # Usuário opcional (para usuários logados)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Usuário"
    )
    
    # Campo para rastreamento de atualizações
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-created_at']  # Comentários mais recentes primeiro
        
    def __str__(self):
        return f"{self.full_name} - {self.comment[:50]}..."
