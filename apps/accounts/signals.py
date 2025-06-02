from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Normalizar nome de usuário para minúsculas
@receiver(pre_save, sender=User)
def normalize_username(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()
