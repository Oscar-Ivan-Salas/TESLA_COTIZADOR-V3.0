# Migraciones de Base de Datos

Este directorio contiene las migraciones de la base de datos para Tesla Cotizador.

## Convención de nombres

Las migraciones siguen el formato:
```
YYYYMMDD_HHMMSS_descripcion.sql
```

Ejemplo:
```
20250118_120000_crear_tabla_usuarios.sql
20250118_130000_agregar_campo_email.sql
```

## Orden de ejecución

Las migraciones se ejecutan en orden cronológico según su timestamp.

## Crear una nueva migración

1. Crear archivo con timestamp actual
2. Escribir SQL para cambios
3. Incluir instrucciones de rollback (opcional)

## Ejemplo de migración
```sql
-- Migración: 20250118_120000_ejemplo.sql
-- Descripción: Agrega campo nuevo a tabla

-- UP
ALTER TABLE cotizaciones ADD COLUMN campo_nuevo VARCHAR(100);

-- DOWN (rollback)
-- ALTER TABLE cotizaciones DROP COLUMN campo_nuevo;
```