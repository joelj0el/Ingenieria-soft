# DOCUMENTACIÓN DE API - OLIMPAZ

## URL Base del Servidor
- **Base URL**: `http://localhost:8000` (desarrollo)

## VERSIONES DE API

### 🔸 API V1 (Personalizada)
- **Base URL**: `/usuarios/api/`
- **Características**: APIs personalizadas con lógica específica
- **Autenticación**: Sesiones Django

### 🔸 API V2 (Django REST Framework)
- **Base URL**: `/api/v2/`
- **Características**: ViewSets con CRUD automático completo
- **Autenticación**: JWT Tokens (recomendado)

### 🔸 API Partidos
- **Base URL**: `/partidos/api/`
- **Características**: APIs específicas para gestión de partidos

## AUTENTICACIÓN

### 1. Login de Usuario
- **Endpoint**: `POST /usuarios/api/login/`
- **JSON Request**:
```json
{
    "username": "admin",
    "password": "123456"
}
```
- **JSON Response** (éxito):
```json
{
    "message": "Login exitoso",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@uab.edu.bo",
        "first_name": "Administrador",
        "last_name": "Sistema"
    },
    "perfil": {
        "rol": "admin",
        "carrera": null
    }
}
```

### 2. Logout de Usuario
- **Endpoint**: `DELETE /usuarios/api/logout/`
- **Headers**: `Content-Type: application/json`
- **No requiere body**

### 3. JWT Token (Alternativo)
- **Endpoint**: `POST /api/token/`
- **JSON Request**:
```json
{
    "username": "admin",
    "password": "123456"
}
```
- **JSON Response**:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## USUARIOS

### 4. Crear Usuario (V1)
- **Endpoint**: `POST /usuarios/api/registro/`
- **JSON Request**:
```json
{
    "username": "nuevo_estudiante",
    "password": "123456",
    "email": "estudiante@uab.edu.bo",
    "first_name": "Juan",
    "last_name": "Pérez",
    "perfil": {
        "rol": "estudiante",
        "carrera": 1
    }
}
```

### 5. Listar Usuarios (V1)
- **Endpoint**: `GET /usuarios/api/usuarios/`
- **Response**:
```json
[
    {
        "id": 1,
        "username": "admin",
        "email": "admin@uab.edu.bo",
        "first_name": "Admin",
        "last_name": "Sistema",
        "perfil": {
            "rol": "admin",
            "carrera": null
        }
    }
]
```

### 6. Obtener Usuario Actual (V1)
- **Endpoint**: `GET /usuarios/api/usuarios/actual/`
- **Headers**: Requiere autenticación

### 7. USUARIOS API V2 (ViewSets - CRUD Completo)
- **Listar**: `GET /api/v2/usuarios/`
- **Crear/Registrar**: `POST /api/v2/usuarios/`
- **Obtener**: `GET /api/v2/usuarios/{id}/`
- **Actualizar**: `PUT /api/v2/usuarios/{id}/`
- **Actualizar parcial**: `PATCH /api/v2/usuarios/{id}/`
- **Eliminar**: `DELETE /api/v2/usuarios/{id}/`
- **Usuario actual**: `GET /api/v2/usuarios/current/`

**Ejemplo JSON para REGISTRAR usuario (V2)**:
```json
{
    "username": "usuario_v2",
    "email": "usuario@uab.edu.bo",
    "first_name": "Nombre",
    "last_name": "Apellido",
    "password": "123456",
    "rol": "estudiante",
    "carrera": 1
}
```

**Validaciones automáticas (V2)**:
- Email debe terminar en `@uab.edu.bo`
- Si rol es "estudiante", carrera es obligatoria
- Password se encripta automáticamente
- Se crea perfil asociado automáticamente

## CARRERAS

### 8. Listar Carreras (V1)
- **Endpoint**: `GET /usuarios/api/carreras/`
- **Response**:
```json
[
    {
        "id": 1,
        "nombre": "Ingeniería de Sistemas"
    },
    {
        "id": 2,
        "nombre": "Administración de Empresas"
    }
]
```

### 9. CARRERAS API V2 (ViewSets - CRUD Completo)
- **Listar**: `GET /api/v2/carreras/`
- **Crear**: `POST /api/v2/carreras/`
- **Obtener**: `GET /api/v2/carreras/{id}/`
- **Actualizar**: `PUT /api/v2/carreras/{id}/`
- **Eliminar**: `DELETE /api/v2/carreras/{id}/`

