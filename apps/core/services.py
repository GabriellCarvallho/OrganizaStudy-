
from datetime import timedelta
from django.utils import timezone
from django.db import transaction

from apps.core.models import Subject, StudySession, PomodoroSession
from apps.analytics.models import StreakRecord



class SubjectService:

    @staticmethod
    def create_subject(user, name: str, color_hex: str = "#6366F1", icon: str = "📚") -> Subject:
        # coloquei isso pra evitar problemas de nome vazio, cor invalida ou icon grandes
        if not name.strip():
            raise ValueError("Name cannot be empty") 
        if Subject.objects.filter(user=user,name=name).exists():
            raise ValueError("Subject already exists")
        
        with transaction.atomic():
            return Subject.objects.create(user=user, name=name, color_hex=color_hex, icon=icon)
    
    @staticmethod
    def update_subject(subject: Subject, **fields) -> Subject:
        for attr, value in fields.items():
            setattr(subject, attr, value)
        
        subject.save()
        return subject

    

    @staticmethod
    def delete_subject(subject: Subject) -> None:
        subject.delete()


class PomodoroService:
    
    @staticmethod
    @transaction.atomic
    def start_session(user, subject_id: int | None = None, focus_min: int = 25, break_min: int = 5,) -> tuple[StudySession, PomodoroSession]:
        session = StudySession.objects.create(user=user, subject_id=subject_id, scheduled_date=timezone.now().date(), planned_duration_min = focus_min, status = StudySession.Status.IN_PROGRESS,)
        pomodoro = PomodoroSession.objects.create(study_session = session, focus_duration_min = focus_min, break_duration_min = break_min,)
        return session, pomodoro
    
    @staticmethod
    @transaction.atomic
    def complete_pomodoro(pomodoro: PomodoroSession) -> PomodoroSession:
        now = timezone.now()
        pomodoro.ended_at = now
        pomodoro.was_completed = True
        pomodoro.save()


        session = pomodoro.study_session
        session.actual_duration_min += pomodoro.focus_duration_min
        session.status = StudySession.Status.COMPLETED
        session.save()

        StreakService.record_study(session.user, pomodoro.focus_duration_min)
        return pomodoro

    @staticmethod
    def cancel_pomodoro(pomodoro: PomodoroSession, minutes: int = 0) -> PomodoroSession:

        # pomodoro marcado como cancelado
        now = timezone.now()
        pomodoro.ended_at = now
        pomodoro.was_completed = False
        pomodoro.save()
        
        # vai retornar se o usuario nao tiver estudado nada 
        if minutes <= 0:
            return pomodoro
        
        # Se o usuario estudou parcialmente, salva progresso
        session = pomodoro.study_session
        session.actual_duration_min += minutes
        session.status = StudySession.Status.CANCELLED
        session.save()
        return pomodoro



# consistencia diaria nos estudos
class StreakService:
    @staticmethod
    def record_study(user, minutes:int) -> None:
        today = timezone.now().date()
        goal = user.userprofile.daily_goal_minutes

        record, created = StreakRecord.objects.update_or_create(user=user, date=today, defaults={
            "minutes_studied": minutes,
            "goal_achieved": minutes >= goal,
        },
    )
        
        if not created:
            record.minutes_studied += minutes
            record.goal_achieved = record.minutes_studied >= goal
            record.save()

        StreakService.__recalculate_streak(user)

    @staticmethod
    def __recalculate_streak(user) -> None:
        today = timezone.now().date()

        records = (
            StreakRecord.objects.filter(user=user, goal_achieved=True).order_by("-date")
        )

        streak = 0


        for index, record in enumerate(records):
            expected_date = today - timedelta(days=index)
            if record.date != expected_date:
                break

            streak += 1

        profile = user.userprofile
        profile.current_streak = streak
        profile.longest_streak = max(profile.longest_streak, streak)
        profile.save()


