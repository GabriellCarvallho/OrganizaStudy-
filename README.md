OrganizaEstudy

OrganizaEstudy é uma plataforma de produtividade acadêmica projetada para centralizar o gerenciamento completo do estudo.

O sistema integra:

planejamento de sessões de estudo

timer Pomodoro

gestão de tarefas

base de conhecimento com Markdown

dashboard de performance

O objetivo é reduzir a fricção na organização dos estudos, permitindo que o usuário foque no que realmente importa: aprender.

Visão Geral

Muitos estudantes enfrentam dificuldades com:

acúmulo de conteúdo

revisões esquecidas

falta de controle sobre o tempo estudado

organização dispersa entre aplicativos

O OrganizaEstudy resolve isso oferecendo um ambiente único que integra:

gerenciamento de disciplinas

planejamento de sessões

controle de tarefas

anotações estruturadas

métricas de desempenho

Tecnologias Utilizadas
Backend

Python

Django

PostgreSQL

Frontend

HTML

CSS

JavaScript

Django Templates

Infraestrutura

Docker

Docker Compose

Nginx

Bibliotecas principais

django

python-decouple

psycopg2

markdown

pillow


Estrutura de Pastas


organizaEstudy/
│
├── config/                 # Configuração do projeto Django
│
├── apps/
│   ├── users/              # Autenticação e perfis
│   ├── core/               # Ciclos de estudo e Pomodoro
│   ├── tasks/              # Sistema de tarefas
│   ├── knowledge/          # Base de conhecimento
│   └── analytics/          # Dashboard e métricas
│
├── shared/                 # Código reutilizável
│
├── static/                 # Arquivos estáticos
├── media/                  # Uploads do usuário
├── templates/              # Templates globais
│
├── tests/                  # Testes automatizados
├── docs/                   # Documentação técnica
│
├── requirements/
│
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── README.md



Requisitos Funcionais

ID	Descrição
RF01	Cadastro e autenticação de usuários
RF02	Perfil editável com meta diária
RF03	CRUD de disciplinas
RF04	Agendamento de sessões de estudo
RF05	Timer Pomodoro integrado
RF06	Sistema de tarefas com prioridades
RF07	Mudança de status de tarefas
RF08	Alertas de prazo
RF09	Notas com Markdown
RF10	Upload de anexos
RF11	Busca e filtros de notas
RF12	Dashboard de horas estudadas
RF13	Sistema de streaks
RF14	Indicadores de produtividade



Requisitos Não Funcionais

ID	Categoria	Descrição
RNF01	Segurança	Todas as views protegidas
RNF02	Segurança	Senhas com PBKDF2
RNF03	Qualidade	Código seguindo PEP8
RNF04	Qualidade	Lógica isolada em services
RNF05	Qualidade	Cobertura de testes ≥ 80%
RNF06	Ambiente	Configuração via .env
RNF07	Portabilidade	Settings separados
RNF08	Escalabilidade	UUID como chave primária
RNF09	Deploy	Containerização com Docker
RNF10	Documentação	README completo
RNF11	UX	Feedback com Django messages
RNF12	Performance	Uso de select_related
Decisões de Arquitetura
Services Layer


Instalação do Projeto
1. Clonar o repositório
git clone https://github.com/seuusuario/organizaEstudy.git
2. Criar ambiente virtual
python -m venv venv
3. Ativar ambiente

Linux / Mac

source venv/bin/activate

Windows

venv\Scripts\activate
4. Instalar dependências
pip install -r requirements/development.txt
5. Configurar variáveis de ambiente


7. Iniciar servidor
python manage.py runserver