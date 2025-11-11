# API de Colegio

API RESTful construida con **FastAPI** para gestión de autenticación, usuarios y roles en un sistema de colegio.

## Características

- ✅ Autenticación de usuarios con JWT
- ✅ Registro y login de usuarios
- ✅ Gestión de roles (admin, student)
- ✅ Protección de rutas con OAuth2
- ✅ Base de datos SQLite con SQLAlchemy
- ✅ Documentación interactiva (Swagger UI)

## Requisitos Previos

- Python 3.8+
- pip o poetry
- Git (opcional, para clonar el repositorio)

## Instalación

### 1. Clonar el repositorio (si es necesario)

```bash
git clone https://github.com/saromerop2/API-de-colegio.git
cd API-de-colegio
```

### 2. Crear un entorno virtual

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

**En Linux/Mac:**
```bash
source .venv/bin/activate
```

**En Windows:**
```bash
.venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Dependencias principales:**
- `fastapi` — Framework web
- `uvicorn` — Servidor ASGI
- `sqlalchemy` — ORM para base de datos
- `pydantic` y `pydantic-settings` — Validación de datos
- `passlib[bcrypt]` — Hash seguro de contraseñas
- `python-jose[cryptography]` — Manejo de JWT
- `python-multipart` — Procesamiento de formularios
- `python-dotenv` — Variables de entorno

## Configuración

Crea un archivo `.env` en la raíz del proyecto (opcional):

```env
SECRET_KEY=tu_clave_secreta_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=sqlite:///./school.db
```

Si no creas un `.env`, se usarán los valores por defecto de `config.py`.

## Ejecución

### Arrancar el servidor

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O si prefieres desde Python:

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en:
- **API Base:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Rutas Disponibles

### Autenticación

| Método | Ruta | Descripción | Requiere Auth |
|--------|------|-------------|---------------|
| POST | `/register` | Registrar nuevo usuario | ❌ |
| POST | `/token` | Obtener JWT token (login) | ❌ |

### Usuarios

| Método | Ruta | Descripción | Requiere Auth |
|--------|------|-------------|---------------|
| GET | `/me` | Obtener datos del usuario actual | ✅ |
| GET | `/users` | Listar todos los usuarios (solo admin) | ✅ Admin |
| PUT | `/users/{user_id}/role` | Cambiar rol de usuario (solo admin) | ✅ Admin |

### Estudiantes

| Método | Ruta | Descripción | Requiere Auth |
|--------|------|-------------|---------------|
| GET | `/student-area` | Área protegida para estudiantes | ✅ |

## Ejemplo de Uso

### 1. Registrar un usuario

```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "password": "micontraseña123",
    "full_name": "Juan Pérez"
  }'
```

**Respuesta:**
```json
{
  "id": 1,
  "username": "juan",
  "full_name": "Juan Pérez",
  "role": "student",
  "is_active": true
}
```

### 2. Obtener token (Login)

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=juan&password=micontraseña123"
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Acceder a ruta protegida

```bash
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer <TU_TOKEN_AQUI>"
```

**Respuesta:**
```json
{
  "id": 1,
  "username": "juan",
  "full_name": "Juan Pérez",
  "role": "student",
  "is_active": true
}
```

## Estructura del Proyecto

```
API-de-colegio/
├── main.py               # Aplicación principal y rutas
├── models.py             # Modelos de base de datos (User)
├── schemas.py            # Esquemas Pydantic (validación)
├── database.py           # Configuración de SQLAlchemy
├── auth.py               # Funciones de autenticación y JWT
├── config.py             # Configuración de la aplicación
├── requirements.txt      # Dependencias del proyecto
├── README.md             # Este archivo
└── school.db             # Base de datos SQLite (generada en tiempo de ejecución)
```

## Troubleshooting

### Error: `ModuleNotFoundError: No module named 'fastapi'`

**Solución:** Asegúrate de haber instalado las dependencias:
```bash
pip install -r requirements.txt
```

### Error: `pydantic.errors.PydanticImportError: BaseSettings has been moved`

**Solución:** Instala `pydantic-settings`:
```bash
pip install pydantic-settings
```

### Error: `RuntimeError: Form data requires "python-multipart"`

**Solución:** Instala `python-multipart`:
```bash
pip install python-multipart
```

### La base de datos no se crea

**Solución:** Las tablas se crean automáticamente al arrancar `main.py`. Si hay problemas, elimina `school.db` y reinicia el servidor.

## Desarrollo

### Modo watch/reload

El servidor viene configurado con `--reload`, lo que permite que reinicie automáticamente al detectar cambios en los archivos.

### Ejecutar sin reload (producción)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Despliegue en Producción

Para producción, considera:

1. **Variables de entorno:** Usa un archivo `.env` seguro o variables de entorno del sistema
2. **SECRET_KEY:** Cambia a una clave aleatoria y segura
3. **DATABASE_URL:** Usa una base de datos robusta (PostgreSQL, MySQL) en lugar de SQLite
4. **CORS:** Configura CORS según tus necesidades
5. **Servidor:** Usa Gunicorn + Uvicorn en lugar de Uvicorn solo

Ejemplo con Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --host 0.0.0.0 --port 8000
```

## Licencia

Este proyecto está bajo licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Soporte

Si tienes preguntas o encuentras problemas, abre un issue en el repositorio de GitHub.