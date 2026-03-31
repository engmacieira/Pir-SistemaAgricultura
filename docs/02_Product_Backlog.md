# PIR - Product Backlog e Definição de Tarefas

Este documento mapeia todas as tarefas necessárias para a reconstrução do sistema PIR (React + FastAPI), divididas por Épicos (Bouded Contexts do DDD).

## 🚀 ÉPICO 1: Setup Base e Contexto IAM (Identidade e Acesso)
**Objetivo:** Levantar a fundação do projeto e garantir que usuários possam se registrar e autenticar.

* [X] **Tarefa 1.1 - Setup do Repositório (Antigravity):** Inicializar o projeto React (Vite) e a estrutura de pastas do FastAPI seguindo o DDD. Configurar o Docker base e variáveis de ambiente.
* [ ] **Tarefa 1.2 - Modelagem de Dados IAM (Nexus):** Criar as entidades `User`, `Address` e `Audit` no SQLAlchemy e gerar a migration inicial no Alembic.
* [ ] **Tarefa 1.3 - API de Autenticação (Programador):** Implementar os Use Cases e rotas (Endpoints) de Login (JWT), Registro de Usuário e Gestão de Endereços.
* [ ] **Tarefa 1.4 - UI/UX Autenticação (Pixel + Programador):** Desenhar e implementar as telas de Login e Cadastro no React, integrando com a API.
* [ ] **Tarefa 1.5 - Testes e Segurança IAM (Jules):** Escrever testes unitários para o domínio de usuários e garantir que os tokens JWT estão seguros.

## 🧑‍🌾 ÉPICO 2: Core Domain - Gestão de Produtores
**Objetivo:** Permitir que o produtor rural configure seu perfil, certificações e regras de negócio.

* [ ] **Tarefa 2.1 - Modelagem de Produtores (Nexus):** Criar entidade `ProducerProfile` e relacionamentos com `User`.
* [ ] **Tarefa 2.2 - API do Produtor (Programador):** Endpoints para CRUD do perfil do produtor (nome da fazenda, certificações orgânicas, etc.).
* [ ] **Tarefa 2.3 - UI Dashboard do Produtor (Pixel + Programador):** Criar o painel inicial do produtor no React.

## 📦 ÉPICO 3: Catálogo e Ofertas
**Objetivo:** Vitrine de produtos, gestão de estoque e sazonalidade agrícola.

* [ ] **Tarefa 3.1 - Modelagem do Catálogo (Nexus):** Criar `Catalog`, `Product`, `ProducerProduct` e `Offer`.
* [ ] **Tarefa 3.2 - API de Produtos (Programador):** Lógica de criação de produtos, controle de estoque (Inventory) e aplicação de preços sazonais.
* [ ] **Tarefa 3.3 - UI da Vitrine (Pixel + Programador):** Telas de listagem de produtos para o consumidor e tela de gestão de estoque para o produtor.

## 🛒 ÉPICO 4: Pedidos (Orders) e Logística
**Objetivo:** Ciclo de vida da compra, carrinho e status do pedido.

* [ ] **Tarefa 4.1 - Modelagem de Pedidos (Nexus):** Criar as tabelas `Order` e `Checkout`.
* [ ] **Tarefa 4.2 - Máquina de Estados do Pedido (Programador):** Implementar o fluxo do pedido (Pendente -> Confirmado -> Em Preparo -> Entregue) garantindo as regras de negócio no domínio.
* [ ] **Tarefa 4.3 - UI do Carrinho e Checkout (Pixel + Programador):** Fluxo de compra no frontend React.

## 💳 ÉPICO 5: Financeiro (Billing)
**Objetivo:** Registro de pagamentos e repasses (Payouts).

* [ ] **Tarefa 5.1 - Modelagem Financeira (Nexus):** Criar `Transaction` e `Payout`.
* [ ] **Tarefa 5.2 - API de Transações (Programador):** Lógica de divisão de valores (split) e registro de recebíveis.

## 💬 ÉPICO 6: Relacionamento
**Objetivo:** Avaliações e comunicação.

* [ ] **Tarefa 6.1 - Modelagem de Avaliações (Nexus):** Criar `Review` e `Communication`.
* [ ] **Tarefa 6.2 - API de Notificações e Reviews (Programador):** Endpoints para dar nota ao produtor e histórico de mensagens.