**Ejemplo JSON para crear (V2)**:
```json
{
    "nombre": "Ingeniería Industrial"
}
```

## DISCIPLINAS

### 10. Listar Disciplinas (V1)
- **Endpoint**: `GET /usuarios/api/disciplinas/`
- **Response**:
```json
[
    {
        "id": 1,
        "nombre": "Futbol",
        "descripcion": "Futbol masculino y femenino",
        "imagen": "/media/disciplinas/futbol.jpg",
        "categoria": "masculino"
    }
]
```

### 11. Crear Disciplina (V1)
- **Endpoint**: `POST /usuarios/api/disciplinas/`
- **JSON Request**:
```json
{
    "nombre": "Basquet",
    "descripcion": "Basquetbol universitario",
    "categoria": "femenino"
}
```

### 12. Actualizar Disciplina (V1)
- **Endpoint**: `PUT /usuarios/api/disciplinas/{id}/`

### 13. Eliminar Disciplina (V1)
- **Endpoint**: `DELETE /usuarios/api/disciplinas/{id}/`

### 14. DISCIPLINAS API V2 (ViewSets - CRUD Completo)
- **Listar**: `GET /api/v2/disciplinas/`
- **Crear**: `POST /api/v2/disciplinas/`
- **Obtener**: `GET /api/v2/disciplinas/{id}/`
- **Actualizar**: `PUT /api/v2/disciplinas/{id}/`
- **Eliminar**: `DELETE /api/v2/disciplinas/{id}/`

## EQUIPOS

### 14. Listar Equipos
- **Endpoint**: `GET /usuarios/api/equipos/`
- **Response**:
```json
[
    {
        "id": 1,
        "nombre": "Los Tigres",
        "carrera": {
            "id": 1,
            "nombre": "Ingeniería de Sistemas"
        },
        "disciplina": {
            "id": 1,
            "nombre": "Futbol"
        },
        "categoria": "masculino",
        "capitan": {
            "id": 2,
            "username": "capitan1",
            "first_name": "Carlos",
            "last_name": "López"
        },
        "jugadores": [
            {
                "id": 2,
                "username": "jugador1",
                "first_name": "Juan",
                "last_name": "Pérez"
            }
        ],
        "imagen": "/media/equipos/tigres.jpg"
    }
]
```

### 15. Crear Equipo
- **Endpoint**: `POST /usuarios/api/equipos/`
- **JSON Request**:
```json
{
    "nombre": "Los Leones",
    "carrera": 1,
    "disciplina": 1,
    "categoria": "masculino",
    "capitan": 2,
    "jugadores": [2, 3, 4]
}
```

### 16. Actualizar Equipo
- **Endpoint**: `PUT /usuarios/api/equipos/{id}/`
- **JSON Request**: (misma estructura que crear)

### 17. Eliminar Equipo
- **Endpoint**: `DELETE /usuarios/api/equipos/{id}/`

## JUECES

### 18. Listar Jueces
- **Endpoint**: `GET /usuarios/api/jueces/`
- **Response**:
```json
[
    {
        "id": 1,
        "usuario": {
            "id": 3,
            "username": "juez1",
            "first_name": "Pedro",
            "last_name": "Martínez"
        },
        "disciplinas": [
            {
                "id": 1,
                "nombre": "Futbol"
            }
        ],
        "activo": true
    }
]
```

### 19. Crear Juez
- **Endpoint**: `POST /usuarios/api/jueces/`
- **JSON Request**:
```json
{
    "usuario": 3,
    "disciplinas": [1, 2],
    "activo": true
}
```

## PARTIDOS

### 20. Listar Partidos
- **Endpoint**: `GET /partidos/api/partidos/`
- **Query Parameters**:
  - `estado`: programado, en_curso, finalizado, cancelado
  - `disciplina_id`: ID de disciplina
  - `categoria`: masculino, femenino, mixto
- **Example**: `GET /partidos/api/partidos/?estado=programado&disciplina_id=1`

- **Response**:
```json
[
    {
        "id": 1,
        "equipo_local": {
            "id": 1,
            "nombre": "Los Tigres"
        },
        "equipo_visitante": {
            "id": 2,
            "nombre": "Los Leones"
        },
        "disciplina": {
            "id": 1,
            "nombre": "Futbol"
        },
        "fecha_hora": "2024-01-15T15:00:00Z",
        "estado": "programado",
        "categoria": "masculino",
        "resultado_local": null,
        "resultado_visitante": null,
        "observaciones": "",
        "juez": null
    }
]
```

