#  osquestração de request/response
# logica de negocio delegada ao UserService


from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.utils.http import url_has_allowed_host_and_scheme # Para segurança

from apps.users.forms import RegisterForm, EmailAuthenticationForm, ProfileUpdateForm
from apps.users.services import UserService

class RegisterView(View):
    #  view de cadastro de novo usuário

    template_name = "users/register.html"


    def get(self, request):
        if request.user.is_authenticated:
            return redirect("users:profile")
        return render(request, self.template_name, {"form": RegisterForm()})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # user = UserService.create_user(**form.cleaned_data)
            user = UserService.create_user(
                email=form.cleaned_data["email"],
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
)
            login(request, user)
            messages.success(request, f"Bem vindo(a), {user.username}!")
            return redirect("core:dashboard")
        
        return render(request, self.template_name, {"form": form})
        

class LoginView(View):

    template_name = "users/login.html"

    # view de autenticação por email

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        return render(request, self.template_name, {"form": EmailAuthenticationForm()})
    
    def post(self, request):
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # segurança para valira se o next vai apontar para o proprio site
            next_url = request.GET.get("next", "users:profile")
            if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                next_url = "users:profile"
            messages.success(request, f"Bem-vindo(a) de volta, {user.username}!")
            return redirect(next_url)
        messages.error(request, "E-mail ou senha inválidos.")
        return render(request, self.template_name, {"form": form})
    


class LogoutView(View):

    # view de logout, aqui acenita apenas POST por segurança (CSRF)

    def post(self, request):
        logout(request)
        messages.info(request, "Você saiu da sua conta.")
        return redirect("users:login")
    

class ProfileView(LoginRequiredMixin, View):
    # view de visualização e edicação do perfil do usuário autenticado



    template_name = "users/profile.html"

    login_url = "/users/login/" 



    def get(self, request):
        profile = request.user.userprofile
        form = ProfileUpdateForm(initial={
            "bio": profile.bio,
            "daily_goal_minutes": profile.daily_goal_minutes,
        })
        return render(request, self.template_name, {"form": form, "profile": profile})
    
    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            UserService.update_profile(
                user=request.user,
                avatar=form.cleaned_data.get("avatar"),
                bio=form.cleaned_data.get("bio", ""),
                daily_goal_minutes=form.cleaned_data.get("daily_goal_minutes", 60),
            )
            messages.success(request, "Perfil atualizado com sucesso!")

            return redirect("users:profile")
        
        messages.error(request, "Corrija os erros abaixo")
        return render(request, self.template_name, {"form": form})





