
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
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción)
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
   ```bash
   git clone https://github.com/tu-usuario/olimpaz.git
   cd olimpaz
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   # Copiar el archivo de ejemplo
   cp .env.example .env
   
   # Editar .env con tus configuraciones
   ```

5. **Configurar base de datos**
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
```

## 🚀 Despliegue en Producción

### Variables de entorno importantes

Asegúrate de configurar estas variables en producción:

- `SECRET_KEY`: Clave secreta de Django
- `DEBUG=False`: Desactivar modo debug
- `ALLOWED_HOSTS`: Hosts permitidos
- `DATABASE_URL`: URL de base de datos PostgreSQL

### Usando Heroku

1. Instalar Heroku CLI
2. Crear aplicación: `heroku create olimpaz-app`
3. Configurar variables de entorno
4. Desplegar: `git push heroku main`

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [tu-usuario](https://github.com/tu-usuario)

## 📞 Contacto

- Email: tu-email@ejemplo.com
- LinkedIn: [tu-perfil](https://linkedin.com/in/tu-perfil)

---

BASE DE DATOS:

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

-- Procedimiento almacenado para crear un nuevo usuario (opcional)
CREATE PROCEDURE sp_crear_usuario
    @username NVARCHAR(150),
    @password NVARCHAR(128),
    @first_name NVARCHAR(150),
    @last_name NVARCHAR(150),
    @email NVARCHAR(254),
    @is_active BIT = 1,
    @is_staff BIT = 0,
    @is_superuser BIT = 0
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Aquí no se crearán registros en la tabla auth_user, 
    -- porque hemos omitido las tablas relacionadas con Django.
    -- Solo se insertan datos directamente en la tabla 'usuarios_perfil'.
    
    DECLARE @date_registro DATETIME = GETDATE();
    
    INSERT INTO usuarios_perfil (
        usuario_id, telefono, direccion, fecha_registro
    )
    VALUES (
        -- Asumir que 'usuario_id' se gestionará de alguna manera 
        -- o se generará con alguna lógica adicional
        NULL, 
        NULL, 
        NULL, 
        @date_registro
    );
    
    SELECT SCOPE_IDENTITY() AS user_id;
END;
GO




AQUI ESTAN LOS COMANDOS NECESARIOS PARA PODER HACER CORRER EL PROYECTO.

python -m venv venv
venv\Scripts\activate

pip install django
pip install djangorestframework
pip install django-mssql-backend
pip install pyodbc

python manage.py migrate

python manage.py createsuperuser



python manage.py runserver

Este es el proyecto inicial, pero no estamos usndo una api, el endpoint de este proyecto esta mediante rutas, en todo caso para usar los json que nos dijo el docente, necesitamos cambiar algunos archivos, 
para poder usar DjangoRest que es algo mas que debemos aprender, y esto si usa los edpoints para el conectar con la BD y el backend.

El proyecto por el momento solo tiene el login. 
