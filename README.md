# OrganizaStudy 
> Plataforma de produtividade acadêmica para centralização e gestão inteligente de estudos.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

---

##  Sobre o Projeto
O **organizaEstudy** foi desenvolvido para resolver o caos da organização acadêmica. O foco é reduzir a "fadiga de decisão" do estudante, integrando cronograma, execução (Pomodoro) e registro de conhecimento em um único ecossistema.

### Principais Diferenciais:
* **Fluxo Unificado:** Do planejamento à métrica de desempenho.
* **Base de Conhecimento:** Suporte nativo a Markdown para anotações rápidas e estruturadas.
* **Gamificação Leve:** Sistema de *streaks* para manter a constância.

---

## Arquitetura e Tecnologias
O projeto segue as práticas de desenvolvimento Django, com foco em **escalabilidade** e **manutenibilidade**.

* **Backend:** Python 3 + Django (Arquitetura baseada em Apps independentes).
* **Database:** PostgreSQL (Produção) / SQLite (Desenvolvimento).
* **Frontend:** Django Templates + JavaScript Vanilla.
* **Infra:** Docker & Docker Compose para padronização de ambiente.

### Estrutura de Pastas (Padrão Enterprise)

organizaEstudy/
├── apps/               # Aplicações de negócio (Users, Tasks, Core, Analytics)
├── config/             # Configurações do Django (Settings modulares)
├── shared/             # Mixins, validadores e utilitários globais
├── templates/          # Interface do usuário
└── static/             # Assets (CSS/JS/Images)



<<<<<<< HEAD

=======
>>>>>>> 168c050 (feat: add core/models and readjust gitignore and readme.md)
