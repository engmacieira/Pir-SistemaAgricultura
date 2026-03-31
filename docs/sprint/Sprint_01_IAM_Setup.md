# Sprint 01: Setup Base e Contexto IAM (Identidade e Acesso)

## 🎯 Objetivo da Sprint
Estabelecer a fundação do repositório (React + FastAPI) e implementar o Bounded Context de Identidade, permitindo o cadastro de usuários, autenticação via JWT e gestão de endereços.

## 📖 User Stories (Histórias de Usuário)

* **US-01: Estrutura Base (DDD & SPA)**
  * *Como* desenvolvedor, *quero* o repositório configurado com FastAPI no backend (arquitetura em 4 camadas) e React (Vite) no frontend, *para* ter um ambiente padronizado de desenvolvimento.
* **US-02: Registro de Usuário**
  * *Como* produtor ou consumidor, *quero* criar uma conta informando meus dados básicos (Nome, Email, Senha, Tipo de Perfil), *para* poder acessar a plataforma PIR.
* **US-03: Autenticação (Login)**
  * *Como* usuário registrado, *quero* fazer login com email e senha, *para* receber um Token de Acesso (JWT) e navegar em rotas seguras.
* **US-04: Gestão de Endereços**
  * *Como* usuário registrado, *quero* cadastrar e gerenciar meus endereços, *para* viabilizar futuras logísticas de entrega ou busca de produtos.

## 🏗️ Modelagem de Domínio (DDD) - Contexto IAM

**1. Entidade: `User` (Agregador Raiz)**
* *Atributos:* `id` (UUID), `email` (String, único), `hashed_password` (String), `full_name` (String), `is_active` (Booleano), `role` (Enum: ADMIN, PRODUCER, CONSUMER), `created_at`, `updated_at`.

**2. Entidade: `Address`**
* *Atributos:* `id` (UUID), `user_id` (FK), `street`, `number`, `complement`, `neighborhood`, `city`, `state`, `zip_code` (CEP), `is_default` (Booleano).

**3. Entidade: `Audit` (Para rastreabilidade de segurança)**
* *Atributos:* `id`, `user_id` (FK), `action` (String - ex: "LOGIN_SUCCESS", "PASSWORD_RESET"), `timestamp`, `ip_address`.

## 🤖 Briefing de Delegação (Vibe Coding)

**Passo 1: Setup da Infraestrutura (Agente: ANTIGRAVITY)**
* **Ação:** Criar as pastas do backend (`app/domain`, `app/application`, `app/infrastructure`, `app/presentation`). Iniciar o frontend React com Vite (`npm create vite@latest frontend -- --template react-ts`). Configurar o `.env` base e conexão com PostgreSQL.

**Passo 2: Banco de Dados e ORM (Agente: NEXUS)**
* **Ação:** Ler este documento e criar os arquivos de modelo em `app/infrastructure/models/` para `User`, `Address` e `Audit` usando SQLAlchemy. Gerar a primeira revisão do Alembic (`alembic revision --autogenerate -m "Initial IAM setup"`).

**Passo 3: Regras de Negócio e Rotas (Agente: PROGRAMADOR)**
* **Ação:** Implementar os Use Cases de registro, login (geração de JWT) e CRUD de endereços. Criar os endpoints no FastAPI (`/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/users/addresses`).

**Passo 4: Telas Iniciais (Agente: PIXEL + PROGRAMADOR)**
* **Ação:** No frontend React, construir a tela de Login (`/login`) e a tela de Cadastro (`/register`), conectando-as à API recém-criada via Axios ou Fetch API.