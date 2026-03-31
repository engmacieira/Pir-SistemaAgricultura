# PIR - Sistema de Vendas de Produtores Rurais (AgroLocal)
**Documento de Visão e Arquitetura - Versão 2.0 (Stack React + FastAPI)**

## 1. Visão do Produto
O PIR é uma plataforma digital projetada para conectar produtores rurais locais (agricultura familiar) diretamente a consumidores finais, otimizando o processo de venda, catálogo, pedidos e pagamentos em um formato semelhante a aplicativos de delivery, mas com foco no fortalecimento do comércio local e na rastreabilidade.

## 2. Stack Tecnológico
* **Frontend (Apresentação):** React (SPA) moderno, consumindo APIs REST.
* **Backend (API e Domínio):** Python 3.10+ com FastAPI.
* **Banco de Dados:** PostgreSQL (Relacional).
* **ORM e Migrações:** SQLAlchemy + Alembic.
* **Padrão Arquitetural:** Domain-Driven Design (DDD) com separação estrita em 4 camadas (`domain`, `application`, `infrastructure`, `presentation`).

## 3. Mapa de Domínios e Bounded Contexts (DDD)
Para mantermos a totalidade do escopo legado de forma organizada, o sistema é dividido nos seguintes Bounded Contexts:

1. **Contexto de Identidade e Acesso (IAM):**
   * *Entidades:* User, Address, Audit.
   * *Responsabilidade:* Autenticação, autorização, gestão de perfis e auditoria de ações críticas.
2. **Contexto de Produtores (Core Domain):**
   * *Entidades:* ProducerProfile.
   * *Responsabilidade:* Gestão de dados específicos do produtor rural, certificações e capacidade de entrega.
3. **Contexto de Catálogo e Ofertas:**
   * *Entidades:* Catalog, Product, ProducerProduct, Offer.
   * *Responsabilidade:* Vitrine de produtos, gestão de estoque, sazonalidade agrícola e preços.
4. **Contexto de Pedidos (Orders):**
   * *Entidades:* Order, Checkout.
   * *Responsabilidade:* Ciclo de vida da compra, carrinho, logística de busca/entrega e status do pedido.
5. **Contexto Financeiro (Billing):**
   * *Entidades:* Transaction, Payout.
   * *Responsabilidade:* Registro de pagamentos, repasses financeiros para o produtor (payouts) e extratos.
6. **Contexto de Relacionamento:**
   * *Entidades:* Communication, Review.
   * *Responsabilidade:* Avaliações de produtos/produtores e troca de mensagens (notificações).

## 4. Regras Arquiteturais Inquebráveis
* O Domínio (`/domain`) é agnóstico. Nenhuma biblioteca externa (como FastAPI ou SQLAlchemy) deve ditar como as Entidades e Interfaces de Repositório são escritas.
* O fluxo de dependência é sempre de fora para dentro: `Presentation` -> `Application` -> `Domain` <- `Infrastructure`.