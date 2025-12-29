// ============================================
// NUEVA FUNCIÓN handleDescargar - Usar api.js
// ============================================
// Reemplazar la función handleDescargar existente (líneas 531-653) con esta versión:

const handleDescargar = async (formato) => {
    const tipoDocumento = tipoFlujo.includes('cotizacion') ? 'cotizacion' :
        tipoFlujo.includes('proyecto') ? 'proyecto' : 'informe';

    const entidad = tipoDocumento === 'cotizacion' ? cotizacion :
        tipoDocumento === 'proyecto' ? proyecto : informe;

    if (!entidad && !datosEditables) {
        setError(`No hay ${tipoDocumento} para descargar`);
        return;
    }

    setDescargando(formato);
    setError('');
    setExito('');

    try {
        // Determinar entidad según tipo de documento
        const entidadActual = tipoDocumento === 'cotizacion' ? cotizacion :
            tipoDocumento === 'proyecto' ? proyecto : informe;

        // Usar datos editables si existen, sino usar entidad del tipo correcto
        const datosFinales = datosEditables || entidadActual;

        // Preparar datos completos para generación directa
        let datosParaGenerar = { ...datosFinales };

        // Asegurar que los datos tengan la estructura correcta
        if (tipoDocumento === 'cotizacion') {
            const totales = calcularTotales(datosFinales?.items || []);
            datosParaGenerar = {
                ...datosParaGenerar,
                cliente: clienteProyecto || 'Cliente',
                proyecto: nombreProyecto || 'Proyecto',
                descripcion: contextoUsuario || '',
                items: datosFinales?.items || [],
                subtotal: parseFloat(totales.subtotal),
                igv: parseFloat(totales.igv),
                total: parseFloat(ocultarIGV ? totales.subtotal : totales.total),
                observaciones: '',
                vigencia: '30 días',
                html_preview: htmlPreview
            };
        } else if (tipoDocumento === 'proyecto') {
            datosParaGenerar = {
                ...datosParaGenerar,
                nombre: nombreProyecto || 'Proyecto',
                cliente: clienteProyecto || 'Cliente',
                tipo: servicioSeleccionado || 'general',
                presupuesto_estimado: parseFloat(presupuestoEstimado) || 0,
                duracion_meses: parseInt(duracionMeses) || 1,
                descripcion: contextoUsuario || '',
                html_preview: htmlPreview
            };
        } else if (tipoDocumento === 'informe') {
            datosParaGenerar = {
                ...datosParaGenerar,
                proyecto_id: proyectoSeleccionado || 'general',
                tipo: tipoFlujo.includes('ejecutivo') ? 'ejecutivo' : 'simple',
                formato: formatoInforme || 'word',
                incluir_graficos: incluirGraficos,
                contenido: contextoUsuario || '',
                html_preview: htmlPreview
            };
        }

        // Agregar logo si existe
        if (logoBase64) {
            datosParaGenerar.logo_base64 = logoBase64;
        }

        console.log(`📄 Generando ${formato.toUpperCase()} vía API Directa...`);
        setExito(`Generando ${formato.toUpperCase()}...`);

        // Usar servicios de API centralizados
        // api.js detectará automáticamente que es un objeto y usará generación directa
        let resultado;

        if (tipoDocumento === 'cotizacion') {
            if (formato === 'word') {
                resultado = await cotizacionesAPI.generarWord(datosParaGenerar);
            } else {
                resultado = await cotizacionesAPI.generarPDF(datosParaGenerar);
            }
        } else if (tipoDocumento === 'proyecto') {
            if (formato === 'word') {
                resultado = await proyectosAPI.generarInformeWord(datosParaGenerar);
            } else {
                resultado = await proyectosAPI.generarInformePDF(datosParaGenerar);
            }
        } else {
            // Informes
            if (formato === 'word') {
                resultado = await cotizacionesAPI.generarDocumentoDirecto(datosParaGenerar, 'word');
            } else {
                resultado = await cotizacionesAPI.generarDocumentoDirecto(datosParaGenerar, 'pdf');
            }
        }

        if (resultado && resultado.success) {
            setExito(`✅ ${formato.toUpperCase()} descargado exitosamente`);
            setTimeout(() => setExito(''), 4000);
        } else {
            throw new Error("No se pudo iniciar la descarga");
        }

    } catch (error) {
        console.error('Error al descargar:', error);
        setError(`Error al generar el documento: ${error.message}`);
    } finally {
        setDescargando(null);
    }
};
