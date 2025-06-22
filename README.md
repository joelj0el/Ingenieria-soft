# 🏆 OLIMPAZ - Sistema de Gestión de Juegos Olímpicos Universitarios

## 📋 Descripción del Proyecto

**OLIMPAZ** es un sistema web completo desarrollado en Django para la gestión integral de competencias deportivas universitarias. El sistema permite administrar equipos, disciplinas, partidos, resultados y generar rankings automáticos tanto por equipos como por carreras universitarias.

### 🎯 Objetivo Principal
Facilitar la organización y gestión de eventos deportivos universitarios, proporcionando herramientas para:
- Registrar y gestionar equipos deportivos
- Programar y administrar partidos
- Registrar resultados automáticamente
- Generar rankings dinámicos
- Gestionar usuarios con diferentes roles

## ✨ Características Principales

### 🔐 **Sistema de Usuarios**
- **Roles diferenciados**: Administrativo, Juez, Estudiante
- **Autenticación segura** con perfiles personalizados
- **Gestión de permisos** por rol de usuario

### 👥 **Gestión de Equipos**
- Registro de equipos por disciplina y carrera
- Asignación de jugadores con restricciones por disciplina
- Subida de logos y información detallada
- Validación: 1 jugador = 1 equipo por disciplina

### 🏃 **Disciplinas Deportivas**
- Soporte para múltiples disciplinas (Fútbol, Baloncesto, Vóley, Futsal, etc.)
- Configuración específica por disciplina
- Gestión de categorías (Masculino, Femenino, Mixto)

### 📅 **Sistema de Partidos**
- Programación automática de fixtures
- Registro de resultados en tiempo real
- Actualización automática de estadísticas
- Control de estados de partidos

### 📊 **Rankings y Estadísticas**
- **Ranking general de carreras**: Puntuación acumulada por carrera universitaria
- **Tablas por disciplina**: Posiciones específicas por deporte
- **Actualización automática**: Los puntos se calculan automáticamente
- **Sistema de puntuación**: Victoria = 2000 pts, Empate = 1000 pts, Derrota = 0 pts

