# 🧠 AIQFome Favorites API

Uma API RESTful desenvolvida em **FastAPI + PostgreSQL (assíncrono)** para gerenciar **clientes e seus produtos favoritos**.  
A API realiza integração com a [FakeStore API](https://fakestoreapi.com) para validar e exibir informações dos produtos favoritos de cada cliente.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.12+**
- **FastAPI**
- **SQLAlchemy (async + asyncpg)**
- **PostgreSQL 15**
- **Uvicorn**
- **Docker & Docker Compose**
- **Alembic (migrações opcionais)**

---

## ⚙️ Pré-requisitos

- **Docker** ≥ 20.10  
- **Docker Compose** (ou `docker compose plugin`)  
  Verifique:
  ```bash
  docker --version
  docker compose version
  ```

---

## 🔧 Configuração

Crie um arquivo `.env` na raiz do projeto (mesmo nível do `docker`):

```env
APP_ENV=production
PORT=8000

DATABASE_URL=postgresql+asyncpg://appuser:apppass@postgres:5432/aiqfome
```

> As variáveis de ambiente são automaticamente carregadas dentro dos containers no momento da execução.

---

## 🐳 Como Subir o Projeto com Docker


### 2️⃣ Suba os containers:
```bash
docker compose up --build
```

Esse comando irá:

1. Criar a imagem da API FastAPI;  
2. Subir o PostgreSQL com volume persistente (`pgdata`);  
3. Executar automaticamente o script `init_db.py`, que cria todas as tabelas conforme os modelos definidos em `app/data/models.py`;  
4. Iniciar a aplicação em `http://localhost:8000`.

---

## 🗄️ Inicialização Automática do Banco de Dados

Na **primeira vez** que o container `postgres_db` for iniciado, o script  
`docker/init_db.py` será executado automaticamente dentro da pasta  
`/docker-entrypoint-initdb.d/` e criará todas as tabelas do banco.

Se você quiser **forçar uma recriação completa do banco e tabelas**, rode:
```bash
docker compose down -v
docker compose up --build
```

---

## 🌐 Endpoints Principais

### **Clientes**
| Método | Rota | Descrição |
|--------|------|------------|
| `GET` | `/clients/` | Lista todos os clientes |
| `GET` | `/clients/{id}` | Retorna um cliente pelo ID |
| `POST` | `/clients/` | Cria um novo cliente |
| `PUT` | `/clients/{id}` | Atualiza totalmente um cliente |
| `PATCH` | `/clients/{id}` | Atualiza parcialmente um cliente |
| `DELETE` | `/clients/{id}` | Remove um cliente |

---

### **Favoritos**
| Método | Rota | Descrição |
|--------|------|------------|
| `POST` | `/clients/{client_id}/favorites` | Adiciona um produto favorito ao cliente |
| `GET` | `/clients/{client_id}/favorites` | Lista os produtos favoritos do cliente |
| `DELETE` | `/clients/{client_id}/favorites/{product_id}` | Remove um produto favorito do cliente |

---

## 🔍 Testando a API

Acesse a documentação interativa:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)


## 🧱 Estrutura do Banco de Dados

**Entidades principais:**

- `clients` — cadastro de clientes (nome, email, timestamps)
- `products_snapshot` — cache local de produtos vindos da FakeStore API
- `favorites` — relacionamento N:N entre clientes e produtos (sem duplicidade)

**Relacionamentos:**
```
clients (1) --- (N) favorites (N) --- (1) products_snapshot
```

---

## 📦 Exemplo de Uso via cURL

### Criar um cliente:
```bash
curl -X POST http://localhost:8000/clients -H "Content-Type: application/json" -d '{"name": "Maria", "email": "maria@teste.com"}'
```

### Adicionar um produto favorito:
```bash
curl -X POST http://localhost:8000/clients/1/favorites -H "Content-Type: application/json" -d '{"external_product_id": 1}'
```

### Listar favoritos do cliente:
```bash
curl http://localhost:8000/clients/1/favorites
```
