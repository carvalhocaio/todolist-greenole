# ToDo List Greenole

Sistema de gerenciamento de tarefas (ToDo List) desenvolvido em Python/Django para fins de teste técnico na Greenole.

## Descrição

Esta aplicação fornece uma API para criação, listagem, atualização, filtragem (por status e busca textual) e remoção de tarefas. O backend foi construído utilizando Django e Django Rest Framework, com suporte a testes automatizados e documentação OpenAPI/Swagger.

## Funcionalidades

- CRUD completo de tarefas (ToDo)
- Filtragem por status (`IN_PROGRESS`, `CONCLUDED`)
- Busca textual no título e descrição
- Paginação nos resultados
- Testes automatizados com Django TestCase
- Documentação automática da API (Swagger/OpenAPI)
- Configuração pronta para uso com Docker (Postgres e Redis)

## Requisitos

- Python >= 3.11
- Poetry ([documentação](https://python-poetry.org/docs/))
- Django >= 4.2.7
- Docker (para banco de dados e cache)
- Redis
- PostgreSQL

## Instalação e Execução

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/carvalhocaio/todolist-greenole.git
   cd todolist-greenole
   ```

2. **Instale o Poetry e ative o ambiente virtual:**
   ```sh
   pipx inject poetry poetry-plugin-shell
   poetry shell
   ```

3. **Instale as dependências:**
   ```sh
   poetry install
   ```

4. **Configure as variáveis de ambiente:**
   - Renomeie `.env-sample` para `.env` e preencha os valores (ex: `SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`).

5. **Suba os containers de banco e cache:**
   ```sh
   docker run -d --name postgres-greenole -e POSTGRES_PASSWORD="postgres" -p 5432:5432 postgres
   docker run -d --name redis-greenole -p 6379:6379 redis
   ```

6. **Rode as migrações:**
   ```sh
   python manage.py migrate
   ```

7. **Inicie o servidor de desenvolvimento:**
   ```sh
   python manage.py runserver
   ```

## Uso

- Acesse a API em: http://localhost:8000/
- Documentação automática em: http://localhost:8000/api/schema/swagger-ui/

## Testes

Para executar os testes automatizados:
```sh
python manage.py test todo/tests
```

## Principais Endpoints

- `GET /todo/` — Lista as tarefas, com filtros por status e busca
- `POST /todo/` — Cria uma nova tarefa
- `GET /todo/{id}/` — Consulta uma tarefa específica
- `PATCH /todo/{id}/` — Atualiza parcialmente uma tarefa (status, título, descrição)
- `PUT /todo/{id}/` — Atualiza totalmente uma tarefa
- `DELETE /todo/{id}/` — Remove uma tarefa

## Licença

MIT

---

Desenvolvido por [carvalhocaio](https://github.com/carvalhocaio)
