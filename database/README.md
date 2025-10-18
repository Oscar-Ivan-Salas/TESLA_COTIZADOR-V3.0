# Database - Tesla Cotizador V3

Scripts SQL y migraciones de la base de datos PostgreSQL.

## 📁 Estructura
```
database/
├── init.sql           # Script de inicialización
├── migrations/        # Migraciones versionadas
│   └── README.md
└── README.md         # Este archivo
```

## 🚀 Inicialización

### Con Docker
```bash
# Automático al ejecutar docker-compose up
docker-compose up -d
```

### Manual
```bash
# Crear base de datos
psql -U postgres -f init.sql

# Verificar
psql -U postgres -d tesla_cotizador -c "\dt"
```

## 📊 Esquema

### Tablas Principales

- `proyectos` - Proyectos del cliente
- `cotizaciones` - Cotizaciones generadas
- `documentos` - Archivos subidos
- `items` - Items de cotizaciones (opcional)

### Vistas

- `vista_resumen_proyectos` - Resumen con estadísticas
- `vista_estadisticas_cotizaciones` - Métricas de cotizaciones

## 🔄 Migraciones

Ver `/migrations/README.md` para más información sobre cómo crear y aplicar migraciones.

## 🗄️ Backup
```bash
# Crear backup
pg_dump -U postgres tesla_cotizador > backup_$(date +%Y%m%d).sql

# Restaurar
psql -U postgres tesla_cotizador < backup_20250118.sql
```