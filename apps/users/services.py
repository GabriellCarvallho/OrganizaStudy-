""""
Responsavel pela logica de negocio do app users
A view apenas osquestra HTTP: regra de negocio vive aqui
"""

from django.contrib.auth import get_user_model
from apps.users.models import UserProfile
from django.db import transaction
from typing import Optional


User = get_user_model()

class UserService:
    """ Serviço central para operações relacionada ao usuário """

    @staticmethod
    def create_user(email: str, username: str, password: str) -> User:
        """
        Vamos criar um novo usuário e seu perfil associado.
        Garantir que o UserProfile é criado atomicamente com o usuário
        """
        with transaction.atomic(): 
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            UserProfile.objects.create(user=user)
            return user
    

    @staticmethod
    def update_profile(user: User, avatar: Optional[str] = None, bio:Optional[str] = None, daily_goal_minutes: Optional[int] = None) -> UserProfile:
        """
        Atualiza os dados do perfil do usuário
        Cria o perfil caso ele não exista
        """

        profile, _ = UserProfile.objects.get_or_create(user=user)

        if avatar is not None:
            profile.avatar = avatar
        
        if bio is not None:
            profile.bio = bio
        if daily_goal_minutes is not None:
            if daily_goal_minutes < 0:
                raise ValueError("daily_goal_minutes não pode ser negativo")
            profile.daily_goal_minutes = daily_goal_minutes

        profile.save()
        

        return profile
    
