/**
 * Servicio de API para Tesla Cotizador v3.0
 * 
 * CONFIGURACIÓN ACTUALIZADA para trabajar con los nuevos endpoints
 */

// Configuración de la URL base del backend
// Nota: No incluir '/api' al final ya que se agrega en cada endpoint
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Helper para manejar respuestas de la API
 */
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || `HTTP Error: ${response.status}`);
  }
  
  // Si es un archivo (blob), retornarlo directamente
  const contentType = response.headers.get('content-type');
  if (contentType && (
    contentType.includes('application/pdf') ||
    contentType.includes('application/vnd.openxmlformats') ||
    contentType.includes('application/msword')
  )) {
    return response.blob();
  }
  
  // Si es JSON, parsearlo
  if (contentType && contentType.includes('application/json')) {
    return response.json();
  }
  
  return response.text();
};

/**
 * Helper para descargar archivos
 */
const downloadFile = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
};

// ═══════════════════════════════════════════════════════════
// ENDPOINTS DE COTIZACIONES
// ═══════════════════════════════════════════════════════════

export const cotizacionesAPI = {
  /**
   * Listar cotizaciones
   */
  listar: async (params = {}) => {
    const queryParams = new URLSearchParams(params).toString();
    const url = `${API_BASE_URL}/api/cotizaciones?${queryParams}`;
    
    const response = await fetch(url);
    return handleResponse(response);
  },

  /**
   * Obtener una cotización por ID
   */
  obtener: async (id) => {
    const response = await fetch(`${API_BASE_URL}/api/cotizaciones/${id}`);
    return handleResponse(response);
  },

  /**
   * Crear nueva cotización
   */
  crear: async (data) => {
    const response = await fetch(`${API_BASE_URL}/api/cotizaciones`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * Actualizar cotización
   */
  actualizar: async (id, data) => {
    const response = await fetch(`${API_BASE_URL}/api/cotizaciones/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * Eliminar cotización
   */
  eliminar: async (id) => {
    const response = await fetch(`${API_BASE_URL}/api/cotizaciones/${id}`, {
      method: 'DELETE',
    });
    return handleResponse(response);
  },

  /**
   * NUEVO: Generar documento Word de cotización
   */
  generarWord: async (id, opciones = {}) => {
    try {
      console.log(`Generando Word para cotización ${id}...`);
      
      const response = await fetch(
        `${API_BASE_URL}/api/cotizaciones/${id}/generar-word`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(opciones),
        }
      );

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }

      const contentDisposition = response.headers.get('content-disposition');
      let filename = `cotizacion_${id}_${new Date().getTime()}.docx`; // fallback
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch && filenameMatch.length > 1) {
          filename = filenameMatch[1];
        }
      }

      const blob = await response.blob();
      downloadFile(blob, filename);
      
      console.log(`✅ Word generado: ${filename}`);
      return { success: true, filename };
      
    } catch (error) {
      console.error('Error al generar Word:', error);
      throw error;
    }
  },

  /**
   * NUEVO: Generar documento PDF de cotización
   */
  generarPDF: async (id, opciones = {}) => {
    try {
      console.log(`Generando PDF para cotización ${id}...`);
      
      const response = await fetch(
        `${API_BASE_URL}/api/cotizaciones/${id}/generar-pdf`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(opciones),
        }
      );

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }

      const contentDisposition = response.headers.get('content-disposition');
      let filename = `cotizacion_${id}_${new Date().getTime()}.pdf`; // fallback
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch && filenameMatch.length > 1) {
          filename = filenameMatch[1];
        }
      }

      const blob = await response.blob();
      downloadFile(blob, filename);
      
      console.log(`✅ PDF generado: ${filename}`);
      return { success: true, filename };
      
    } catch (error) {
      console.error('Error al generar PDF:', error);
      throw error;
    }
  },
};

// ═══════════════════════════════════════════════════════════
// ENDPOINTS DE PROYECTOS
// ═══════════════════════════════════════════════════════════

export const proyectosAPI = {
  /**
   * Listar proyectos
   */
  listar: async (params = {}) => {
    const queryParams = new URLSearchParams(params).toString();
    const url = `${API_BASE_URL}/api/proyectos?${queryParams}`;
    
    const response = await fetch(url);
    return handleResponse(response);
  },

  /**
   * Obtener proyecto por ID
   */
  obtener: async (id) => {
    const response = await fetch(`${API_BASE_URL}/api/proyectos/${id}`);
    return handleResponse(response);
  },

  /**
   * Crear nuevo proyecto
   */
  crear: async (data) => {
    const response = await fetch(`${API_BASE_URL}/api/proyectos`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * NUEVO: Obtener análisis IA del proyecto
   */
  obtenerAnalisisIA: async (id) => {
    try {
      console.log(`Obteniendo análisis IA para proyecto ${id}...`);
      
      const response = await fetch(
        `${API_BASE_URL}/api/proyectos/${id}/analisis-ia`
      );

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }

      const data = await response.json();
      console.log('✅ Análisis IA obtenido');
      return data;
      
    } catch (error) {
      console.error('Error al obtener análisis IA:', error);
      throw error;
    }
  },

  /**
   * NUEVO: Generar informe de proyecto en Word
   */
  generarInformeWord: async (id, opciones = {}) => {
    try {
      console.log(`Generando informe Word para proyecto ${id}...`);
      
      const defaultOpciones = {
        incluir_cotizaciones: true,
        incluir_documentos: true,
        incluir_estadisticas: true,
        incluir_analisis_ia: true, // ⭐ ACTIVAR ANÁLISIS IA
        ...opciones
      };
      
      const response = await fetch(
        `${API_BASE_URL}/api/proyectos/${id}/generar-informe-word`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(defaultOpciones),
        }
      );

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }

      const contentDisposition = response.headers.get('content-disposition');
      let filename = `informe_proyecto_${id}_${new Date().getTime()}.docx`; // fallback
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch && filenameMatch.length > 1) {
          filename = filenameMatch[1];
        }
      }

      const blob = await response.blob();
      downloadFile(blob, filename);
      
      console.log(`✅ Informe Word generado: ${filename}`);
      return { success: true, filename };
      
    } catch (error) {
      console.error('Error al generar informe Word:', error);
      throw error;
    }
  },

  /**
   * NUEVO: Generar informe de proyecto en PDF
   */
  generarInformePDF: async (id, opciones = {}) => {
    try {
      console.log(`Generando informe PDF para proyecto ${id}...`);
      
      const defaultOpciones = {
        incluir_cotizaciones: true,
        incluir_documentos: true,
        incluir_estadisticas: true,
        incluir_analisis_ia: true, // ⭐ ACTIVAR ANÁLISIS IA
        ...opciones
      };
      
      const response = await fetch(
        `${API_BASE_URL}/api/proyectos/${id}/generar-informe-pdf`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(defaultOpciones),
        }
      );

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }

      const contentDisposition = response.headers.get('content-disposition');
      let filename = `informe_proyecto_${id}_${new Date().getTime()}.pdf`; // fallback
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch && filenameMatch.length > 1) {
          filename = filenameMatch[1];
        }
      }

      const blob = await response.blob();
      downloadFile(blob, filename);
      
      console.log(`✅ Informe PDF generado: ${filename}`);
      return { success: true, filename };
      
    } catch (error) {
      console.error('Error al generar informe PDF:', error);
      throw error;
    }
  },
};

// ═══════════════════════════════════════════════════════════
// ENDPOINTS DE DOCUMENTOS
// ═══════════════════════════════════════════════════════════

export const documentosAPI = {
  /**
   * Subir documento
   */
  subir: async (file, proyectoId = null) => {
    const formData = new FormData();
    formData.append('archivo', file);
    if (proyectoId) {
      formData.append('proyecto_id', proyectoId);
    }

    const response = await fetch(`${API_BASE_URL}/api/documentos/upload`, {
      method: 'POST',
      body: formData,
    });

    return handleResponse(response);
  },

  /**
   * Listar documentos
   */
  listar: async (params = {}) => {
    const queryParams = new URLSearchParams(params).toString();
    const url = `${API_BASE_URL}/api/documentos?${queryParams}`;
    
    const response = await fetch(url);
    return handleResponse(response);
  },

  /**
   * NUEVO: Generar informe de análisis en Word
   */
  generarInformeAnalisisWord: async (id, opciones = {}) => {
    try {
      console.log(`Generando informe de análisis Word para documento ${id}...`);
      
      const response = await fetch(
        `${API_BASE_URL}/api/documentos/${id}/generar-informe-analisis-word`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(opciones),
        }
      );

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }

      const contentDisposition = response.headers.get('content-disposition');
      let filename = `analisis_documento_${id}_${new Date().getTime()}.docx`; // fallback
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch && filenameMatch.length > 1) {
          filename = filenameMatch[1];
        }
      }

      const blob = await response.blob();
      downloadFile(blob, filename);
      
      console.log(`✅ Informe de análisis generado: ${filename}`);
      return { success: true, filename };
      
    } catch (error) {
      console.error('Error al generar informe de análisis:', error);
      throw error;
    }
  },

  /**
   * NUEVO: Generar informe de análisis en PDF
   */
  generarInformeAnalisisPDF: async (id, opciones = {}) => {
    try {
      console.log(`Generando informe de análisis PDF para documento ${id}...`);
      
      const response = await fetch(
        `${API_BASE_URL}/api/documentos/${id}/generar-informe-analisis-pdf`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(opciones),
        }
      );

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }

      const contentDisposition = response.headers.get('content-disposition');
      let filename = `analisis_documento_${id}_${new Date().getTime()}.pdf`; // fallback
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch && filenameMatch.length > 1) {
          filename = filenameMatch[1];
        }
      }

      const blob = await response.blob();
      downloadFile(blob, filename);
      
      console.log(`✅ Informe de análisis PDF generado: ${filename}`);
      return { success: true, filename };
      
    } catch (error) {
      console.error('Error al generar informe de análisis PDF:', error);
      throw error;
    }
  },
};

// ═══════════════════════════════════════════════════════════
// ENDPOINTS DE PLANTILLAS (CHAT)
// ═══════════════════════════════════════════════════════════

export const plantillasAPI = {
  /**
   * NUEVO: Subir plantilla
   */
  subir: async (file, nombrePlantilla, descripcion = '') => {
    try {
      const formData = new FormData();
      formData.append('archivo', file);
      formData.append('nombre_plantilla', nombrePlantilla);
      formData.append('descripcion', descripcion);

      const response = await fetch(`${API_BASE_URL}/api/chat/subir-plantilla`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }

      return response.json();
    } catch (error) {
      console.error('Error al subir plantilla:', error);
      throw error;
    }
  },

  /**
   * NUEVO: Listar plantillas
   */
  listar: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/listar-plantillas`);
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }

      return response.json();
    } catch (error) {
      console.error('Error al listar plantillas:', error);
      throw error;
    }
  },

  /**
   * NUEVO: Usar plantilla en cotización
   */
  usarEnCotizacion: async (cotizacionId, nombrePlantilla, opciones = {}) => {
    try {
      console.log(`Usando plantilla ${nombrePlantilla} en cotización ${cotizacionId}...`);
      
      const response = await fetch(
        `${API_BASE_URL}/api/chat/usar-plantilla/${cotizacionId}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            nombre_plantilla: nombrePlantilla,
            ...opciones
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }

      const contentDisposition = response.headers.get('content-disposition');
      let filename = `cotizacion_${cotizacionId}_${new Date().getTime()}.docx`; // fallback
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch && filenameMatch.length > 1) {
          filename = filenameMatch[1];
        }
      }

      const blob = await response.blob();
      downloadFile(blob, filename);
      
      console.log(`✅ Cotización generada con plantilla: ${filename}`);
      return { success: true, filename };
      
    } catch (error) {
      console.error('Error al usar plantilla:', error);
      throw error;
    }
  },

  /**
   * NUEVO: Validar plantilla
   */
  validar: async (file) => {
    try {
      const formData = new FormData();
      formData.append('archivo', file);

      const response = await fetch(`${API_BASE_URL}/api/chat/validar-plantilla`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }

      return response.json();
    } catch (error) {
      console.error('Error al validar plantilla:', error);
      throw error;
    }
  },
};

// ═══════════════════════════════════════════════════════════
// FUNCIÓN DE COMPATIBILIDAD (para código antiguo)
// ═══════════════════════════════════════════════════════════

/**
 * @deprecated Usa api.cotizaciones.generarWord() o api.cotizaciones.generarPDF()
 * Esta función existe solo para mantener compatibilidad con código antiguo
 * Acepta parámetros en cualquier orden (detecta automáticamente)
 */
export const descargarInforme = async (param1, param2) => {
  console.warn('⚠️ descargarInforme() está deprecado. Usa api.cotizaciones.generarWord() o generarPDF()');
  
  // Detectar automáticamente cuál es el tipo y cuál es el ID
  let tipo, cotizacionId;
  
  if (typeof param1 === 'string' && (param1 === 'word' || param1 === 'pdf')) {
    tipo = param1;
    cotizacionId = param2;
  } else if (typeof param2 === 'string' && (param2 === 'word' || param2 === 'pdf')) {
    tipo = param2;
    cotizacionId = param1;
  } else {
    throw new Error(`Parámetros inválidos. Debes pasar 'word' o 'pdf' y un ID numérico. Recibido: ${param1}, ${param2}`);
  }
  
  console.log(`📄 Generando documento ${tipo.toUpperCase()} para cotización ${cotizacionId}`);
  
  if (tipo === 'word') {
    return await cotizacionesAPI.generarWord(cotizacionId);
  } else if (tipo === 'pdf') {
    return await cotizacionesAPI.generarPDF(cotizacionId);
  }
};

// ═══════════════════════════════════════════════════════════
// EXPORTACIÓN POR DEFECTO
// ═══════════════════════════════════════════════════════════

export default {
  cotizaciones: cotizacionesAPI,
  proyectos: proyectosAPI,
  documentos: documentosAPI,
  plantillas: plantillasAPI,
};