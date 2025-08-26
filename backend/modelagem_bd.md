# Modelagem do Banco de Dados

Este documento descreve a modelagem do banco de dados para o projeto de **Controle de Gastos**, que será implementado com **FastAPI** e **PostgreSQL**.

---

## Visão Geral
O sistema permite que múltiplos usuários cadastrem suas **categorias de gastos**, dentro delas criem **expenses (subcategorias)**, definam **orçamentos mensais** e registrem **transações**.

Fluxo principal:
```
Usuário → Categoria → Expense → Transaction
```

---

## Entidades e Relacionamentos

### users
Armazena os dados de autenticação e identificação do usuário.
- **id** (PK)
- **name**
- **email** (único)
- **password_hash**
- **created_at**

### categories
Categorias principais de gastos.
- **id** (PK)
- **user_id** (FK → users.id)
- **name**
- **created_at**

### expenses
Subcategorias de gastos (dentro de uma categoria). Cada expense possui um orçamento mensal definido.
- **id** (PK)
- **user_id** (FK → users.id)
- **category_id** (FK → categories.id)
- **name**
- **created_at**

### expense_budgets
Tabela que define o **orçamento mensal** de cada expense.
- **id** (PK)
- **expense_id** (FK → expenses.id)
- **month** (formato `YYYY-MM`)
- **budget**

### transactions
Registro dos gastos reais.
- **id** (PK)
- **user_id** (FK → users.id)
- **expense_id** (FK → expenses.id)
- **amount** (valor da transação)
- **description** (opcional)
- **transaction_date** (data do gasto)
- **created_at**

---

## Diagrama ER (simplificado)

```
 users (1) ────< categories (N)
 categories (1) ────< expenses (N)
 expenses (1) ────< expense_budgets (N)
 expenses (1) ────< transactions (N)
```

---

## Script SQL (DDL - PostgreSQL)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE expense_budgets (
    id SERIAL PRIMARY KEY,
    expense_id INT NOT NULL REFERENCES expenses(id) ON DELETE CASCADE,
    month VARCHAR(7) NOT NULL, -- formato YYYY-MM
    budget NUMERIC(10,2) NOT NULL,
    UNIQUE(expense_id, month)
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expense_id INT NOT NULL REFERENCES expenses(id) ON DELETE CASCADE,
    amount NUMERIC(10,2) NOT NULL,
    description TEXT,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Notas de Implementação
- Cada usuário só vê suas próprias categorias, expenses e transações.
- O orçamento mensal agora é **obrigatório** e está na tabela `expense_budgets`, vinculado a cada mês.
- O relacionamento é em cascata (`ON DELETE CASCADE`) para evitar órfãos no banco.
- Todos os `created_at` são automáticos com `NOW()`.

---

## Próximos Passos
- Criar migrations com **Alembic** para versionamento do schema.
- Integrar com FastAPI (camada ORM usando SQLAlchemy/Pydantic models).
- Implementar autenticação (JWT) para proteger endpoints de cada usuário.

