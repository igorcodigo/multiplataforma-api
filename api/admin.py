from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Campos a serem exibidos na lista
    list_display = ['full_name', 'email', 'comment_preview', 'created_at', 'user']
    
    # Filtros laterais
    list_filter = ['created_at', 'user']
    
    # Campos de busca
    search_fields = ['full_name', 'email', 'comment']
    
    # Campos somente leitura
    readonly_fields = ['created_at', 'updated_at']
    
    # Ordenação padrão
    ordering = ['-created_at']
    
    # Campos no formulário de edição
    fieldsets = (
        ('Informações do Comentário', {
            'fields': ('comment', 'full_name', 'email')
        }),
        ('Usuário Associado', {
            'fields': ('user',),
            'classes': ('collapse',),
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Personalizar o preview do comentário
    def comment_preview(self, obj):
        return obj.comment[:100] + "..." if len(obj.comment) > 100 else obj.comment
    comment_preview.short_description = "Comentário (Preview)"
    
    # Exibir quantos comentários há no total
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            response.context_data['title'] = f'Comentários ({Comment.objects.count()} total)'
        return response
