import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    """
    Modelo de usúario personalizado que utiliza UUID como chave primária.
    Substitui o ID sequencial padrão por um identificador único universal.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True)


    def save(self, *args, **kwargs):
        # normalização de lowercase do email antes de salvar
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    

class UserProfile(models.Model):
    """
    Armazena informações complementares do perfil do usuário
    Implementaa lógica de gamificação (Streaks) e metas diárias
    """

    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )
    bio = models.TextField(max_length=500, blank=True)
    daily_goal_minutes = models.PositiveBigIntegerField(default=0)
    current_streak = models.PositiveBigIntegerField(default=0)
    longest_streak = models.PositiveBigIntegerField(default=0)
    # Meta diaria de minutos, sequencia atual de dias cumpridos por meta e  maior sequencia ja atingida 
    # PositiveBigIntegerField vai garantir que só aceita numeros positivos e suporta valores grandes


    def __str__(self):
        return f"Perfil de {self.user.username}"

