# SOLUCIÓN AL ERROR 422 - Items Vacíos

## Problema
El frontend intenta guardar la cotización en la base de datos antes de generar el documento, pero el array de `items` está vacío, causando error 422.

## Solución Temporal (Prueba Rápida)
Para probar la generación de documentos ahora mismo, usa este comando en PowerShell:

```powershell
$body = @{
    cliente = "Cliente de Prueba"
    proyecto = "Instalación Eléctrica Residencial"
    descripcion = "Instalación completa para casa de 150m2"
    items = @(
        @{
            descripcion = "Punto de luz LED 18W"
            cantidad = 15
            unidad = "und"
            precio_unitario = 25.0
        },
        @{
            descripcion = "Tomacorriente doble con tierra"
            cantidad = 12
            unidad = "und"
            precio_unitario = 35.0
        },
        @{
            descripcion = "Interruptor simple"
            cantidad = 8
            unidad = "und"
            precio_unitario = 18.0
        }
    )
    subtotal = 939.0
    igv = 169.02
    total = 1108.02
    observaciones = "Precios incluyen IGV"
    vigencia = "30 días"
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri "http://localhost:8000/api/generar-documento-directo?formato=word" -Method POST -Body $body -ContentType "application/json" -OutFile "cotizacion_prueba.docx"
```

Esto descargará un archivo Word válido llamado `cotizacion_prueba.docx`.

Para PDF, cambia `formato=word` por `formato=pdf` y el nombre del archivo a `.pdf`.

## Solución Permanente (Requiere Edición de Código)
El frontend necesita modificarse para usar el endpoint de generación directa cuando no hay ID.

Archivo a modificar: `frontend/src/App.jsx`
Líneas: 559-621 (función `handleDescargar`)

El cambio es reemplazar el flujo "guardar primero, luego generar" por "generar directamente si no hay ID".

¿Quieres que te dé las instrucciones detalladas para el cambio permanente?
