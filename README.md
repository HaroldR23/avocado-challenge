# Avocado challenge

##  🚀 ¿Cómo levantar el projecto?

Este documento explica cómo iniciar el backend de FastAPI junto con PostgreSQL usando **Docker Compose**.

---

## 1️⃣ Requisitos

- **Docker** instalado  
- **Docker Compose** V2 o el plugin `docker-compose`  

---

## 2️⃣ Crear archivo `.env`

En la raíz del proyecto (junto a `docker-compose.yml`), crea un archivo `.env` con el siguiente contenido:

```env
POSTGRES_USER=<user_db>
POSTGRES_PASSWORD=<password_db>
POSTGRES_DB=<name_db>
```

## 3️⃣ Levantar la aplicación

Ejecuta en tu terminal el siguiente comando:

```shell
docker compose up --build
```

## 4️⃣ Migraciones automáticas

El docker-compose.yml está configurado para ejecutar:

```shell
alembic upgrade head
```

## 5️⃣ Acceder a la API

Una vez que los contenedores estén levantados, la API estará disponible en:

http://localhost:8000

La documentación interactiva de FastAPI estará en:

http://localhost:8000/docs
