from django import forms
from apps.core.models import Subject


tailwindInput = ("w-full px-4 py-2 rounded-lg border border-gray-300 "
                  "focus:outline-none focus:ring-2 focus:ring-indigo-500")

colorInputStyle  = "w-16 h-10 rounded cursor-pointer border border-gray-300"

class SubjectForm(forms.ModelForm):
    # criação e edição das disciplinas pelo formularios

    class Meta:
        model = Subject
        fields = ["name", "color_hex", "icon"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Digite o nome da disciplina",
                "class": tailwindInput,
            }),
            "color_hex": forms.TextInput(attrs={
                "type": "color", 
                "class": colorInputStyle
            }),
            "icon": forms.TextInput(attrs={
                "placeholder": "Ex: 📚",
                "class": tailwindInput
            })
        }

class PomodoroConfigForm(forms.Form):
    # configuração do pomodoro pelo formulario

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        required=False,
        label ="Disciplina (opcional)", 
        empty_label="- Nehuma Disciplina -",
        widget=forms.NumberInput(attrs={"class": tailwindInput}),

    )
    breakDurationMin = forms.IntegerField(min_value=1, max_value=60, initial= 5, label="Tempo de pausa (minutos)", widget=forms.NumberInput(attrs={"clas": tailwindInput}))    

    def __init__(self,*args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["subject"].queryset = Subject.objects.filter(user=user)