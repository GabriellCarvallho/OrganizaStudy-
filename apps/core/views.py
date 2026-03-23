""" Orquestra dashboard, disciplinas, e o tempo do pomodoro"""


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils import timezone
from apps.core.forms import SubjectForm, PomodoroConfigForm
from apps.core.models import Subject, StudySession, PomodoroSession
from apps.core.services import SubjectService, PomodoroService



class DashBoardView(LoginRequiredMixin, View):

    """Resumo geral do usuário pelo DashBoard"""

    login_url = "/users/login/"
    template_name = "core/dashboard.html"


    def get(self, request):
        user = request.user
        today = timezone.now().date()

        # Isso aqui é uma busca otmizada para não ter que percorrer toda query do banco de dados
        sessionsRecent = StudySession.objects.filter(user=user).select_related("subject").order_by("-created_at")[:8]

        subjects = Subject.objects.filter(user=user)
        profile = user.userprofile

        context = {"sessionsRecent": sessionsRecent, "subjects": subjects, "profile": profile, "today": today, "total_sessions": StudySession.objects.filter(user=user).count(), "completed_today": StudySession.objects.filter(user=user, scheduled_date=today, status=StudySession.Status.COMPLETED).count(),}
        return render(request, self.template_name, context)
    

class SubjectListView(LoginRequiredMixin, View):
    """Crição e arrayList das disciplinas"""


    login_url = "/users/login/"
    template_name = "core/subject_list.html"


    def get(self, request):
        subjects = Subject.objects.filter(user=request.user)
        form = SubjectForm()
        return render(request, self.template_name, {"subjects": subjects, "form": form})
    

    def post(self, request):
        form = SubjectForm(request.POST)
        if form.is_valid():
            try:
                SubjectService.create_subject(user=request.user, name=form.cleaned_data["name"], color_hex=form.cleaned_data["color_hex"], icon= form.cleaned_data["icon"],)
                messages.success(request, "Matéria foi criada com sucesso!")
                return redirect("core:subject_list")

            except ValueError as e: 
                messages.error(request, "Usuário, por favor corrija os erros logo abaixo")
                subjects = Subject.objects.filter(user=request.user)
                return render(request, self.template_name, {"subjects": subjects, "form": form})
    



    
class SubjectDeleteView(LoginRequiredMixin, View):
    """Meio para excluir alguma disciplina"""
    login_url = "/users/login/"

    def post(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk, user=request.user)
        SubjectService.delete_subject(subject)
        messages.success(request, "Matéria removida")
        return redirect("core:subject_list")



class PomodoroView(LoginRequiredMixin, View):
    """ Pomodro com a configuração de tempo escolhida pelo usuario """

    login_url = "/users/login/"
    template_name = "core/pomodoro.html"

    def get(self, request):
        form = PomodoroConfigForm(user=request.user)
        return render(request, self.template_name, {"form": form})
    

    def post(self, request):
        form = PomodoroConfigForm(user=request.user, data=request.POST)
        if form.is_valid():
            study_session, pomodoro = PomodoroService.start_session(user=request.user, subject_id=form.cleaned_data["subject"].id if form.cleaned_data["subject"] else None,
            focus_duration_min=form.cleaned_data["focus_duration_min"], break_duration_min=form.cleaned_data["break_duration_min"], )
            return redirect("core:pomodoro_timer", pk=pomodoro.pk)
        
        return render(request, self.template_name, {"form": form})
    

class PomodoroCompleteView(LoginRequiredMixin, View):
    """Aqui iremos concluir um ciclo do pomodoro e atualizar o streak."""

    login_url = "/users/login/"

    def post(self, request, pk):
        pomodoro = get_object_or_404(
            PomodoroSession,
            pk=pk,
            study_session__user = request.user
        )

        PomodoroService.complete_pomodoro(pomodoro)
        messages.success(request, f"Temporizador personalizado de {pomodoro.focus_duration_min} minutos concluído")
        return redirect("core:dashboard")
    

class PomodoroTimeView(LoginRequiredMixin, View):
    """ Tela do tempo em execução para o usuario"""

    login_url = "/users/login/"

    template_name = "core/pomodoro_time.html" 

    def get(self, request, pk):
        pomodoro = get_object_or_404(
            PomodoroSession,
            pk=pk,
            study_session__user = request.user
        )  
        return render(request, self.template_name, {"pomodoro": pomodoro})
    

