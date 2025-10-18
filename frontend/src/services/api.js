const API_URL = 'http://localhost:8000/api';

// Helper para manejar respuestas
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ 
      detail: 'Error en la solicitud' 
    }));
    throw new Error(error.detail || 'Error en la solicitud');
  }
  return response.json();
};

// ============================================
// COTIZACIONES
// ============================================

export const crearCotizacion = async (datos) => {
  const response = await fetch(`${API_URL}/cotizaciones/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(datos)
  });
  return handleResponse(response);
};

export const obtenerCotizaciones = async () => {
  const response = await fetch(`${API_URL}/cotizaciones/`);
  return handleResponse(response);
};

export const obtenerCotizacion = async (id) => {
  const response = await fetch(`${API_URL}/cotizaciones/${id}`);
  return handleResponse(response);
};

export const actualizarCotizacion = async (id, datos) => {
  const response = await fetch(`${API_URL}/cotizaciones/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(datos)
  });
  return handleResponse(response);
};

export const eliminarCotizacion = async (id) => {
  const response = await fetch(`${API_URL}/cotizaciones/${id}`, {
    method: 'DELETE'
  });
  return handleResponse(response);
};

// ============================================
// PROYECTOS
// ============================================

export const crearProyecto = async (datos) => {
  const response = await fetch(`${API_URL}/proyectos/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(datos)
  });
  return handleResponse(response);
};

export const obtenerProyectos = async () => {
  const response = await fetch(`${API_URL}/proyectos/`);
  return handleResponse(response);
};

export const obtenerProyecto = async (id) => {
  const response = await fetch(`${API_URL}/proyectos/${id}`);
  return handleResponse(response);
};

export const actualizarProyecto = async (id, datos) => {
  const response = await fetch(`${API_URL}/proyectos/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(datos)
  });
  return handleResponse(response);
};

// ============================================
// DOCUMENTOS (Upload y procesamiento)
// ============================================

export const subirDocumento = async (archivo) => {
  const formData = new FormData();
  formData.append('file', archivo);

  const response = await fetch(`${API_URL}/documentos/upload`, {
    method: 'POST',
    body: formData
  });
  return handleResponse(response);
};

export const procesarDocumento = async (archivoId) => {
  const response = await fetch(`${API_URL}/documentos/${archivoId}/procesar`, {
    method: 'POST'
  });
  return handleResponse(response);
};

export const obtenerDocumentos = async (proyectoId) => {
  const response = await fetch(`${API_URL}/documentos/?proyecto_id=${proyectoId}`);
  return handleResponse(response);
};

// ============================================
// CHAT IA (Gemini)
// ============================================

export const enviarMensajeChat = async (mensajes, contexto = {}) => {
  const response = await fetch(`${API_URL}/chat/generar-cotizacion`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      mensajes,
      contexto
    })
  });
  return handleResponse(response);
};

export const generarCotizacionIA = async (descripcion, documentos = []) => {
  const response = await fetch(`${API_URL}/chat/generar-cotizacion-rapida`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      descripcion,
      documentos
    })
  });
  return handleResponse(response);
};

// ============================================
// INFORMES (Generación de documentos)
// ============================================

export const generarPDF = async (cotizacionId) => {
  const response = await fetch(`${API_URL}/informes/generar-pdf/${cotizacionId}`, {
    method: 'POST'
  });
  
  if (!response.ok) {
    throw new Error('Error al generar PDF');
  }
  
  // Descargar archivo
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `cotizacion_${cotizacionId}.pdf`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
  
  return { success: true };
};

export const generarWord = async (cotizacionId) => {
  const response = await fetch(`${API_URL}/informes/generar-word/${cotizacionId}`, {
    method: 'POST'
  });
  
  if (!response.ok) {
    throw new Error('Error al generar Word');
  }
  
  // Descargar archivo
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `cotizacion_${cotizacionId}.docx`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
  
  return { success: true };
};

export const generarInformeEjecutivo = async (proyectoId, opciones = {}) => {
  const response = await fetch(`${API_URL}/informes/generar-informe-ejecutivo/${proyectoId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(opciones)
  });
  
  if (!response.ok) {
    throw new Error('Error al generar informe');
  }
  
  // Descargar archivo
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `informe_ejecutivo_${proyectoId}.docx`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
  
  return { success: true };
};

// ============================================
// BÚSQUEDA Y RAG
// ============================================

export const buscarEnDocumentos = async (query, proyectoId = null) => {
  const params = new URLSearchParams({ query });
  if (proyectoId) params.append('proyecto_id', proyectoId);
  
  const response = await fetch(`${API_URL}/documentos/buscar?${params}`);
  return handleResponse(response);
};

// ============================================
// UTILIDADES
// ============================================

export const verificarConexion = async () => {
  try {
    const response = await fetch(`${API_URL}/health`);
    return response.ok;
  } catch (error) {
    return false;
  }
};

export default {
  // Cotizaciones
  crearCotizacion,
  obtenerCotizaciones,
  obtenerCotizacion,
  actualizarCotizacion,
  eliminarCotizacion,
  
  // Proyectos
  crearProyecto,
  obtenerProyectos,
  obtenerProyecto,
  actualizarProyecto,
  
  // Documentos
  subirDocumento,
  procesarDocumento,
  obtenerDocumentos,
  
  // Chat IA
  enviarMensajeChat,
  generarCotizacionIA,
  
  // Informes
  generarPDF,
  generarWord,
  generarInformeEjecutivo,
  
  // Búsqueda
  buscarEnDocumentos,
  
  // Utilidades
  verificarConexion
};
