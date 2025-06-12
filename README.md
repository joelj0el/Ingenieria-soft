
# 🏆 OLIMPAZ - Sistema de Gestión Deportiva

## 📋 Descripción

OLIMPAZ es un sistema web desarrollado en Django para la gestión de competencias deportivas, equipos, jugadores y jueces. Permite administrar disciplinas deportivas, crear fixtures, gestionar equipos y llevar un control completo de los eventos deportivos.

## ✨ Características

- 🔐 **Autenticación y autorización**: Sistema de usuarios con roles (Admin, Juez, Participante)
- 👥 **Gestión de equipos**: Registro y administración de equipos deportivos
- 🏃 **Gestión de disciplinas**: Manejo de diferentes disciplinas deportivas
- ⚖️ **Sistema de jueces**: Asignación y gestión de jueces por disciplina
- 📅 **Gestión de fixtures**: Creación y administración de calendarios deportivos
- 🏟️ **Gestión de sedes**: Control de sedes y horarios de competencias
- 📊 **API REST**: API completa con documentación Swagger
- 🔒 **Autenticación JWT**: Sistema de tokens para API

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2+
- **API**: Django REST Framework
- **Autenticación**: JWT (JSON Web Tokens)
- **Base de datos**: SQL SERVER
- **Documentación API**: drf-yasg (Swagger)
- **Frontend**: HTML, CSS, JavaScript
- **Imágenes**: Pillow para procesamiento

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de instalación

1. **Clonar el repositorio**


2. **Configurar base de datos**


CREA EL MODELO
   BASE DE DATOS:Add commentMore actions

-- Crear la base de datos
CREATE DATABASE OLIMPAZ1;
GO

USE OLIMPAZ1;
GO

-- Tabla para el perfil (extensión del modelo User)
CREATE TABLE usuarios_perfil (
    id INT IDENTITY(1,1) PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    telefono NVARCHAR(15) NULL,
    direccion NVARCHAR(MAX) NULL,
    fecha_registro DATETIME NOT NULL
);
GO

-- Crear índices para mejorar el rendimiento
-- Puedes agregar índices específicos si es necesario más adelante
-- CREATE INDEX IX_usuarios_perfil_usuario_id ON usuarios_perfil (usuario_id);
GO

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Poblar datos iniciales (opcional)**
   ```bash
   python populate_carreras.py
   ```

8. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

El proyecto estará disponible en `http://localhost:8000`

## 📚 Documentación de la API

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **Panel de Admin**: `http://localhost:8000/admin/`

## 🗂️ Estructura del Proyecto

```
olimpaz/
├── Olimpaz/                 # Configuración principal del proyecto
│   ├── settings.py         # Configuraciones de Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuración WSGI
├── usuarios/               # App principal de usuarios y gestión
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas del frontend
│   ├── api_views.py       # Vistas de la API
│   ├── serializers.py     # Serializadores para API
│   └── urls.py            # URLs de la app
├── templates/              # Plantillas HTML
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── media/                  # Archivos subidos por usuarios
├── requirements.txt        # Dependencias del proyecto
└── manage.py              # Script de gestión de Django
```

## 🔧 Comandos Útiles

```bash
# Ejecutar tests
python manage.py test

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar shell de Django
python manage.py shell