### 🖥️ **Dashboard Interactivo**
- Panel de control con estadísticas en tiempo real
- Filtros por disciplina y categoría
- Visualización de partidos recientes
- Alternancia entre rankings generales y específicos

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2+ (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL o SQL Server (producción)
- **API**: Django REST Framework
- **Autenticación**: Sistema de sesiones de Django
- **UI Framework**: Bootstrap 5
- **Iconos**: Font Awesome
- **Archivos**: Pillow para procesamiento de imágenes

## 🚀 Instalación Completa

### 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8 o superior** ([Descargar Python](https://www.python.org/downloads/))
- **pip** (incluido con Python)
- **Git** ([Descargar Git](https://git-scm.com/downloads))
- **Editor de código** (recomendado: VS Code)

### 🔧 Paso 1: Preparar el Entorno

```bash
# Verificar versiones instaladas
python --version
pip --version
git --version

# Crear directorio para el proyecto
mkdir olimpaz-proyecto
cd olimpaz-proyecto
```

### 📥 Paso 2: Clonar o Descargar el Proyecto

**Opción A: Si tienes acceso al repositorio Git**
```bash
git clone [URL_DEL_REPOSITORIO] olimpaz
cd olimpaz
```

**Opción B: Si tienes los archivos localmente**
```bash
# Copiar todos los archivos del proyecto a la carpeta actual
# Asegúrate de que todos los archivos estén en la carpeta 'olimpaz'
cd olimpaz
```

### 🐍 Paso 3: Configurar Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Verificar que el entorno esté activo (verás (venv) en el prompt)
```

### 📦 Paso 4: Instalar Dependencias

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Si no existe requirements.txt, instalar manualmente:
pip install django==4.2
pip install djangorestframework
pip install pillow
pip install django-cors-headers
```

### 🗄️ Paso 5: Configurar Base de Datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Verificar que las tablas se crearon correctamente
python manage.py showmigrations
```

### 👤 Paso 6: Crear Usuario Administrador

```bash
# Crear superusuario
python manage.py createsuperuser

# Seguir las instrucciones:
# - Nombre de usuario: admin (o el que prefieras)
# - Email: tu-email@ejemplo.com
# - Contraseña: (usa una contraseña segura)
```

### 🌱 Paso 7: Poblar Datos Iniciales (Opcional)

```bash
# Ejecutar script para crear carreras universitarias
python populate_carreras.py

# Crear usuarios de prueba (opcional)
python crear_usuarios_prueba.py

# Crear disciplinas y equipos de prueba (opcional)
python crear_partidos_prueba.py
```

### 🚀 Paso 8: Ejecutar el Servidor

```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# El servidor estará disponible en:
# http://127.0.0.1:8000/ o http://localhost:8000/
```

## 🔍 Primeros Pasos

### 1. **Acceder al Sistema**
- Abrir navegador en `http://localhost:8000`
- Hacer clic en "Iniciar Sesión"
- Usar las credenciales del superusuario creado

### 2. **Configuración Inicial**
- Ir a **Panel de Administración**: `http://localhost:8000/admin/`
- Crear **Carreras Universitarias** si no se poblaron automáticamente
- Crear **Disciplinas Deportivas** (Fútbol, Baloncesto, Vóley, etc.)

### 3. **Crear Primer Equipo**
- Ir a **Teams** en el menú principal
- Hacer clic en "Nuevo Equipo"
- Completar información: nombre, carrera, disciplina, categoría
- Buscar y agregar jugadores
- Guardar equipo

### 4. **Programar Partidos**
- Ir al panel de administración de partidos
- Crear nuevos partidos entre equipos existentes
- Asignar fechas y horarios

### 5. **Registrar Resultados**
- Una vez finalizado un partido, registrar el resultado
- El sistema actualizará automáticamente las estadísticas
- Ver los rankings actualizados en el dashboard

## 📁 Estructura del Proyecto

```
OLIMPAZ/
├── 📁 Olimpaz/                    # Configuración principal
│   ├── ⚙️ settings.py            # Configuraciones de Django
│   ├── 🌐 urls.py                # URLs principales del proyecto
│   ├── 📄 wsgi.py                # Configuración para servidor web
│   └── 📄 asgi.py                # Configuración para WebSockets
│
├── 📁 usuarios/                   # App principal - Gestión de usuarios y equipos
│   ├── 📄 models.py              # Modelos: Usuario, Perfil, Carrera, Disciplina, Equipo
│   ├── 📄 views.py               # Vistas del frontend
│   ├── 📄 api_views.py           # API REST endpoints
│   ├── 📄 serializers.py         # Serializadores para API
│   ├── 📄 forms.py               # Formularios de Django
│   ├── 📄 urls.py                # URLs de la app usuarios
│   ├── 📄 equipos_views.py       # Vistas específicas para equipos
│   ├── 📄 jueces_views.py        # Vistas específicas para jueces
│   └── 📁 migrations/            # Migraciones de base de datos
│
├── 📁 partidos/                   # App de partidos y competencias
│   ├── 📄 models.py              # Modelos: Partido, Sede, FixtureGenerado
│   ├── 📄 views.py               # Vistas para gestión de partidos
│   ├── 📄 urls.py                # URLs de partidos
│   └── 📁 migrations/            # Migraciones de partidos
│
├── 📁 templates/                  # Plantillas HTML
│   ├── 📄 base.html              # Plantilla base
│   ├── 📄 home.html              # Dashboard principal
│   ├── 📄 teams.html             # Gestión de equipos
│   └── 📄 admin_panel.html       # Panel administrativo
│
├── 📁 static/                     # Archivos estáticos
│   ├── 📁 css/                   # Hojas de estilo
│   │   ├── 📄 styles.css         # Estilos principales
│   │   ├── 📄 dashboard.css      # Estilos del dashboard
│   │   └── 📄 teams.css          # Estilos de equipos
│   ├── 📁 js/                    # JavaScript
│   │   ├── 📄 script.js          # Scripts principales
│   │   └── 📄 teams.js           # Scripts de equipos
│   └── 📁 images/                # Imágenes del sistema
│
├── 📁 media/                      # Archivos subidos por usuarios
│   ├── 📁 equipos/               # Logos de equipos
│   └── 📁 disciplinas/           # Imágenes de disciplinas
│
├── 📄 manage.py                   # Script principal de Django
├── 📄 requirements.txt           # Dependencias Python
├── 📄 README.md                  # Este archivo
├── 📄 populate_carreras.py       # Script para poblar carreras
├── 📄 crear_usuarios_prueba.py   # Script para crear usuarios de prueba
└── 📄 crear_partidos_prueba.py   # Script para crear datos de prueba
```

## 🔧 Comandos Útiles para Desarrollo

### 🗄️ Base de Datos
```bash
# Crear nuevas migraciones después de cambios en models.py
python manage.py makemigrations

# Aplicar migraciones pendientes
python manage.py migrate

# Ver estado de migraciones
python manage.py showmigrations

# Acceder al shell de Django
python manage.py shell

# Crear copia de seguridad de la base de datos (SQLite)
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3
```

### 🧪 Testing y Depuración
```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de una app específica
python manage.py test usuarios

# Ejecutar servidor en modo debug
python manage.py runserver --settings=Olimpaz.settings_debug

# Verificar configuración
python manage.py check
```

### 📊 Datos y Contenido
```bash
# Recopilar archivos estáticos para producción
python manage.py collectstatic

# Limpiar sesiones expiradas
python manage.py clearsessions

# Crear datos de prueba
python crear_usuarios_prueba.py
python crear_partidos_prueba.py
```

## 🌐 Acceso a las Funcionalidades

### 🏠 **Dashboard Principal**
- **URL**: `http://localhost:8000/`
- **Funcionalidad**: Vista general con estadísticas, rankings y partidos recientes
- **Usuarios**: Todos los usuarios autenticados

### 👥 **Gestión de Equipos**
- **URL**: `http://localhost:8000/usuarios/teams/`
- **Funcionalidad**: Crear, editar y eliminar equipos y disciplinas
- **Usuarios**: Solo administradores

### ⚙️ **Panel de Administración**
- **URL**: `http://localhost:8000/admin/`
- **Funcionalidad**: Administración completa del sistema
- **Usuarios**: Solo superusuarios

### 🔐 **Gestión de Usuarios**
- **Login**: `http://localhost:8000/usuarios/login/`
- **Registro**: `http://localhost:8000/usuarios/registro/`
- **Panel Admin**: `http://localhost:8000/usuarios/admin/`

## 🚨 Solución de Problemas Comunes

### ❌ **Error: "No module named 'django'"**
```bash
# Verificar que el entorno virtual esté activo
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstalar Django
pip install django
```

### ❌ **Error: "You have unapplied migrations"**
```bash
# Aplicar todas las migraciones
python manage.py migrate

# Si persiste, crear nuevas migraciones
python manage.py makemigrations
python manage.py migrate
```

### ❌ **Error: "Port already in use"**
```bash
# Usar un puerto diferente
python manage.py runserver 8001

# O encontrar y matar el proceso en puerto 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### ❌ **Error: "Static files not loading"**
```bash
# Recopilar archivos estáticos
python manage.py collectstatic

# Verificar configuración en settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

## 🤝 Contribuir al Proyecto

1. **Fork** el repositorio
2. **Crear** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crear** un Pull Request

## 📞 Soporte y Contacto

Si tienes problemas con la instalación o el funcionamiento del sistema:

1. **Revisar** este README completo
2. **Verificar** la sección de solución de problemas
3. **Consultar** los logs de error en la consola
4. **Contactar** al equipo de desarrollo

## 📄 Licencia

Este proyecto está desarrollado para fines educativos y de gestión deportiva universitaria.

---

### 🎉 ¡Proyecto Configurado Exitosamente!

Si llegaste hasta aquí y el servidor está corriendo en `http://localhost:8000`, ¡felicitaciones! El sistema OLIMPAZ está listo para gestionar tus competencias deportivas universitarias.

**Próximos pasos recomendados:**
1. Explorar el dashboard principal
2. Crear algunas disciplinas y equipos de prueba
3. Programar partidos de ejemplo
4. Registrar resultados y ver los rankings en acción

¡Disfruta gestionando tus Juegos Olímpicos de Paz! 🏆

---

### 🗄️ Configuración de Base de Datos en SQL Server

Si vas a usar **SQL Server** como base de datos (recomendado para producción), sigue estos pasos antes de ejecutar las migraciones:

#### 1. Crear la base de datos en SQL Server

Puedes usar SQL Server Management Studio (SSMS) o ejecutar el siguiente script en tu consola de SQL Server:

```sql
-- Crear la base de datos
CREATE DATABASE OLIMPAZ1;
GO

-- (Opcional) Crear un usuario y asignarle permisos
USE OLIMPAZ1;
GO
CREATE LOGIN olimpaz_user WITH PASSWORD = 'TuPasswordSegura123';
CREATE USER olimpaz_user FOR LOGIN olimpaz_user;
ALTER ROLE db_owner ADD MEMBER olimpaz_user;
GO
```

#### 2. Instalar el driver de SQL Server para Python

```bash
pip install mssql-django
pip install pyodbc
```

#### 3. Configurar la conexión en `settings.py` de Django

En el archivo `Olimpaz/settings.py`, busca la sección `DATABASES` y reemplázala por:

```python
# Configuración para SQL Server
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'OLIMPAZ1',
        'USER': '',  # si usas conexión integrada
        'PASSWORD': '', 
        'HOST': 'localhost\\SQLEXPRESS',  # ← con doble backslash
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'yes',
        },
    }
}
```

> **Nota:** Asegúrate de tener instalado el driver ODBC adecuado en tu sistema. Puedes descargarlo desde: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

#### 4. Probar la conexión

Una vez configurado, ejecuta:
```bash
python manage.py migrate
```
Si no hay errores, ¡la conexión está lista!
