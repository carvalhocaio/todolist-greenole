# ToDo List for Greenole

Greenole test app

## Requisites

- Python >= 3.11
- Poetry (https://python-poetry.org/docs/)
- Django >= 4.2.7
- Docker

## Execute project

- Install poetry shell: `pipx inject poetry poetry-plugin-shell`
- Start the poetry shell: `poetry shell`
- Install the dependencies: `poetry install`
- Rename `.env-sample` for `.env` and fill in the variable values, mainly to `SECRET_KEY`, `DATABASE_URL`
  and `REDIS_URL`
- Before starting the application, the database containers must be started. Postgres
  with `docker run -d --name postgres-greenole -e POSTGRES_PASSWORD="postgres" -p 5432:5432 postgres` and
  Redis `docker run -d --name redis-greenole -p 6379:6379 redis`
- After running the containers, run the pending migrations: `python manage.py migrate`
- Lastly, run the application with: `python manage.py runserver`

## Test

For execute tests, run in the terminal `python manage.py test todo/tests`

---
