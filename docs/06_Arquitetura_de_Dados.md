# 🏛️ Arquitetura e Regras de Dados (AgroLocal)
**Autor:** Nexus (Arquiteto de Dados / DBA)
**Contexto:** Bounded Contexts, Domain-Driven Design (DDD), SQLAlchemy e PostgreSQL.

Este documento define as regras inegociáveis para a modelagem, manipulação e persistência de dados no projeto AgroLocal. Qualquer nova entidade, tabela ou repositório deve seguir estritamente estas diretrizes.

---

## 1. Princípio de Separação de Camadas (DDD)
A Regra de Ouro: **O Domínio dita as regras, a Infraestrutura obedece.**
* **Camada de Domínio (`app/domain/entities/`):** Deve ser escrita em Python puro (`dataclasses`). **NÃO PODE** conter importações do SQLAlchemy, FastAPI ou qualquer outro framework de I/O.
* **Camada de Infraestrutura (`app/infrastructure/models/`):** É aqui que o SQLAlchemy vive. Os modelos são mapas exatos das tabelas do banco de dados e não contêm regras de negócio.
* **Repositórios:** O Domínio define *o que* precisa ser feito (Interfaces/ABCs em `domain/repositories/`). A Infraestrutura define *como* fazer (Implementações com Session do banco em `infrastructure/repositories/`). A camada de serviço nunca manipula modelos de banco, apenas Entidades de Domínio.

---

## 2. Princípio DRY (Don't Repeat Yourself) e Herança Base
Antes de criar qualquer arquivo novo, **verifique os arquivos base do sistema**. Não reescreva código de infraestrutura.

### Entidades de Domínio
* Toda entidade comum deve herdar de `AuditableEntity` (em `app/domain/entities/base_entity.py`).
* Isso injeta automaticamente: `id` (UUID), `created_at`, `updated_at` e `deleted_at`, além dos comportamentos de mutação de data e exclusão lógica.

### Modelos de Banco de Dados (SQLAlchemy)
* Todo modelo deve herdar de `Base` (em `app/core/database.py`).
* Se a tabela precisar de rastreio de tempo, herde de `TimestampMixin`.
* Se a tabela permitir exclusão, herde de `SoftDeleteMixin`.
* **Exceção (Tabelas Imutáveis):** Tabelas de logs (ex: Auditoria) e Eventos (Event Sourcing) são *Append-Only* (apenas inserção). Elas **não** herdam mixins de atualização ou deleção.

### Repositórios
* Todo repositório padrão deve herdar da interface genérica `IBaseRepository` no Domínio e implementar `BaseRepositoryImpl` na Infraestrutura.
* O `BaseRepositoryImpl` já possui os métodos genéricos de CRUD (`save`, `get_by_id`, `update`). Desenvolva apenas consultas exclusivas (ex: `get_by_email`).

---

## 3. Padrão de Exclusão: Soft Delete (Exclusão Lógica)
Nenhum dado relacional de negócio deve ser apagado fisicamente (Hard Delete) para garantir integridade e auditoria (LGPD).
* **Camada de Banco:** Utilizamos a coluna `deleted_at` (Timestamp). Se for NULO, o registro está ativo.
* **Camada de Repositório:** A implementação genérica (`BaseRepositoryImpl`) já adiciona automaticamente a cláusula `.filter(Model.deleted_at.is_(None))` em buscas por ID ou Updates. **Qualquer busca customizada deve incluir este filtro obrigatoriamente.**
* Para as camadas superiores da aplicação, um registro com Soft Delete deve ser tratado como "Não Encontrado" (404).

---

## 4. Documentação Ativa e Tipagem Rigorosa (Clean Code)
O código é o dicionário de dados do sistema.
* **Docstrings:** Toda Classe e Método complexo deve ter um comentário explicando a sua intenção de negócio.
* **Tipagem (Type Hints):** É obrigatório o uso de tipagem em todas as variáveis, argumentos de função e retornos (ex: `def get_user(id: UUID) -> Optional[User]:`).
* **Documentação de Colunas (SQLAlchemy):** Toda a coluna definida nos modelos de infraestrutura deve preencher o parâmetro `doc="..."`. Isso serve para facilitar a manutenção de DBA e geração de metadados.
  * *Exemplo Correto:* `email = Column(String, doc="Endereço de e-mail do usuário para login.")`

---

## 5. Migrações e Versionamento de Schema (Alembic)
* Nenhuma alteração manual é feita na base de dados de produção ou desenvolvimento.
* Para cada nova entidade ou alteração de coluna:
  1. Crie/Edite os modelos Python (`infrastructure/models/`).
  2. Garanta que o modelo está a ser importado no ficheiro `alembic/env.py`.
  3. Gere o script de migração: `alembic revision --autogenerate -m "Sua mensagem"`
  4. **REVISÃO OBRIGATÓRIA:** Leia o arquivo gerado em `alembic/versions/` para verificar inconsistências em Enums, JSONs ou deleções acidentais antes de aplicar.
  5. Aplique a migração: `alembic upgrade head`