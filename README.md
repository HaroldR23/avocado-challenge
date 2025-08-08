# Avocado challenge

##  🚀 ¿Cómo levantar el projecto?

Esta primera parte del documento explica cómo iniciar el backend de FastAPI junto con PostgreSQL usando **Docker Compose**.

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


## Tests

Para ejecutar los tests basta con moverte a la carpeta /backend, instalar las dependencias y ejecutar los tests, como sigue:

```shell
poetry install
```

Este comando creará un virtual env el cual tienes que activar, y luego podrás ejectuar los tests como sigue:
```shell
pytest
```



En esta segunda parte se explica como levantar el frontend de nuestra aplicación

## 1️⃣ Instalar dependencias

Primero tiene que moverte a la carpeta /frontend, puedes hacerlo corriendo el siguiente comando:

```shell
cd /frontend
```
Y luego ejecuta este comando:

```shell
npm install
```

## 2️⃣ Levantar nuestro frontend

Para levantar nuestro frontend basta con ejecutar este comando:

```shell
npm run dev
```
