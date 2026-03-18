import uuid
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MaxValueValidator


class Subject(models.Model):


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)
    color_hex = models.CharField(max_length=7,validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$')])
    icon = models.CharField(max_length=50, default="📚")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        unique_together = ["user", "name"]

    def __str__(self):
        return self.name
    


class StudySession(models.Model):
    # Aqui iremos será a sessão agendada pelo usuário


    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        IN_PROGRESS = "IN_PROGRESS", "Em andamento"
        COMPLETED = "COMPLETED", "Concluída"
        CANCELLED = "CANCELLED", "Cancelada"


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="study_sessions")
    subject = models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True, blank=True, related_name="sessions")
    scheduled_date = models.DateField(db_index=True) # data agendada
    planned_duration_min = models.PositiveIntegerField(default=25, validators=[MaxValueValidator(600)]) 
    actual_duration_min = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
        )
    
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-scheduled_date"]
        indexes = [
            models.Index(fields=["user", "scheduled_date"])
        ]
        

    def __str__(self):
        return f"{self.subject or 'Sem matéria'} - {self.scheduled_date}"
    

class PomodoroSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study_session = models.ForeignKey(StudySession, on_delete=models.CASCADE, related_name="pomodoros")
    focus_duration_min = models.PositiveIntegerField(default=25)
    break_duration_min = models.PositiveIntegerField(default=5)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    was_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-started_at"]
  

    def __str__(self):
        return f"Pomodoro {self.focus_duration_min}min — {self.started_at.date()}"
        



