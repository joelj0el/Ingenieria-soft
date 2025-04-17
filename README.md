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