### 21. Crear Partido
- **Endpoint**: `POST /partidos/api/partidos/`
- **JSON Request**:
```json
{
    "equipo_local": 1,
    "equipo_visitante": 2,
    "disciplina": 1,
    "fecha_hora": "2024-01-15T15:00:00Z",
    "categoria": "masculino",
    "juez": 1
}
```

### 22. Actualizar Partido
- **Endpoint**: `PUT /partidos/api/partidos/{id}/`
- **JSON Request** (actualizar resultado):
```json
{
    "estado": "finalizado",
    "resultado_local": 3,
    "resultado_visitante": 1,
    "observaciones": "Partido disputado sin incidentes"
}
```

### 23. Eliminar Partido
- **Endpoint**: `DELETE /partidos/api/partidos/{id}/`

### 24. Generar Fixture Automático
- **Endpoint**: `POST /partidos/api/generar-fixture/`
- **JSON Request**:
```json
{
    "disciplina_id": 1,
    "categoria": "masculino",
    "fecha_inicio": "2024-01-15",
    "descripcion": "Torneo de Futbol Masculino 2024"
}
```

- **Response**:
```json
{
    "message": "Fixture generado exitosamente",
    "fixture_id": 1,
    "partidos_creados": 6,
    "partidos": [
        {
            "id": 1,
            "equipo_local": "Los Tigres",
            "equipo_visitante": "Los Leones",
            "fecha_hora": "2024-01-15T15:00:00Z"
        }
    ]
}
```

### 25. Obtener Equipos por Disciplina
- **Endpoint**: `GET /partidos/api/equipos-disciplina/{disciplina_id}/`
- **Query Parameters**:
  - `categoria`: masculino, femenino, mixto (opcional)
- **Example**: `GET /partidos/api/equipos-disciplina/1/?categoria=masculino`

## POSTS (Blog/Noticias)

### 26. Listar Posts
- **Endpoint**: `GET /usuarios/api/posts/`

### 27. Crear Post
- **Endpoint**: `POST /usuarios/api/posts/`
- **JSON Request**:
```json
{
    "titulo": "Inicio del Torneo 2024",
    "contenido": "El torneo universitario inicia el próximo lunes...",
    "autor": 1
}
```

## ADMINISTRACIÓN

### 28. Listar Administrativos
- **Endpoint**: `GET /usuarios/api/administrativos/`
- **Requiere**: Permisos de administrador

### 29. Crear Administrativo
- **Endpoint**: `POST /usuarios/api/administrativos/`
- **JSON Request**:
```json
{
    "username": "admin2",
    "password": "123456",
    "email": "admin2@uab.edu.bo",
    "first_name": "Admin",
    "last_name": "Segundo",
    "perfil": {
        "rol": "admin"
    }
}
```

## BÚSQUEDA Y FILTROS

### 30. Buscar Usuarios (Admin)
- **Endpoint**: `GET /usuarios/admin/usuarios/buscar/`
- **Query Parameters**: `q` (término de búsqueda)
- **Example**: `GET /usuarios/admin/usuarios/buscar/?q=juan`

## CÓDIGOS DE ESTADO HTTP

- `200`: OK - Solicitud exitosa
- `201`: Created - Recurso creado exitosamente
- `400`: Bad Request - Error en los datos enviados
- `401`: Unauthorized - No autenticado
- `403`: Forbidden - Sin permisos
- `404`: Not Found - Recurso no encontrado
- `500`: Internal Server Error - Error del servidor

## NOTAS IMPORTANTES

1. **Autenticación**: La mayoría de endpoints requieren autenticación. Usa el endpoint de login primero.

2. **Headers**: Incluye siempre `Content-Type: application/json` en tus requests POST/PUT.

3. **CSRF**: Si usas las vistas web, necesitarás el token CSRF.

4. **Paginación**: Las listas grandes pueden estar paginadas.

5. **Validaciones**: Los campos tienen validaciones específicas (ej: email válido, username único).

6. **Imágenes**: Para subir imágenes, usa `multipart/form-data` en lugar de JSON.

## COLECCIÓN POSTMAN

Puedes importar esta estructura a Postman creando requests con:
- Método HTTP correcto (GET, POST, PUT, DELETE)
- URL completa (`http://localhost:8000` + endpoint)
- Headers apropiados
- Body en formato JSON (para POST/PUT)

### Ejemplo de Headers en Postman:
```
Content-Type: application/json
Accept: application/json
```

### Variables de Entorno en Postman:
- `base_url`: `http://localhost:8000`
- `auth_token`: (obtener del login)
