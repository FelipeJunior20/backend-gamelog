# GameLog — Backend

API REST do projeto GameLog, desenvolvida com FastAPI e Python.

---

## Pré-requisitos

Antes de qualquer coisa, certifique-se de ter instalado na sua máquina:

### 1. Python 3.14+

Baixe em [python.org](https://www.python.org/downloads/) e instale.

Verifique a instalação:
```bash
python --version
```

### 2. uv (gerenciador de pacotes)

O projeto usa `uv` no lugar do `pip` para gerenciar dependências. Instale via pip:

```bash
pip install uv
```

Verifique:
```bash
python -m uv --version
```

### 3. make (para rodar os comandos do projeto)

No Windows, instale via **winget** (disponível por padrão no Windows 10/11):

```bash
winget install GnuWin32.Make
```

Após a instalação, **reinicie o terminal** e verifique:
```bash
make --version
```

> Se o comando não for reconhecido após reiniciar, adicione `C:\Program Files (x86)\GnuWin32\bin` ao PATH do Windows manualmente em: Configurações do Sistema → Variáveis de Ambiente → Path.

---

## Configuração do Projeto

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd backend-gamelog
```

### 2. Instale as dependências

```bash
python -m uv sync
```

Esse comando lê o `pyproject.toml` e instala tudo automaticamente dentro de um ambiente virtual `.venv`.

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```bash
cp .env.example .env
```

Abra o `.env` e preencha os valores:

```env
DATABASE_URL=postgresql+asyncpg://<usuario>:<senha>@<host>/<banco>
SECRET_KEY=<chave-secreta>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Onde obter cada valor:**

| Variável | Como obter |
|---|---|
| `DATABASE_URL` | Dashboard do Neon → Connection Details → copie a string e troque `postgresql://` por `postgresql+asyncpg://`, removendo `?sslmode=require` do final |
| `SECRET_KEY` | Gere com o comando abaixo |
| `ALGORITHM` | Deixe `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Deixe `30` |

Para gerar a `SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Aplique as migrations no banco

```bash
make migrate
```

Isso cria as tabelas necessárias no banco de dados Neon.

---

## Rodando o projeto

```bash
make dev
```

O servidor sobe em `http://localhost:8000`. Para confirmar que está funcionando, acesse:

- `http://localhost:8000/api/v1/health` → deve retornar `{"status": "ok", "database": "ok"}`
- `http://localhost:8000/docs` → Swagger UI com todos os endpoints

---

## Endpoints disponíveis

| Método | Rota | Descrição | Autenticação |
|---|---|---|---|
| `GET` | `/api/v1/health` | Status da API e banco | Não |
| `POST` | `/api/v1/auth/register` | Cadastro de usuário | Não |
| `POST` | `/api/v1/auth/login` | Login, retorna JWT | Não |
| `GET` | `/api/v1/auth/me` | Dados do usuário logado | Sim (Bearer token) |

---

## Rodando os testes

```bash
make test
```

Os testes usam um banco SQLite em memória — não afetam o banco de dados do Neon.

---

## Comandos úteis

| Comando | O que faz |
|---|---|
| `make dev` | Sobe o servidor com hot reload |
| `make test` | Roda todos os testes |
| `make migrate` | Aplica migrations pendentes no banco |
| `make migration name="descricao"` | Gera uma nova migration |

---

## Estrutura do projeto

```
backend-gamelog/
├── app/
│   ├── api/v1/routes/     # Endpoints HTTP
│   ├── core/              # Config, banco de dados, segurança
│   ├── models/            # Models do banco (SQLAlchemy)
│   ├── repositories/      # Queries ao banco
│   ├── schemas/           # Schemas de entrada/saída (Pydantic)
│   └── services/          # Regras de negócio
├── tests/                 # Testes automatizados
├── alembic/               # Migrations do banco
├── .env.example           # Exemplo de variáveis de ambiente
├── Makefile               # Comandos do projeto
└── pyproject.toml         # Dependências
```
