from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    # Personalizar a exibição do usuário (mostrar username se existir)
    user_display = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'comment',
            'email', 
            'full_name',
            'created_at',
            'updated_at',
            'user',
            'user_display'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_display']
        
    def get_user_display(self, obj):
        """Retorna informações do usuário se existir"""
        if obj.user:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
                'email': obj.user.email
            }
        return None
        
    def validate_email(self, value):
        """Validação personalizada para email"""
        if not value:
            raise serializers.ValidationError("Email é obrigatório.")
        return value.lower()
        
    def validate_comment(self, value):
        """Validação personalizada para comentário"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Comentário deve ter pelo menos 10 caracteres.")
        return value.strip()
        
    def validate_full_name(self, value):
        """Validação personalizada para nome completo"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Nome completo deve ter pelo menos 2 caracteres.")
        return value.strip().title()  # Capitaliza o nome
