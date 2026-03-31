# 💸 Dívidas Técnicas e Melhorias - PIR (AgroLocal)

**Status Geral:** Sob Controle (Fase Inicial)

> "Código bom é código que evolui. Se deixamos algo para trás, registramos aqui para não esquecer."

---

## 🚨 Crítico (Prioridade Alta)
*Coisas que funcionam "por milagre", riscos de segurança ou bugs conhecidos.*

* **[Autenticação / IAM]** Segredo do JWT (Secret Key) exposto no código.
    * *Causa:* Chave hardcoded temporária em `app/application/use_cases/authenticate_user.py` para validar o fluxo inicial.
    * *Solução Proposta:* Extrair `SECRET_KEY`, `ALGORITHM` e `ACCESS_TOKEN_EXPIRE_MINUTES` para um arquivo `settings.py` usando `pydantic-settings`, lendo diretamente das variáveis de ambiente (`.env`).

## ⚠️ Atenção (Prioridade Média)
*Funcionalidades incompletas, validações fracas ou performance ruim.*

* **[Infraestrutura / IAM]** Implementações de Repositório Pendentes (Mockadas).
    * *Causa:* Focamos na construção da Camada de Aplicação e Apresentação, mas os arquivos `AddressRepositoryImpl` e `AuditRepositoryImpl` não foram escritos.
    * *Solução Proposta:* Implementar as classes reais usando o SQLAlchemy no diretório `app/infrastructure/repositories/`.

* **[Aplicação / IAM]** Ausência de Controle Transacional Completo nos Use Cases.
    * *Causa:* No registro de usuário, o *User* e o *AuditLog* estão sendo salvos de forma independente. Se a gravação da auditoria falhar, o usuário já terá sido persistido no banco de dados.
    * *Solução Proposta:* Adicionar suporte a *Unit of Work* ou repassar o bloco transacional (commit/rollback) garantindo atomicidade entre a entidade de domínio principal e seus side-effects (como logs de auditoria).

## 🔧 Refatoração (Melhoria de Código)
*Código que funciona, mas está feio, repetitivo ou difícil de ler (Code Smell).*

* *(Nenhuma refatoração estrutural necessária no momento. Arquitetura DDD está limpa).*

## 🧪 Testes e Cobertura
*Áreas que estão sem cobertura de testes automatizados.*

* [ ] Criar testes unitários para a Camada de Domínio (`app/domain/entities`).
* [ ] Criar testes de integração para as rotas de Registro e Login no pacote `app/tests/`.

---

### 📝 Histórico de Pagamentos (Resolvidos)
*Mova para cá o que for resolvido, para termos o registro da evolução.*

* *(Nenhuma dívida paga ainda).*