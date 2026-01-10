# Script para eliminar console.logs que causan bucle infinito

$files = @(
    "e:\TESLA_COTIZADOR-V3.0\frontend\src\App.jsx",
    "e:\TESLA_COTIZADOR-V3.0\frontend\src\components\VistaPreviaProfesional.jsx",
    "e:\TESLA_COTIZADOR-V3.0\frontend\src\components\EDITABLE_PROYECTO_COMPLEJO.jsx"
)

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    
    # Eliminar console.logs específicos
    $content = $content -replace "console\.log\('🔄 App\.jsx: Actualizando datosEditables desde Vista Previa'[^\)]*\);?\r?\n?", ""
    $content = $content -replace "console\.log\('🎬 VistaPreviaProfesional RENDERIZANDO'\);?\r?\n?", ""
    $content = $content -replace "console\.log\('📦 Props:'[^\)]*\);?\r?\n?", ""
    $content = $content -replace "console\.log\('🎨 Renderizando componente para tipo:'[^\)]*\);?\r?\n?", ""
    $content = $content -replace "console\.log\('✅ Renderizando EDITABLE_PROYECTO_COMPLEJO'\);?\r?\n?", ""
    $content = $content -replace "console\.log\('📝 Datos actualizados desde componente EDITABLE:'[^\)]*\);?\r?\n?", ""
    $content = $content -replace "console\.log\('🔍 SINCRONIZANDO DATOS DEL CHATBOT:'[^\)]*\);?\r?\n?", ""
    $content = $content -replace "console\.log\('🔍 COMPLEJIDAD RECIBIDA:'[^\)]*\);?\r?\n?", ""
    $content = $content -replace "console\.log\('🔍 FASES RECIBIDAS:'[^\)]*\);?\r?\n?", ""
    
    Set-Content $file $content -NoNewline
    Write-Host "✅ Limpiado: $file"
}

Write-Host "`n✅ Todos los console.logs eliminados"
