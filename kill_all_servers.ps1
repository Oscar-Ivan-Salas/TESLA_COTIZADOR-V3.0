# Script para matar todos los procesos Python y Node
Write-Host "🔍 Buscando procesos Python y Node..." -ForegroundColor Yellow

$pythonProcesses = Get-Process | Where-Object {$_.ProcessName -like "*python*"}
$nodeProcesses = Get-Process | Where-Object {$_.ProcessName -like "*node*"}

Write-Host "`n📋 Procesos Python encontrados: $($pythonProcesses.Count)" -ForegroundColor Cyan
$pythonProcesses | ForEach-Object {
    Write-Host "  - PID: $($_.Id) | Tiempo: $((Get-Date) - $_.StartTime)" -ForegroundColor Gray
}

Write-Host "`n📋 Procesos Node encontrados: $($nodeProcesses.Count)" -ForegroundColor Cyan
$nodeProcesses | ForEach-Object {
    Write-Host "  - PID: $($_.Id) | Tiempo: $((Get-Date) - $_.StartTime)" -ForegroundColor Gray
}

Write-Host "`n💀 Matando todos los procesos Python..." -ForegroundColor Red
$pythonProcesses | ForEach-Object {
    try {
        Stop-Process -Id $_.Id -Force
        Write-Host "  ✅ Proceso $($_.Id) terminado" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Error matando proceso $($_.Id): $_" -ForegroundColor Red
    }
}

Write-Host "`n💀 Matando todos los procesos Node..." -ForegroundColor Red
$nodeProcesses | ForEach-Object {
    try {
        Stop-Process -Id $_.Id -Force
        Write-Host "  ✅ Proceso $($_.Id) terminado" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Error matando proceso $($_.Id): $_" -ForegroundColor Red
    }
}

Write-Host "`n⏳ Esperando 3 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "`n🔍 Verificando que no queden procesos..." -ForegroundColor Yellow
$remaining = Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*node*"}
if ($remaining.Count -eq 0) {
    Write-Host "✅ TODOS LOS PROCESOS ELIMINADOS" -ForegroundColor Green
} else {
    Write-Host "⚠️ Aún quedan $($remaining.Count) procesos:" -ForegroundColor Yellow
    $remaining | ForEach-Object {
        Write-Host "  - $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
    }
}

Write-Host "`n✅ Limpieza completada. Ahora puedes iniciar los servidores frescos." -ForegroundColor Green
