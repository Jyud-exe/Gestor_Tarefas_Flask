﻿# Gestor de Tarefas

Aplicação web de gerenciamento de tarefas com autenticação de usuários.

O sistema permite que cada usuário gerencie suas próprias tarefas de forma independente, com operações completas de CRUD.

---

## Funcionalidades

- Autenticação de usuários (login/logout)
- Cadastro de novos usuários
- Criação, edição e exclusão de tarefas
- verificação de Email
- Associação de tarefas por usuário
- Persistência em banco de dados

---

## Tecnologias utilizadas

- Python
- Flask
- SQLAlchemy
- SQLite
- HTML / CSS
- Jinja2

---

## Arquitetura e organização

O projeto foi estruturado separando responsabilidades:

- **Models**: definição das entidades e relacionamento com o banco
- **Routes**: controle de fluxo da aplicação
- **Templates**: renderização das páginas com Jinja2

Esse padrão facilita manutenção e escalabilidade da aplicação.

---

## Como executar o projeto

Clone o repositório:

```bash
git clone https://github.com/Jyud-exe/Gestor_tarefas.git
cd Gestor_tarefas

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python app.py
