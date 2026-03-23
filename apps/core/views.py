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

        context = {"sessionsRecent": sessionsRecent, "subjects": subjects, "profile": profile, "today": today, "total_sessions": StudySession.objects.filter(user=user).count(), "completed_today": StudySession.object.filter(user=user, scheduled_date=today, status=StudySession.Status.COMPLETED).count(),}
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
    



    
