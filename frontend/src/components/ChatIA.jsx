import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader, User, Bot, Zap, FileText, Upload, Download } from 'lucide-react';

/**
 * 🎯 ChatIA.jsx - INTEGRADO CON MULTI-IA TESLA COTIZADOR V3.0
 * 
 * Este componente SE INTEGRA con la arquitectura existente:
 * ✅ Usa endpoint /api/chat/chat-contextualizado (CORRECTO)
 * ✅ Maneja los 6 tipos de flujo (cotización/proyecto/informe simple/complejo) 
 * ✅ Sistema Multi-IA con fallback automático a PILIBrain
 * ✅ Especialización PILI expandida (no solo ITSE, ahora 6 documentos)
 * ✅ Compatible con App_TESLA_COMPLETO.jsx existente
 */
const ChatIA = ({
  tipoFlujo = 'cotizacion-simple',  // cotizacion-simple/compleja, proyecto-simple/complejo, informe-simple/ejecutivo
  contexto = {},                    // Datos del formulario (servicio, industria, etc.)
  archivos = [],                    // Archivos subidos
  onCotizacionGenerada,             // Callback cuando se genera cotización
  onProyectoGenerado,              // Callback cuando se genera proyecto  
  onInformeGenerado,               // Callback cuando se genera informe
  onHtmlPreviewGenerado,           // Callback cuando se genera HTML preview editable
  onConversacionUpdate             // Callback para actualizar conversación en componente padre
}) => {
  const [conversacion, setConversacion] = useState([]);
  const [inputChat, setInputChat] = useState('');
  const [analizando, setAnalizando] = useState(false);
  const [sistemaActivo, setSistemaActivo] = useState(true);
  const [proveedorActual, setProveedorActual] = useState('Verificando...');
  const messagesEndRef = useRef(null);

  // Colores según tipo de flujo
  const colores = {
    'cotizacion-simple': { primary: 'yellow', bg: 'yellow-600' },
    'cotizacion-compleja': { primary: 'yellow', bg: 'yellow-600' },
    'proyecto-simple': { primary: 'blue', bg: 'blue-600' },
    'proyecto-complejo': { primary: 'blue', bg: 'blue-600' },
    'informe-simple': { primary: 'green', bg: 'green-600' },
    'informe-ejecutivo': { primary: 'green', bg: 'green-600' }
  };
  const color = colores[tipoFlujo] || colores['cotizacion-simple'];

  // Configuración de servicios especializados
  const serviciosConfig = {
    'cotizacion-simple': {
      nombre: '🔥 Cotización Rápida',
      descripcion: 'Proceso simplificado 5-15 minutos',
      especialidad: 'PILI Cotizadora Rápida',
      capacidades: ['Análisis básico', 'Cálculo automático', 'Plantilla estándar']
    },
    'cotizacion-compleja': {
      nombre: '⚙️ Cotización Compleja',
      descripcion: 'Proyectos grandes con análisis detallado',
      especialidad: 'PILI Cotizadora Avanzada',
      capacidades: ['Análisis profundo', 'Múltiples variables', 'Documentación técnica']
    },
    'proyecto-simple': {
      nombre: '📁 Proyecto Simple',
      descripcion: 'Gestión básica y seguimiento',
      especialidad: 'PILI Gestora de Proyectos',
      capacidades: ['Planificación básica', 'Seguimiento simple', 'Reportes estándar']
    },
    'proyecto-complejo': {
      nombre: '🎯 Proyecto Complejo',
      descripcion: 'Con Gantt, hitos y seguimiento avanzado',
      especialidad: 'PILI Project Manager PMI',
      capacidades: ['Metodología PMI', 'Cronograma Gantt', 'Gestión de riesgos']
    },
    'informe-simple': {
      nombre: '📄 Informe Simple',
      descripcion: 'Reporte básico formato estándar',
      especialidad: 'PILI Reportera Técnica',
      capacidades: ['Formato básico', 'Datos técnicos', 'Conclusiones claras']
    },
    'informe-ejecutivo': {
      nombre: '📊 Informe Ejecutivo',
      descripcion: 'Formato APA con gráficos y análisis',
      especialidad: 'PILI Analista Ejecutiva',
      capacidades: ['Formato APA', 'Gráficos avanzados', 'Análisis ejecutivo']
    }
  };

  const servicioActual = serviciosConfig[tipoFlujo];

  // Verificar estado del sistema Multi-IA
  useEffect(() => {
    const verificarSistemaMultiIA = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/chat/pili/estado-ias');
        if (response.ok) {
          const data = await response.json();
          setSistemaActivo(true);
          setProveedorActual(data.proveedores_activos?.[0] || 'PILIBrain Local');
        } else {
          setSistemaActivo(false);
          setProveedorActual('PILIBrain (Offline)');
        }
      } catch (error) {
        setSistemaActivo(false);
        setProveedorActual('PILIBrain (Offline)');
      }
    };

    verificarSistemaMultiIA();

    // Mensaje de bienvenida especializado
    addMessage(
      `¡Hola! Soy **${servicioActual.especialidad}** ⚡

🎯 **Servicio activo:** ${servicioActual.nombre}
${servicioActual.descripcion}

**Mis capacidades especializadas:**
${servicioActual.capacidades.map(cap => `✅ ${cap}`).join('\n')}

**Proveedor IA:** ${proveedorActual}

¿En qué puedo ayudarte con este ${tipoFlujo.includes('cotizacion') ? 'presupuesto' : tipoFlujo.includes('proyecto') ? 'proyecto' : 'informe'}?`,
      'asistente'
    );
  }, [tipoFlujo]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversacion]);

  const addMessage = (mensaje, tipo) => {
    const nuevoMensaje = {
      tipo,
      mensaje,
      timestamp: new Date().toLocaleTimeString()
    };
    setConversacion(prev => [...prev, nuevoMensaje]);

    // Notificar al componente padre si existe el callback
    if (onConversacionUpdate) {
      onConversacionUpdate([...conversacion, nuevoMensaje]);
    }
  };

  // 🎯 FUNCIÓN PRINCIPAL - USA LA MISMA LÓGICA QUE App_TESLA_COMPLETO.jsx
  const handleEnviarMensajeChat = async () => {
    if (!inputChat.trim() || analizando) return;

    const nuevoMensaje = { tipo: 'usuario', mensaje: inputChat };
    const nuevaConversacion = [...conversacion, nuevoMensaje];
    setConversacion(nuevaConversacion);
    setInputChat('');
    setAnalizando(true);

    try {
      // 🔥 PREPARAR CONTEXTO DINÁMICO (IGUAL QUE EN APP_TESLA_COMPLETO.jsx)
      let contextoPrincipal = '';

      if (contexto.servicioSeleccionado) {
        contextoPrincipal += `Servicio: ${contexto.servicioSeleccionado}`;
      }
      if (contexto.industriaSeleccionada) {
        contextoPrincipal += `, Industria: ${contexto.industriaSeleccionada}`;
      }
      if (contexto.contextoUsuario) {
        contextoPrincipal += `, Contexto: ${contexto.contextoUsuario}`;
      }

      // Contexto específico según tipo de flujo
      if (tipoFlujo.includes('proyecto')) {
        if (contexto.nombreProyecto) contextoPrincipal += `, Nombre: ${contexto.nombreProyecto}`;
        if (contexto.clienteProyecto) contextoPrincipal += `, Cliente: ${contexto.clienteProyecto}`;
        if (contexto.presupuestoEstimado) contextoPrincipal += `, Presupuesto: ${contexto.presupuestoEstimado}`;
        if (contexto.duracionMeses) contextoPrincipal += `, Duración: ${contexto.duracionMeses} meses`;
      } else if (tipoFlujo.includes('informe')) {
        if (contexto.proyectoSeleccionado) contextoPrincipal += `, Proyecto: ${contexto.proyectoSeleccionado}`;
        if (contexto.formatoInforme) contextoPrincipal += `, Formato: ${contexto.formatoInforme}`;
      }

      // 🎯 LLAMADA AL ENDPOINT CORRECTO (MULTI-IA CON FALLBACK)
      const response = await fetch('http://localhost:8000/api/chat/chat-contextualizado', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tipo_flujo: tipoFlujo,
          mensaje: inputChat,
          historial: nuevaConversacion,
          contexto_adicional: contextoPrincipal,
          generar_html: true,  // ✅ SOLICITAR DATOS ESTRUCTURADOS
          archivos_procesados: archivos.map(a => ({
            nombre: a.nombre,
            contenido: a.contenidoTexto || a.contenido
          }))
        })
      });

      const data = await response.json();

      if (data.success) {
        // Agregar respuesta de PILI especializada
        addMessage(data.respuesta, 'asistente');

        // 🎯 MANEJAR DOCUMENTOS GENERADOS SEGÚN TIPO DE FLUJO
        if (tipoFlujo.includes('cotizacion') && data.cotizacion_generada && onCotizacionGenerada) {
          onCotizacionGenerada(data.cotizacion_generada);
          addMessage(
            '✅ **¡Cotización generada exitosamente!**\n\nPuedes ver el documento en el panel lateral. El sistema Multi-IA ha procesado todos los datos y creado una cotización profesional.',
            'asistente'
          );
        }

        if (tipoFlujo.includes('proyecto') && data.proyecto_generado && onProyectoGenerado) {
          onProyectoGenerado(data.proyecto_generado);
          addMessage(
            '✅ **¡Proyecto estructurado exitosamente!**\n\nLa planificación está lista con cronogramas y entregables definidos.',
            'asistente'
          );
        }

        if (tipoFlujo.includes('informe') && data.informe_generado && onInformeGenerado) {
          onInformeGenerado(data.informe_generado);
          addMessage(
            '✅ **¡Informe técnico completado!**\n\nDocumento profesional generado según estándares requeridos.',
            'asistente'
          );
        }

        // Actualizar proveedor actual si está en la respuesta
        if (data.proveedor_utilizado) {
          setProveedorActual(data.proveedor_utilizado);
        }

        // 🎯 NUEVO: Pasar HTML preview editable si existe
        if (data.html_preview && onHtmlPreviewGenerado) {
          onHtmlPreviewGenerado(data.html_preview);
        }

      } else {
        throw new Error(data.error || 'Error en la respuesta');
      }

    } catch (error) {
      console.error('Error en chat Multi-IA:', error);

      // Mensaje de error informativo pero tranquilizador
      addMessage(
        `⚠️ **Conexión limitada con servicios IA externos**

Pero no te preocupes: **PILIBrain (sistema local) está activo** y puede ayudarte con:

✅ **Análisis de documentos** básico
✅ **Estructura de ${tipoFlujo}** estándar  
✅ **Plantillas pre-configuradas** Tesla
✅ **Cálculos automáticos** según base de datos

El sistema **funcionará en modo local** mientras se restaura la conexión con los proveedores IA externos.

¿Quieres continuar con PILIBrain local?`,
        'asistente'
      );

      // Cambiar a modo local
      setProveedorActual('PILIBrain (Local)');
      setSistemaActivo(false);

    } finally {
      setAnalizando(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleEnviarMensajeChat();
    }
  };

  // Ejemplos contextuales según tipo de flujo
  const obtenerEjemplos = () => {
    const ejemplos = {
      'cotizacion-simple': [
        'Casa 120m² con 8 puntos de luz LED',
        'Local comercial 80m² con aire acondicionado',
        'Oficina 150m² con sistema básico'
      ],
      'cotizacion-compleja': [
        'Planta industrial 2000m² con motores trifásicos',
        'Centro comercial con subestación eléctrica',
        'Hospital con sistema UPS de emergencia'
      ],
      'proyecto-simple': [
        'Instalación residencial 3 dormitorios',
        'Remodelación eléctrica local comercial',
        'Mantenimiento preventivo edificio'
      ],
      'proyecto-complejo': [
        'Construcción planta industrial 6 meses',
        'Modernización sistema eléctrico hospital',
        'Automatización línea de producción'
      ],
      'informe-simple': [
        'Reporte post-instalación residencial',
        'Informe técnico mantenimiento',
        'Certificación de obra terminada'
      ],
      'informe-ejecutivo': [
        'Análisis de eficiencia energética',
        'Estudio de factibilidad proyecto',
        'Reporte ejecutivo trimestral'
      ]
    };

    return ejemplos[tipoFlujo] || ejemplos['cotizacion-simple'];
  };

  return (
    <div className="flex flex-col h-[600px] bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl shadow-2xl border-2 border-yellow-600">

      {/* Header especializado */}
      <div className={`bg-gradient-to-r from-${color.bg} to-${color.primary}-500 p-6 rounded-t-2xl border-b-2 border-${color.primary}-400`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`p-3 rounded-full shadow-lg ${sistemaActivo ? 'bg-white animate-pulse' : 'bg-gray-300'}`}>
              <Zap className="w-8 h-8 text-gray-900" />
            </div>
            <div>
              <h3 className="text-white font-bold text-xl">
                {servicioActual.especialidad}
              </h3>
              <p className="text-gray-900 text-sm font-medium">
                {servicioActual.nombre} • Tesla Electricidad S.A.C.
              </p>
            </div>
          </div>

          <div className="text-right">
            <div className={`text-sm font-bold ${sistemaActivo ? 'text-green-900' : 'text-yellow-900'}`}>
              {sistemaActivo ? '🟢 Multi-IA Activa' : '🟡 Modo Local'}
            </div>
            <div className="text-xs text-gray-800">
              IA: {proveedorActual}
            </div>
          </div>
        </div>
      </div>

      {/* Mensajes */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-100">
        {conversacion.map((msg, index) => (
          <div
            key={index}
            className={`flex gap-3 ${msg.tipo === 'usuario' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.tipo === 'asistente' && (
              <div className={`bg-${color.primary}-600 p-2 rounded-full h-fit shadow-md`}>
                <Bot size={20} className="text-white" />
              </div>
            )}

            <div className={`max-w-[75%] p-4 rounded-2xl shadow-lg ${msg.tipo === 'usuario'
              ? `bg-gradient-to-r from-${color.primary}-600 to-${color.primary}-500 text-white`
              : 'bg-white text-gray-800 border border-gray-200'
              }`}>
              <div className="whitespace-pre-wrap">
                {msg.mensaje.replace(/\*\*(.*?)\*\*/g, '').replace(/\n/g, '\n')}
              </div>

              {msg.timestamp && (
                <div className={`text-xs mt-2 pt-2 border-t ${msg.tipo === 'usuario' ? 'border-white/20 text-white/80' : 'border-gray-200 text-gray-500'
                  }`}>
                  {msg.timestamp}
                </div>
              )}
            </div>

            {msg.tipo === 'usuario' && (
              <div className="bg-gray-600 p-2 rounded-full h-fit">
                <User size={20} className="text-white" />
              </div>
            )}
          </div>
        ))}

        {/* Indicador de carga */}
        {analizando && (
          <div className="flex gap-3 justify-start">
            <div className={`bg-${color.primary}-600 p-2 rounded-full h-fit animate-pulse shadow-md`}>
              <Bot size={20} className="text-white" />
            </div>
            <div className="bg-white p-4 rounded-2xl border border-gray-200 shadow-lg">
              <div className="flex gap-2 items-center">
                <Loader className="animate-spin text-gray-600" size={20} />
                <span className="text-gray-600">{servicioActual.especialidad} analizando...</span>
              </div>
            </div>
          </div>
        )}

        {/* Sugerencias de ejemplo */}
        {conversacion.length <= 1 && (
          <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-lg">
            <h4 className="text-gray-800 font-bold mb-3 flex items-center gap-2">
              <FileText size={16} className={`text-${color.primary}-600`} />
              Ejemplos para {servicioActual.nombre}:
            </h4>
            <div className="space-y-2">
              {obtenerEjemplos().map((ejemplo, i) => (
                <button
                  key={i}
                  onClick={() => setInputChat(ejemplo)}
                  className={`block w-full text-left text-sm text-gray-600 hover:text-white hover:bg-${color.primary}-500 p-3 rounded-lg transition-colors duration-200`}
                >
                  💡 "{ejemplo}"
                </button>
              ))}
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input de mensaje */}
      <div className="p-4 bg-gray-900 rounded-b-2xl border-t-2 border-yellow-600">
        <div className="flex gap-3">
          <textarea
            value={inputChat}
            onChange={(e) => setInputChat(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={`Describe tu ${tipoFlujo.includes('cotizacion') ? 'proyecto para cotizar' : tipoFlujo.includes('proyecto') ? 'proyecto para planificar' : 'requerimiento para el informe'}...`}
            className="flex-1 bg-gray-800 text-white rounded-xl p-3 border-2 border-gray-700 focus:border-yellow-600 focus:outline-none resize-none placeholder-gray-500"
            rows="2"
            disabled={analizando}
          />
          <button
            onClick={handleEnviarMensajeChat}
            disabled={analizando || !inputChat.trim()}
            className={`px-6 rounded-xl font-bold transition-all flex items-center gap-2 ${analizando || !inputChat.trim()
              ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
              : `bg-gradient-to-r from-${color.primary}-600 to-${color.primary}-500 text-black hover:from-${color.primary}-500 hover:to-${color.primary}-400`
              }`}
          >
            {analizando ? (
              <Loader className="animate-spin" size={20} />
            ) : (
              <Send size={20} />
            )}
            {analizando ? 'Procesando...' : 'Enviar'}
          </button>
        </div>

        {/* Indicador de estado */}
        <div className="flex justify-between items-center mt-3 text-xs text-gray-500">
          <div>
            Presiona Enter para enviar, Shift+Enter para nueva línea
          </div>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${sistemaActivo ? 'bg-green-400' : 'bg-yellow-400'}`}></div>
            <span>{sistemaActivo ? 'Sistema Multi-IA Operativo' : 'Modo Local PILIBrain'}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatIA;