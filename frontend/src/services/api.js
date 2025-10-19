/**
 * Módulo de API para interactuar con el backend de Tesla Cotizador.
 */

/**
 * Descarga un informe (PDF o DOCX) de una cotización.
 *
 * @param {number} cotizacionId - El ID de la cotización.
 * @param {'pdf' | 'word'} formato - El formato del archivo a descargar.
 * @returns {Promise<{success: boolean, message: string}>} - Un objeto indicando si la descarga fue exitosa.
 */
export const descargarInforme = async (cotizacionId, formato) => {
  if (!cotizacionId) {
    return { success: false, message: 'ID de cotización no válido.' };
  }

  const endpoint = `/api/informes/generar-${formato}/${cotizacionId}`;

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
    });

    if (!response.ok) {
      let errorMessage;
      // Clone the response so we can read it twice
      const clonedResponse = response.clone();
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || JSON.stringify(errorData);
      } catch (e) {
        errorMessage = await clonedResponse.text();
      }
      throw new Error(errorMessage);
    }

    // Obtener el nombre del archivo del header Content-Disposition
    const disposition = response.headers.get('content-disposition');
    let nombreArchivo = `cotizacion-${cotizacionId}.${formato === 'word' ? 'docx' : 'pdf'}`;
    if (disposition && disposition.indexOf('attachment') !== -1) {
      const filenameRegex = /filename[^;=\n]*=((['"])(.*?)\2|[^;\n]*)/;
      const matches = filenameRegex.exec(disposition);
      if (matches != null && matches[3]) {
        nombreArchivo = matches[3];
      }
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = nombreArchivo;
    document.body.appendChild(a);
    a.click();
    
    // Limpieza
    a.remove();
    window.URL.revokeObjectURL(url);

    return { success: true, message: `Descargando ${nombreArchivo}` };

  } catch (error) {
    console.error(`Error al descargar el informe (${formato}):`, error);
    return { success: false, message: error.message || 'No se pudo iniciar la descarga.' };
  }
};