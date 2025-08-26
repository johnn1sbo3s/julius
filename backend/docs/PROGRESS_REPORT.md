# Relatório de Progresso do Projeto FastAPI

Este documento resume o trabalho realizado até agora e os próximos passos para o desenvolvimento do backend da aplicação de controle de gastos.

---

## 1. O que fizemos até agora

### 1.1. Modelagem de Dados (backend/app/models.py)
Concluímos a criação de todos os modelos SQLAlchemy que representam as tabelas do banco de dados, seguindo a modelagem inicial:
- `User`
- `Category`
- `Expense`
- `ExpenseBudget`
- `Transaction`

Durante este processo, garantimos que os modelos estão alinhados com as melhores práticas do SQLAlchemy 2.0, incluindo:
- Uso de `Mapped` para anotações de tipo.
- Uso de `mapped_column` para definição das colunas.
- Configuração correta de relacionamentos (`relationship`).
- Tratamento de datas com `datetime.now(timezone.utc)` para timezone-awareness.
- Anotação explícita de `__tablename__: str`.

### 1.2. Configuração Básica do Banco de Dados (backend/app/database.py)
Configuramos o arquivo `database.py` para gerenciar a conexão com o banco de dados PostgreSQL. Ele é responsável por:
- Carregar credenciais do banco a partir de variáveis de ambiente (via `.env`).
- Criar o `engine` do SQLAlchemy.
- Fornecer uma fábrica de sessões (`SessionLocal`).
- Inclui uma função `get_db` para injeção de dependência de sessão no FastAPI.

### 1.3. Gerenciamento de Dependências (backend/requirements.txt)
O arquivo `requirements.txt` foi atualizado para incluir as bibliotecas essenciais para o projeto:
- `fastapi`
- `uvicorn`
- `SQLAlchemy`

(As dependências `python-dotenv` e `alembic` foram adicionadas e posteriormente removidas para resetar o ambiente conforme solicitado.)

---

## 2. Onde paramos (Próximos Passos)

Estamos com a modelagem de dados e a configuração básica de conexão com o banco prontas.

### 2.1. Criação das Tabelas no Banco de Dados
Precisamos criar as tabelas físicas no banco de dados PostgreSQL com base nos modelos SQLAlchemy definidos.
- **Opção Recomendada (Alembic):** Utilizar uma ferramenta de migrations como o Alembic para gerenciar o esquema do banco de dados de forma versionada. Isso permite evoluir o banco de dados de forma controlada.
    - **Status:** A inicialização do Alembic foi tentada, mas enfrentou desafios de configuração de ambiente e `PATH` dentro do contêiner Docker. O ambiente Alembic foi removido para resetar.
- **Opção Simples (Desenvolvimento Inicial):** Para um início rápido em desenvolvimento, pode-se usar `Base.metadata.create_all(engine)` para criar todas as tabelas de uma vez. **Atenção:** Esta opção não é recomendada para produção ou para gerenciar mudanças no esquema ao longo do tempo.

### 2.2. Criação dos Schemas Pydantic
Definir os modelos Pydantic para validação de entrada e saída de dados da API. Estes schemas são a "interface" da sua API e são diferentes dos modelos SQLAlchemy (que são a "interface" com o banco de dados).
- Ex: `UserCreate` (para criar um usuário), `UserResponse` (para retornar dados de usuário), `CategoryBase`, `CategoryCreate`, etc.

### 2.3. Criação das Rotas da API
Implementar os endpoints da API usando FastAPI para as operações CRUD (Criar, Ler, Atualizar, Deletar) para cada um dos modelos (usuários, categorias, despesas, etc.).

### 2.4. Autenticação e Autorização
Implementar um sistema de autenticação (ex: JWT) para login/registro de usuários e autorização para proteger as rotas da API, garantindo que apenas usuários autorizados possam acessar certos recursos.

### 2.5. Testes
Escrever testes unitários e de integração para garantir a funcionalidade e a robustez da aplicação.

---

**Próximo Passo Sugerido:**
Decidir como criar as tabelas no banco de dados (Alembic ou `create_all()`) e então prosseguir com a criação dos schemas Pydantic.
