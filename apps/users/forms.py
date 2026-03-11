from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

# Constante de estilo para manter o DRY (Don't Repeat Yourself)
# Facilita a manutenção: alterou aqui, muda em todo o sistema.
TW_INPUT_STYLE = (
    "w-full px-4 py-2 rounded-lg border border-gray-300 "
    "focus:outline-none focus:ring-2 focus:ring-indigo-500"
)

class RegisterForm(forms.Form):
    """Formulário de cadastro otimizado com e-mail e validação de segurança."""

    username = forms.CharField(
        max_length=150,
        label="Nome do usuário",
        widget=forms.TextInput(attrs={
            "placeholder": "Seu nome de usuário",
            "class": TW_INPUT_STYLE
        }),
    )
    
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            "placeholder": "seu@email.com",
            "class": TW_INPUT_STYLE
        }),
    )
    
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Mínimo 8 caracteres",
            "class": TW_INPUT_STYLE
        }),
    )
    
    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repita a senha",
            "class": TW_INPUT_STYLE
        }),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email").lower() # Normalização para performance de busca
        if User.objects.filter(email=email).exists():
            raise ValidationError("Esse e-mail já está cadastrado.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2:
            if p1 != p2:
                raise ValidationError("As senhas não coincidem.")
            
            validate_password(p1)
            
        return cleaned_data


class EmailAuthenticationForm(AuthenticationForm):
    """
    Override do AuthenticationForm. 
    O Django usa 'username' internamente, mas aqui o tratamos como E-mail.
    """
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            "placeholder": "seu@email.com",
            "autofocus": True,
            "autocomplete": "username",
            "class": TW_INPUT_STYLE,
        }),
    )
    
    password = forms.CharField(
        label="Senha",
        strip=False, # Importante para senhas complexas
        widget=forms.PasswordInput(attrs={
            "placeholder": "Sua senha",
            "autocomplete": "current-password",
            "class": TW_INPUT_STYLE,
        }),
    )

    def clean_username(self):
        return self.cleaned_data.get("username").lower()


class ProfileUpdateForm(forms.Form):
    
    avatar = forms.ImageField(
        required=False,
        label="Foto de perfil"
    )
    
    bio = forms.CharField(
        required=False,
        max_length=500,
        label="Bio",
        widget=forms.Textarea(attrs={
            "rows": 3,
            "placeholder": "Fale um pouco sobre você...",
            "class": TW_INPUT_STYLE,
        }),
    )

    daily_goal_minutes = forms.IntegerField(
        min_value=10,
        max_value=720,
        initial=60,
        label="Meta diária (minutos)",
        widget=forms.NumberInput(attrs={
            "class": TW_INPUT_STYLE
        }),
    )