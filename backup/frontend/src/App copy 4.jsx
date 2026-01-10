import React, { useState, useRef, useEffect } from 'react';
import { Upload, MessageSquare, FileText, Download, Zap, Send, Loader, Edit, Save, AlertCircle, CheckCircle, X, RefreshCw, Home, FolderOpen, Eye, EyeOff, Folder, Users, TrendingUp, Clock, BarChart3, FileCheck, Briefcase, ChevronDown, ChevronUp, Layout, Layers, BookOpen, Calculator, Calendar, Target, Archive, Settings, PieChart } from 'lucide-react';

const CotizadorTesla30 = () => {
  // ============================================
  // ESTADOS PRINCIPALES - CONSERVADOS + EXTENDIDOS
  // ============================================
  
  const [pantallaActual, setPantallaActual] = useState('inicio');
  const [tipoFlujo, setTipoFlujo] = useState(null);
  
  // Estados de menús expandibles
  const [menuCotizaciones, setMenuCotizaciones] = useState(false);
  const [menuProyectos, setMenuProyectos] = useState(false);
  const [menuInformes, setMenuInformes] = useState(false);
  
  // Estados del flujo general
  const [paso, setPaso] = useState(1);
  const [archivos, setArchivos] = useState([]);
  const [conversacion, setConversacion] = useState([]);
  const [contextoUsuario, setContextoUsuario] = useState('');
  const [inputChat, setInputChat] = useState('');
  const [analizando, setAnalizando] = useState(false);
  const [cotizacion, setCotizacion] = useState(null);
  const [proyecto, setProyecto] = useState(null);
  const [informe, setInforme] = useState(null);
  const [error, setError] = useState('');
  const [exito, setExito] = useState('');
  const [servicioSeleccionado, setServicioSeleccionado] = useState('');
  const [industriaSeleccionada, setIndustriaSeleccionada] = useState('');
  const [descargando, setDescargando] = useState(null);
  const [logoBase64, setLogoBase64] = useState('');
  const [botonesContextuales, setBotonesContextuales] = useState([]);
  
  // Estados específicos para proyectos
  const [proyectoActual, setProyectoActual] = useState(null);
  const [vistaProyecto, setVistaProyecto] = useState('dashboard');
  const [tipoProyecto, setTipoProyecto] = useState('');
  const [presupuestoEstimado, setPresupuestoEstimado] = useState('');
  const [duracionMeses, setDuracionMeses] = useState('');
  const [nombreProyecto, setNombreProyecto] = useState('');
  const [clienteProyecto, setClienteProyecto] = useState('');
  
  // Estados específicos para informes
  const [tipoInforme, setTipoInforme] = useState('');
  const [proyectoSeleccionado, setProyectoSeleccionado] = useState('');
  const [formatoInforme, setFormatoInforme] = useState('word');
  const [incluirGraficos, setIncluirGraficos] = useState(true);
  const [informeGenerado, setInformeGenerado] = useState(null);
  
  // Referencias
  const chatContainerRef = useRef(null);
  const fileInputLogoRef = useRef(null);
  
  // ============================================
  // DATOS DE CONFIGURACIÓN
  // ============================================
  
  const [datosEmpresa] = useState({
    nombre: 'TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.',
    ruc: '20601138787',
    direccion: 'Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos',
    telefono: '906315961',
    email: 'ingenieria.teslaelectricidad@gmail.com',
    ciudad: 'San Juan de Lurigancho, Lima - Perú'
  });

  const servicios = [
    { id: 'electricidad', nombre: '⚡ Electricidad', icon: '⚡', descripcion: 'Instalaciones eléctricas completas' },
    { id: 'itse', nombre: '📋 Certificado ITSE', icon: '📋', descripcion: 'Inspección técnica de seguridad' },
    { id: 'puesta-tierra', nombre: '🔌 Puesta a Tierra', icon: '🔌', descripcion: 'Sistemas de protección eléctrica' },
    { id: 'contra-incendios', nombre: '🔥 Contra Incendios', icon: '🔥', descripcion: 'Sistemas de detección y extinción' },
    { id: 'domotica', nombre: '🏠 Domótica', icon: '🏠', descripcion: 'Automatización inteligente' },
    { id: 'cctv', nombre: '📹 CCTV', icon: '📹', descripcion: 'Videovigilancia profesional' },
    { id: 'redes', nombre: '🌐 Redes', icon: '🌐', descripcion: 'Cableado estructurado' },
    { id: 'automatizacion-industrial', nombre: '⚙️ Automatización Industrial', icon: '⚙️', descripcion: 'PLCs y control de procesos' }
  ];

  const industrias = [
    { id: 'construccion', nombre: '🏗️ Construcción' },
    { id: 'arquitectura', nombre: '🏢 Arquitectura' },
    { id: 'industrial', nombre: '⚙️ Industrial' },
    { id: 'mineria', nombre: '⛏️ Minería' },
    { id: 'educacion', nombre: '🎓 Educación' },
    { id: 'salud', nombre: '🏥 Salud' },
    { id: 'retail', nombre: '🏪 Retail' },
    { id: 'residencial', nombre: '🏘️ Residencial' }
  ];

  const basePreciosUniversal = {
    electricidad: {
      'Punto luz empotrado': 15, 'Tomacorriente doble': 18, 'Interruptor simple': 12,
      'Tablero general trifásico': 2800, 'Tablero depto monofásico': 800,
      'Cable THW 2.5mm²': 2.0, 'Cable THW 4mm²': 3.08, 'Luminaria LED 18W': 45
    },
    'itse': {
      'Derecho municipal ITSE Bajo': 168.30, 'Derecho municipal ITSE Medio': 208.60,
      'Servicio técnico ITSE Bajo': 400, 'Servicio técnico ITSE Medio': 550
    },
    'puesta-tierra': {
      'Pozo tierra completo': 1760, 'Varilla copperweld': 85, 'Cable desnudo Cu': 12
    },
    'domotica': {
      'Interruptor inteligente': 120, 'Sensor movimiento': 80, 'Central domótica': 1500
    },
    'cctv': {
      'Cámara IP 2MP': 350, 'DVR 8 canales': 800, 'Disco duro 1TB': 180
    }
  };

  // Datos mock para proyectos
  const proyectosMock = [
    { id: 'PROJ-2025-001', nombre: 'Instalación Eléctrica Torre Office', cliente: 'Constructora Lima', tipo: 'electricidad' },
    { id: 'PROJ-2025-002', nombre: 'Sistema CCTV Planta Industrial', cliente: 'Industrial Perú S.A.', tipo: 'cctv' },
    { id: 'PROJ-2025-003', nombre: 'Automatización Línea Producción', cliente: 'Manufactura XYZ', tipo: 'automatizacion-industrial' }
  ];

  // ============================================
  // FUNCIONES PRINCIPALES - CONSERVADAS + EXTENDIDAS
  // ============================================
  
  const volverAlInicio = () => {
    setPantallaActual('inicio');
    setTipoFlujo(null);
    setPaso(1);
    setProyectoActual(null);
    setConversacion([]);
    setCotizacion(null);
    setProyecto(null);
    setInforme(null);
    setServicioSeleccionado('');
    setIndustriaSeleccionada('');
    setContextoUsuario('');
    setBotonesContextuales([]);
    setArchivos([]);
    setNombreProyecto('');
    setClienteProyecto('');
    setPresupuestoEstimado('');
    setDuracionMeses('');
    setProyectoSeleccionado('');
    setExito('Sistema reiniciado');
    setTimeout(() => setExito(''), 2000);
  };

  const iniciarFlujo = (tipo) => {
    setTipoFlujo(tipo);
    setPantallaActual('flujo-pasos');
    setPaso(1);
    setConversacion([]);
    setCotizacion(null);
    setProyecto(null);
    setInforme(null);
  };

  // ============================================
  // FUNCIONES DEL CHAT - UNIVERSALES
  // ============================================
  
  const obtenerBotonesContextuales = async () => {
    try {
      const etapa = conversacion.length === 0 ? 'inicial' : 'refinamiento';
      const response = await fetch(`http://localhost:8000/api/chat/botones-contextuales/${tipoFlujo}?etapa=${etapa}&historial_length=${conversacion.length}`);
      const data = await response.json();
      setBotonesContextuales(data.botones || []);
    } catch (error) {
      console.error('Error obteniendo botones:', error);
      setBotonesContextuales([]);
    }
  };

  const handleEnviarMensajeChat = async () => {
    if (!inputChat.trim() || analizando) return;

    const nuevoMensaje = { tipo: 'usuario', mensaje: inputChat };
    const nuevaConversacion = [...conversacion, nuevoMensaje];
    setConversacion(nuevaConversacion);
    setInputChat('');
    setAnalizando(true);
    setError('');

    try {
      // Preparar contexto según el tipo de flujo
      let contextoPrincipal = `Servicio: ${servicioSeleccionado}, Industria: ${industriaSeleccionada}, Contexto: ${contextoUsuario}`;
      
      if (tipoFlujo.includes('proyecto')) {
        contextoPrincipal += `, Nombre: ${nombreProyecto}, Cliente: ${clienteProyecto}, Presupuesto: ${presupuestoEstimado}, Duración: ${duracionMeses} meses`;
      } else if (tipoFlujo.includes('informe')) {
        contextoPrincipal += `, Proyecto: ${proyectoSeleccionado}, Tipo: ${tipoInforme}`;
      }

      const response = await fetch('http://localhost:8000/api/chat/chat-contextualizado', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tipo_flujo: tipoFlujo,
          mensaje: inputChat,
          historial: nuevaConversacion,
          contexto_adicional: contextoPrincipal,
          archivos_procesados: archivos.map(a => ({ nombre: a.nombre, contenido: a.contenidoTexto }))
        })
      });

      const data = await response.json();
      
      if (data.success) {
        const mensajeIA = { tipo: 'asistente', mensaje: data.respuesta };
        setConversacion(prev => [...prev, mensajeIA]);

        // Manejar respuestas según el tipo de flujo
        if (tipoFlujo.includes('cotizacion') && data.cotizacion_generada) {
          setCotizacion(data.cotizacion_generada);
        } else if (tipoFlujo.includes('proyecto') && data.proyecto_generado) {
          setProyecto(data.proyecto_generado);
        } else if (tipoFlujo.includes('informe') && data.informe_generado) {
          setInforme(data.informe_generado);
        }

        // Actualizar botones contextuales
        if (data.botones_contextuales) {
          setBotonesContextuales(data.botones_contextuales);
        }
      } else {
        throw new Error(data.error || 'Error en la respuesta');
      }
    } catch (error) {
      console.error('Error en chat:', error);
      const mensajeError = { tipo: 'asistente', mensaje: 'Lo siento, hubo un error. Inténtalo de nuevo.' };
      setConversacion(prev => [...prev, mensajeError]);
      setError('Error de conexión con la IA');
    } finally {
      setAnalizando(false);
    }
  };

  const enviarRespuestaRapida = (texto) => {
    setInputChat(texto);
    setTimeout(() => {
      handleEnviarMensajeChat();
    }, 100);
  };

  // ============================================
  // FUNCIONES DE ARCHIVOS
  // ============================================
  
  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    files.forEach(file => {
      if (file.size > 10 * 1024 * 1024) {
        setError(`El archivo ${file.name} es demasiado grande (máx 10MB)`);
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (e) => {
        const archivo = {
          nombre: file.name,
          extension: file.name.split('.').pop(),
          tamano: `${(file.size / 1024).toFixed(1)} KB`,
          contenido: e.target.result,
          contenidoTexto: file.type.includes('text') ? e.target.result : null
        };
        
        setArchivos(prev => [...prev, archivo]);
        setExito(`Archivo ${file.name} procesado correctamente`);
        setTimeout(() => setExito(''), 3000);
      };
      
      if (file.type.includes('text')) {
        reader.readAsText(file);
      } else {
        reader.readAsDataURL(file);
      }
    });
  };

  const cargarLogo = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 2 * 1024 * 1024) {
        setError('El logo debe ser menor a 2MB');
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setLogoBase64(e.target.result);
        setExito('Logo cargado correctamente');
        setTimeout(() => setExito(''), 3000);
      };
      reader.readAsDataURL(file);
    }
  };

  // ============================================
  // FUNCIONES DE DESCARGA UNIVERSALES
  // ============================================
  
  const handleDescargar = async (tipo, formato) => {
    let entidad = null;
    let endpoint = '';
    let fileName = '';

    // Determinar qué entidad descargar
    if (tipo === 'cotizacion' && cotizacion) {
      entidad = cotizacion;
      endpoint = 'cotizaciones';
      fileName = `cotizacion_${cotizacion.id || 'nueva'}`;
    } else if (tipo === 'proyecto' && proyecto) {
      entidad = proyecto;
      endpoint = 'proyectos';
      fileName = `proyecto_${proyecto.id || 'nuevo'}`;
    } else if (tipo === 'informe' && informe) {
      entidad = informe;
      endpoint = 'informes';
      fileName = `informe_${informe.id || 'nuevo'}`;
    } else {
      setError(`No hay ${tipo} para descargar`);
      return;
    }

    setDescargando(`${tipo}-${formato}`);
    setError('');
    setExito('');

    try {
      let entidadId = entidad.id;

      // Si no tiene ID, guardar primero
      if (!entidadId) {
        console.log(`📝 Guardando ${tipo} en el backend...`);
        
        let datosParaBackend = {};
        
        if (tipo === 'cotizacion') {
          datosParaBackend = {
            cliente: entidad.cliente || 'Cliente',
            proyecto: entidad.proyecto || 'Proyecto',
            descripcion: entidad.descripcionGeneral || '',
            items: entidad.items || [],
            subtotal: parseFloat(calcularTotales().subtotal),
            igv: parseFloat(calcularTotales().igv),
            total: parseFloat(calcularTotales().total),
            observaciones: entidad.observaciones || '',
            vigencia: entidad.validez || '30 días',
            estado: 'borrador'
          };
        } else if (tipo === 'proyecto') {
          datosParaBackend = {
            nombre: nombreProyecto || 'Proyecto',
            cliente: clienteProyecto || 'Cliente',
            tipo: servicioSeleccionado || 'general',
            presupuesto_estimado: parseFloat(presupuestoEstimado) || 0,
            duracion_meses: parseInt(duracionMeses) || 1,
            descripcion: contextoUsuario || '',
            estado: 'planificacion'
          };
        } else if (tipo === 'informe') {
          datosParaBackend = {
            proyecto_id: proyectoSeleccionado || 'general',
            tipo: tipoInforme || 'simple',
            formato: formatoInforme || 'word',
            incluir_graficos: incluirGraficos,
            contenido: entidad.contenido || '',
            estado: 'borrador'
          };
        }

        const response = await fetch(`http://localhost:8000/api/${endpoint}/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(datosParaBackend)
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error al guardar: ${errorText}`);
        }

        const entidadGuardada = await response.json();
        entidadId = entidadGuardada.id;
        
        // Actualizar estado
        if (tipo === 'cotizacion') {
          setCotizacion({ ...entidad, id: entidadId });
        } else if (tipo === 'proyecto') {
          setProyecto({ ...entidad, id: entidadId });
        } else if (tipo === 'informe') {
          setInforme({ ...entidad, id: entidadId });
        }
      }

      // Generar documento
      console.log(`📄 Generando ${formato.toUpperCase()} para ${tipo}`);
      setExito(`Generando ${formato.toUpperCase()}...`);
      
      const docResponse = await fetch(`http://localhost:8000/api/${endpoint}/${entidadId}/generar-${formato}`, {
        method: 'POST'
      });

      if (!docResponse.ok) {
        throw new Error(`Error al generar ${formato}`);
      }

      const blob = await docResponse.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${fileName}.${formato === 'word' ? 'docx' : 'pdf'}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      setExito(`✅ ${formato.toUpperCase()} descargado exitosamente`);
      setTimeout(() => setExito(''), 4000);
    } catch (error) {
      console.error('Error al descargar:', error);
      setError(`Error al generar el documento: ${error.message}`);
    } finally {
      setDescargando(null);
    }
  };

  const calcularTotales = () => {
    if (!cotizacion?.items) return { subtotal: 0, igv: 0, total: 0 };
    const subtotal = cotizacion.items.reduce((sum, item) => sum + (item.cantidad * item.precioUnitario), 0);
    return {
      subtotal: subtotal.toFixed(2),
      igv: (subtotal * 0.18).toFixed(2),
      total: (subtotal * 1.18).toFixed(2)
    };
  };

  // ============================================
  // COMPONENTE ALERTA
  // ============================================
  
  const Alerta = ({ tipo, mensaje, onClose }) => {
    if (!mensaje) return null;
    const estilos = tipo === 'error' ? 'bg-red-900 border-red-600' : 'bg-green-900 border-green-600';
    const Icono = tipo === 'error' ? AlertCircle : CheckCircle;
    
    return (
      <div className={`${estilos} border-2 text-white px-4 py-3 rounded-lg mb-4 flex items-center justify-between backdrop-blur-sm bg-opacity-90`}>
        <div className="flex items-center gap-2">
          <Icono className="w-5 h-5" />
          <span>{mensaje}</span>
        </div>
        {onClose && <button onClick={onClose} className="text-white hover:text-gray-300">✕</button>}
      </div>
    );
  };

  // ============================================
  // HOOKS
  // ============================================
  
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [conversacion]);

  useEffect(() => {
    if (tipoFlujo && paso === 2) {
      obtenerBotonesContextuales();
    }
  }, [conversacion, tipoFlujo, paso]);

  const totales = calcularTotales();

  // ============================================
  // RENDERIZADO - PANTALLA INICIO
  // ============================================
  
  if (pantallaActual === 'inicio') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6">
        <div className="max-w-5xl mx-auto">
          {/* HEADER PRINCIPAL */}
          <div className="bg-gradient-to-r from-red-950 via-red-900 to-black rounded-2xl p-8 mb-8 border-2 border-yellow-600 shadow-2xl backdrop-blur-md bg-opacity-90 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-yellow-600/10 via-transparent to-yellow-600/10 animate-pulse"></div>
            <div className="relative z-10">
              <h1 className="text-5xl font-bold flex items-center gap-4 text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-yellow-300 to-yellow-500">
                <Zap className="w-12 h-12 text-yellow-400 animate-pulse" />
                {datosEmpresa.nombre}
              </h1>
              <p className="text-yellow-400 mt-3 font-semibold text-xl">Sistema Profesional Elite - Clase Mundial v3.0</p>
              <div className="flex items-center gap-4 mt-4 text-sm">
                <span className="text-gray-300">📱 WhatsApp: {datosEmpresa.telefono}</span>
                <span className="text-gray-300">📧 {datosEmpresa.email}</span>
              </div>
            </div>
          </div>

          {error && <Alerta tipo="error" mensaje={error} onClose={() => setError('')} />}
          {exito && <Alerta tipo="exito" mensaje={exito} onClose={() => setExito('')} />}

          {/* TÍTULO PRINCIPAL */}
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-yellow-400 mb-4">¿Qué necesitas hacer?</h2>
            <p className="text-gray-300 text-lg">Selecciona el tipo de trabajo que deseas realizar</p>
          </div>

          {/* MENÚS EXPANDIBLES */}
          <div className="space-y-4">
            
            {/* MENÚ 1: COTIZACIONES */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl border-2 border-yellow-700 shadow-xl backdrop-blur-md bg-opacity-90 overflow-hidden">
              <button
                onClick={() => setMenuCotizaciones(!menuCotizaciones)}
                className="w-full p-6 flex items-center justify-between hover:bg-gray-800 transition-all duration-300">
                <div className="flex items-center gap-4">
                  <div className="bg-gradient-to-br from-yellow-600 to-yellow-500 p-3 rounded-xl">
                    <FileText className="w-8 h-8 text-black" />
                  </div>
                  <div className="text-left">
                    <h3 className="text-2xl font-bold text-yellow-400">📊 COTIZACIONES</h3>
                    <p className="text-gray-400 text-sm">Genera presupuestos y cotizaciones</p>
                  </div>
                </div>
                {menuCotizaciones ? <ChevronUp className="w-6 h-6 text-yellow-400" /> : <ChevronDown className="w-6 h-6 text-yellow-400" />}
              </button>
              
              {menuCotizaciones && (
                <div className="px-6 pb-6 space-y-3 animate-fadeIn">
                  <button
                    onClick={() => iniciarFlujo('cotizacion-rapida')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-yellow-900 hover:to-yellow-800 p-4 rounded-xl border-2 border-gray-700 hover:border-yellow-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <Zap className="w-6 h-6 text-yellow-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Cotización Rápida</p>
                        <p className="text-gray-400 text-sm">Proceso simplificado - 5 a 15 minutos</p>
                      </div>
                    </div>
                  </button>

                  <button
                    onClick={() => iniciarFlujo('cotizacion-compleja')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-purple-900 hover:to-purple-800 p-4 rounded-xl border-2 border-gray-700 hover:border-purple-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <Layers className="w-6 h-6 text-purple-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Cotización Compleja</p>
                        <p className="text-gray-400 text-sm">Proyectos grandes con análisis detallado</p>
                      </div>
                    </div>
                  </button>
                </div>
              )}
            </div>

            {/* MENÚ 2: PROYECTOS */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl border-2 border-blue-700 shadow-xl backdrop-blur-md bg-opacity-90 overflow-hidden">
              <button
                onClick={() => setMenuProyectos(!menuProyectos)}
                className="w-full p-6 flex items-center justify-between hover:bg-gray-800 transition-all duration-300">
                <div className="flex items-center gap-4">
                  <div className="bg-gradient-to-br from-blue-600 to-blue-500 p-3 rounded-xl">
                    <Briefcase className="w-8 h-8 text-white" />
                  </div>
                  <div className="text-left">
                    <h3 className="text-2xl font-bold text-blue-400">📁 PROYECTOS</h3>
                    <p className="text-gray-400 text-sm">Gestión integral de proyectos</p>
                  </div>
                </div>
                {menuProyectos ? <ChevronUp className="w-6 h-6 text-blue-400" /> : <ChevronDown className="w-6 h-6 text-blue-400" />}
              </button>
              
              {menuProyectos && (
                <div className="px-6 pb-6 space-y-3 animate-fadeIn">
                  <button
                    onClick={() => iniciarFlujo('proyecto-simple')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-blue-900 hover:to-blue-800 p-4 rounded-xl border-2 border-gray-700 hover:border-blue-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <Folder className="w-6 h-6 text-blue-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Proyecto Simple</p>
                        <p className="text-gray-400 text-sm">Gestión básica y seguimiento</p>
                      </div>
                    </div>
                  </button>

                  <button
                    onClick={() => iniciarFlujo('proyecto-complejo')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-purple-900 hover:to-purple-800 p-4 rounded-xl border-2 border-gray-700 hover:border-purple-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <Layout className="w-6 h-6 text-purple-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Proyecto Complejo</p>
                        <p className="text-gray-400 text-sm">Con Gantt, hitos y seguimiento avanzado</p>
                      </div>
                    </div>
                  </button>
                </div>
              )}
            </div>

            {/* MENÚ 3: INFORMES */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl border-2 border-green-700 shadow-xl backdrop-blur-md bg-opacity-90 overflow-hidden">
              <button
                onClick={() => setMenuInformes(!menuInformes)}
                className="w-full p-6 flex items-center justify-between hover:bg-gray-800 transition-all duration-300">
                <div className="flex items-center gap-4">
                  <div className="bg-gradient-to-br from-green-600 to-green-500 p-3 rounded-xl">
                    <BookOpen className="w-8 h-8 text-white" />
                  </div>
                  <div className="text-left">
                    <h3 className="text-2xl font-bold text-green-400">📄 INFORMES</h3>
                    <p className="text-gray-400 text-sm">Documentos y reportes profesionales</p>
                  </div>
                </div>
                {menuInformes ? <ChevronUp className="w-6 h-6 text-green-400" /> : <ChevronDown className="w-6 h-6 text-green-400" />}
              </button>
              
              {menuInformes && (
                <div className="px-6 pb-6 space-y-3 animate-fadeIn">
                  <button
                    onClick={() => iniciarFlujo('informe-simple')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-green-900 hover:to-green-800 p-4 rounded-xl border-2 border-gray-700 hover:border-green-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <FileText className="w-6 h-6 text-green-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Informe Simple</p>
                        <p className="text-gray-400 text-sm">PDF básico con datos estándar</p>
                      </div>
                    </div>
                  </button>

                  <button
                    onClick={() => iniciarFlujo('informe-ejecutivo')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-purple-900 hover:to-purple-800 p-4 rounded-xl border-2 border-gray-700 hover:border-purple-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <BarChart3 className="w-6 h-6 text-purple-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Informe Ejecutivo</p>
                        <p className="text-gray-400 text-sm">Word con formato APA, tablas y gráficos</p>
                      </div>
                    </div>
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ============================================
  // PANTALLA: FLUJO DE PASOS (UNIVERSAL)
  // ============================================
  
  if (pantallaActual === 'flujo-pasos') {
    // Determinar el tipo y características del flujo
    const esCotizacion = tipoFlujo.includes('cotizacion');
    const esProyecto = tipoFlujo.includes('proyecto');
    const esInforme = tipoFlujo.includes('informe');
    const esComplejo = tipoFlujo.includes('complejo') || tipoFlujo.includes('compleja') || tipoFlujo.includes('ejecutivo');

    // Configuración del color según el tipo
    let colores = { primary: 'yellow', border: 'yellow-700', bg: 'yellow-600' };
    if (esProyecto) colores = { primary: 'blue', border: 'blue-700', bg: 'blue-600' };
    else if (esInforme) colores = { primary: 'green', border: 'green-700', bg: 'green-600' };

    // Títulos y descripciones
    const configuracion = {
      'cotizacion-rapida': { titulo: '⚡ Cotización Rápida', desc: 'Proceso simplificado - 5 a 15 minutos', icon: Zap },
      'cotizacion-compleja': { titulo: '📄 Cotización Compleja', desc: 'Proyectos grandes con análisis detallado', icon: Layers },
      'proyecto-simple': { titulo: '📁 Proyecto Simple', desc: 'Gestión básica y seguimiento', icon: Folder },
      'proyecto-complejo': { titulo: '🏗️ Proyecto Complejo', desc: 'Con Gantt, hitos y seguimiento avanzado', icon: Layout },
      'informe-simple': { titulo: '📄 Informe Simple', desc: 'PDF básico con datos estándar', icon: FileText },
      'informe-ejecutivo': { titulo: '📊 Informe Ejecutivo', desc: 'Word con formato APA, tablas y gráficos', icon: BarChart3 }
    };

    const config = configuracion[tipoFlujo];
    const IconoTitulo = config.icon;

    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6">
        <div className="max-w-5xl mx-auto">
          {/* BOTÓN VOLVER */}
          <button onClick={volverAlInicio}
            className="fixed top-6 right-6 z-50 bg-gradient-to-r from-red-900 to-red-800 hover:from-red-800 hover:to-red-700 text-yellow-400 px-4 py-2 rounded-lg font-semibold flex items-center gap-2 shadow-2xl border-2 border-yellow-600 backdrop-blur-md transition-all duration-300 hover:scale-105">
            <Home className="w-5 h-5" />
            Inicio
          </button>

          {/* HEADER */}
          <div className="bg-gradient-to-r from-red-950 via-red-900 to-black rounded-2xl p-8 mb-6 border-2 border-yellow-600 shadow-2xl backdrop-blur-md bg-opacity-90 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-yellow-600/10 via-transparent to-yellow-600/10 animate-pulse"></div>
            <div className="relative z-10">
              <h1 className="text-4xl font-bold flex items-center gap-3 text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-yellow-300 to-yellow-500">
                <IconoTitulo className="w-10 h-10 text-yellow-400 animate-pulse" />
                {config.titulo}
              </h1>
              <p className="text-yellow-400 mt-2 font-semibold">{config.desc}</p>
            </div>
          </div>

          {/* ALERTAS */}
          {error && <Alerta tipo="error" mensaje={error} onClose={() => setError('')} />}
          {exito && <Alerta tipo="exito" mensaje={exito} onClose={() => setExito('')} />}

          {/* INDICADOR DE PASOS */}
          <div className={`bg-gradient-to-r from-gray-900 to-black rounded-2xl p-6 mb-6 border-2 border-${colores.border} shadow-xl`}>
            <div className="flex items-center justify-between">
              {[1, 2, 3].map(num => (
                <div key={num} className={`flex items-center ${num < 3 ? 'flex-1' : ''}`}>
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center border-2 font-bold ${
                    paso >= num ? `bg-${colores.bg} border-${colores.bg} text-black` : 'border-gray-700 text-gray-700'
                  }`}>
                    {num}
                  </div>
                  <div className="ml-3">
                    <p className={`font-semibold ${paso >= num ? `text-${colores.primary}-400` : 'text-gray-500'}`}>
                      {num === 1 ? 'Configuración' : num === 2 ? 'Chat con IA' : 'Finalización'}
                    </p>
                  </div>
                  {num < 3 && <div className={`flex-1 h-1 mx-4 ${paso > num ? `bg-${colores.bg}` : 'bg-gray-700'}`} />}
                </div>
              ))}
            </div>
          </div>

          {/* PASO 1: CONFIGURACIÓN */}
          {paso === 1 && (
            <div className="space-y-6">
              
              {/* LOGO OPCIONAL (Solo para cotizaciones e informes) */}
              {(esCotizacion || esInforme) && (
                <div className="bg-gradient-to-br from-purple-900 to-purple-800 rounded-2xl p-6 border-2 border-purple-500 shadow-xl backdrop-blur-md bg-opacity-90">
                  <h2 className="text-2xl font-bold mb-4 text-purple-200 flex items-center gap-2">
                    🎨 Logo Empresa (Opcional)
                  </h2>
                  
                  <div className="flex gap-4 items-center">
                    <div className="flex-1">
                      <input 
                        ref={fileInputLogoRef}
                        type="file" 
                        onChange={cargarLogo} 
                        className="hidden" 
                        accept="image/*"
                      />
                      <button
                        onClick={() => fileInputLogoRef.current?.click()}
                        className="w-full bg-gradient-to-r from-purple-700 to-purple-600 hover:from-purple-600 hover:to-purple-500 text-white px-6 py-3 rounded-xl font-semibold flex items-center justify-center gap-2 shadow-xl border-2 border-purple-400 transition-all duration-300 hover:scale-105">
                        <Upload className="w-5 h-5" />
                        {logoBase64 ? 'Cambiar Logo' : 'Subir Logo'}
                      </button>
                      <p className="text-xs text-purple-200 mt-2 text-center">
                        PNG, JPG, WebP - Máx 2MB • Aparecerá en documentos
                      </p>
                    </div>
                    
                    {logoBase64 && (
                      <div className="bg-white rounded-xl p-3 border-2 border-purple-400 shadow-lg">
                        <img src={logoBase64} alt="Logo" className="w-24 h-24 object-contain" />
                        <p className="text-xs text-gray-600 mt-2 text-center font-semibold">✅ Cargado</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* CONFIGURACIÓN ESPECÍFICA POR TIPO */}
              
              {/* CONFIGURACIÓN DE PROYECTOS */}
              {esProyecto && (
                <>
                  <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-blue-700 shadow-xl backdrop-blur-md bg-opacity-90">
                    <h2 className="text-2xl font-bold mb-4 text-blue-400">📋 Información del Proyecto</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-blue-400 font-semibold mb-2">Nombre del Proyecto *</label>
                        <input 
                          type="text"
                          value={nombreProyecto}
                          onChange={(e) => setNombreProyecto(e.target.value)}
                          className="w-full px-4 py-3 bg-gray-950 border border-blue-700 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
                          placeholder="Ej: Instalación Eléctrica Edificio Central"
                        />
                      </div>
                      <div>
                        <label className="block text-blue-400 font-semibold mb-2">Cliente *</label>
                        <input 
                          type="text"
                          value={clienteProyecto}
                          onChange={(e) => setClienteProyecto(e.target.value)}
                          className="w-full px-4 py-3 bg-gray-950 border border-blue-700 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
                          placeholder="Ej: Constructora ABC S.A.C."
                        />
                      </div>
                      <div>
                        <label className="block text-blue-400 font-semibold mb-2">Presupuesto Estimado (S/)</label>
                        <input 
                          type="number"
                          value={presupuestoEstimado}
                          onChange={(e) => setPresupuestoEstimado(e.target.value)}
                          className="w-full px-4 py-3 bg-gray-950 border border-blue-700 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
                          placeholder="50000"
                        />
                      </div>
                      <div>
                        <label className="block text-blue-400 font-semibold mb-2">Duración (Meses)</label>
                        <input 
                          type="number"
                          value={duracionMeses}
                          onChange={(e) => setDuracionMeses(e.target.value)}
                          className="w-full px-4 py-3 bg-gray-950 border border-blue-700 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
                          placeholder="6"
                        />
                      </div>
                    </div>

                    {esComplejo && (
                      <div className="mt-6 bg-purple-950 bg-opacity-50 border border-purple-700 rounded-xl p-6">
                        <h3 className="text-purple-400 font-bold mb-3">🗂️ Sistema de Gestión Avanzada</h3>
                        <p className="text-gray-300 text-sm mb-4">
                          Se creará una estructura completa de gestión:
                        </p>
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
                          <div className="bg-gray-900 p-3 rounded-lg">📊 Dashboard Ejecutivo</div>
                          <div className="bg-gray-900 p-3 rounded-lg">📅 Cronograma Gantt</div>
                          <div className="bg-gray-900 p-3 rounded-lg">🎯 Hitos y Entregas</div>
                          <div className="bg-gray-900 p-3 rounded-lg">💰 Control Presupuestal</div>
                          <div className="bg-gray-900 p-3 rounded-lg">📈 Análisis de Riesgos</div>
                          <div className="bg-gray-900 p-3 rounded-lg">👥 Asignación de Recursos</div>
                        </div>
                      </div>
                    )}
                  </div>
                </>
              )}

              {/* CONFIGURACIÓN DE INFORMES */}
              {esInforme && (
                <>
                  <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-green-700 shadow-xl backdrop-blur-md bg-opacity-90">
                    <h2 className="text-2xl font-bold mb-4 text-green-400">📄 Configuración del Informe</h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-green-400 font-semibold mb-2">Proyecto Base *</label>
                        <select 
                          value={proyectoSeleccionado}
                          onChange={(e) => setProyectoSeleccionado(e.target.value)}
                          className="w-full px-4 py-3 bg-gray-950 border border-green-700 rounded-xl focus:ring-2 focus:ring-green-500 focus:outline-none text-white">
                          <option value="">Seleccionar proyecto...</option>
                          {proyectosMock.map(p => (
                            <option key={p.id} value={p.id}>{p.nombre} - {p.cliente}</option>
                          ))}
                          <option value="general">📋 Informe General (Sin proyecto específico)</option>
                        </select>
                      </div>
                      
                      <div>
                        <label className="block text-green-400 font-semibold mb-2">Formato de Salida</label>
                        <select 
                          value={formatoInforme}
                          onChange={(e) => setFormatoInforme(e.target.value)}
                          className="w-full px-4 py-3 bg-gray-950 border border-green-700 rounded-xl focus:ring-2 focus:ring-green-500 focus:outline-none text-white">
                          <option value="word">📄 Word (Editable)</option>
                          <option value="pdf">📃 PDF (Final)</option>
                        </select>
                      </div>
                    </div>

                    {esComplejo && (
                      <div className="mt-6 bg-purple-950 bg-opacity-50 border border-purple-700 rounded-xl p-6">
                        <h3 className="text-purple-400 font-bold mb-3">✨ Características del Informe Ejecutivo</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                          <div className="flex items-start gap-2">
                            <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                            <div>
                              <p className="font-semibold text-white">Formato APA Profesional</p>
                              <p className="text-gray-400">Portada, índice automático, referencias</p>
                            </div>
                          </div>
                          <div className="flex items-start gap-2">
                            <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                            <div>
                              <p className="font-semibold text-white">Gráficos y Tablas</p>
                              <p className="text-gray-400">Visualizaciones automáticas de datos</p>
                            </div>
                          </div>
                          <div className="flex items-start gap-2">
                            <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                            <div>
                              <p className="font-semibold text-white">Análisis Ejecutivo</p>
                              <p className="text-gray-400">KPIs, métricas y recomendaciones</p>
                            </div>
                          </div>
                          <div className="flex items-start gap-2">
                            <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                            <div>
                              <p className="font-semibold text-white">Resumen Gerencial</p>
                              <p className="text-gray-400">Dashboard de decisión estratégica</p>
                            </div>
                          </div>
                        </div>
                        
                        <div className="mt-4">
                          <label className="flex items-center gap-2 text-purple-200">
                            <input 
                              type="checkbox" 
                              checked={incluirGraficos}
                              onChange={(e) => setIncluirGraficos(e.target.checked)}
                              className="rounded border-purple-600 text-purple-600 focus:ring-purple-500" 
                            />
                            <span className="font-semibold">Incluir gráficos automáticos</span>
                          </label>
                        </div>
                      </div>
                    )}
                  </div>
                </>
              )}

              {/* CONFIGURACIÓN UNIVERSAL: SERVICIO E INDUSTRIA */}
              <div className={`bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-${colores.border} shadow-xl backdrop-blur-md bg-opacity-90`}>
                <h2 className={`text-2xl font-bold mb-4 text-${colores.primary}-400`}>⚙️ Tipo de Servicio</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {servicios.map(servicio => (
                    <button
                      key={servicio.id}
                      onClick={() => setServicioSeleccionado(servicio.id)}
                      className={`p-4 rounded-xl border-2 transition-all duration-300 text-left ${
                        servicioSeleccionado === servicio.id
                          ? `border-${colores.bg} bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl scale-105`
                          : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800'
                      }`}>
                      <div className="text-2xl mb-2">{servicio.icon}</div>
                      <div className="text-sm font-semibold">{servicio.nombre.split(' ').slice(1).join(' ')}</div>
                    </button>
                  ))}
                </div>
              </div>

              <div className={`bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-${colores.border} shadow-xl backdrop-blur-md bg-opacity-90`}>
                <h2 className={`text-2xl font-bold mb-4 text-${colores.primary}-400`}>🏢 Industria</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {industrias.map(industria => (
                    <button
                      key={industria.id}
                      onClick={() => setIndustriaSeleccionada(industria.id)}
                      className={`p-3 rounded-xl border-2 transition-all duration-300 ${
                        industriaSeleccionada === industria.id
                          ? `border-${colores.bg} bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl`
                          : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800'
                      }`}>
                      <div className="text-sm font-semibold">{industria.nombre}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* INFORMACIÓN Y CONTEXTO */}
              <div className={`bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-${colores.border} shadow-xl backdrop-blur-md bg-opacity-90`}>
                <h2 className={`text-2xl font-bold mb-4 text-${colores.primary}-400`}>📝 Descripción Detallada</h2>
                
                {/* PRECIOS BASE (Solo para cotizaciones) */}
                {esCotizacion && servicioSeleccionado && basePreciosUniversal[servicioSeleccionado] && (
                  <div className="mb-4 p-4 bg-blue-950 bg-opacity-50 border border-blue-700 rounded-xl backdrop-blur-sm">
                    <p className="text-sm font-semibold text-blue-300 mb-2">
                      💡 Precios base {servicios.find(s => s.id === servicioSeleccionado)?.nombre}
                    </p>
                    <div className="grid grid-cols-2 gap-2 text-xs text-gray-300">
                      {Object.entries(basePreciosUniversal[servicioSeleccionado]).slice(0, 4).map(([item, precio]) => (
                        <div key={item}>• {item}: S/ {precio}</div>
                      ))}
                    </div>
                  </div>
                )}
                
                <textarea 
                  value={contextoUsuario} 
                  onChange={(e) => setContextoUsuario(e.target.value)}
                  className="w-full h-32 px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none resize-none mb-4 text-white placeholder-gray-500"
                  placeholder={
                    esCotizacion ? "Describe el proyecto a cotizar detalladamente..." :
                    esProyecto ? "Describe los objetivos y alcance del proyecto..." :
                    "Describe el propósito y contenido del informe..."
                  }
                />

                {/* UPLOAD DE DOCUMENTOS */}
                <div className="border-t-2 border-gray-800 pt-4">
                  <h3 className="text-lg font-semibold mb-3 text-gray-300">Documentos {esComplejo ? '(Recomendado)' : '(Opcional)'}</h3>
                  <div className="border-2 border-dashed border-gray-700 rounded-xl p-6 text-center hover:border-yellow-600 transition-all cursor-pointer mb-4 bg-gray-950 bg-opacity-50">
                    <input type="file" multiple onChange={handleFileUpload} className="hidden" id="fileInput" accept=".pdf,.png,.jpg,.jpeg,.gif,.webp,.xlsx,.xls,.docx,.doc,.html,.json,.txt,.csv" />
                    <label htmlFor="fileInput" className="cursor-pointer">
                      <Upload className="w-12 h-12 mx-auto mb-3 text-yellow-500" />
                      <p className="text-sm text-gray-400 font-semibold">Sube documentos (máx 10MB)</p>
                      <p className="text-xs text-gray-500 mt-2">Formatos: PDF, Excel, Word, imágenes, JSON, TXT, CSV</p>
                    </label>
                  </div>

                  {archivos.length > 0 && (
                    <div className="space-y-2">
                      <p className="text-sm font-semibold text-yellow-400 mb-2">📁 Archivos procesados:</p>
                      {archivos.map((archivo, index) => (
                        <div key={index} className="flex items-center justify-between bg-gray-950 bg-opacity-70 p-3 rounded-xl border border-gray-800 hover:border-yellow-600 transition-all">
                          <div className="flex items-center gap-2 flex-1">
                            <FileText className="w-5 h-5 text-yellow-500" />
                            <div className="flex-1">
                              <div className="flex items-center gap-2">
                                <span className="text-sm font-semibold">{archivo.nombre}</span>
                                <span className="text-xs bg-blue-900 text-blue-300 px-2 py-0.5 rounded">{archivo.extension}</span>
                              </div>
                              <div className="flex items-center gap-3 mt-1">
                                <span className="text-xs text-gray-400">{archivo.tamano}</span>
                                <span className="text-xs text-green-400 font-semibold flex items-center gap-1">
                                  <CheckCircle className="w-3 h-3" />
                                  Procesado
                                </span>
                              </div>
                            </div>
                          </div>
                          <button 
                            onClick={() => setArchivos(prev => prev.filter((_, i) => i !== index))} 
                            className="text-red-400 hover:text-red-300 ml-2">
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* BOTÓN CONTINUAR */}
              <button 
                onClick={() => setPaso(2)} 
                disabled={!servicioSeleccionado || !industriaSeleccionada || !contextoUsuario.trim() || 
                         (esProyecto && (!nombreProyecto || !clienteProyecto)) ||
                         (esInforme && !proyectoSeleccionado)}
                className={`w-full bg-gradient-to-r from-${colores.bg} via-${colores.primary}-500 to-${colores.bg} hover:from-${colores.primary}-500 hover:to-${colores.primary}-400 disabled:from-gray-800 disabled:to-gray-700 disabled:cursor-not-allowed py-4 rounded-xl font-bold text-lg text-black shadow-2xl border-2 border-${colores.primary}-400 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-3`}>
                <MessageSquare className="w-6 h-6" />
                Comenzar Chat con IA Tesla
              </button>
            </div>
          )}

          {/* PASO 2: CHAT CON IA */}
          {paso === 2 && (
            <div className="bg-white rounded-2xl shadow-xl h-[70vh] flex flex-col">
              <div className={`bg-gradient-to-r from-${colores.bg} to-${colores.primary}-500 p-6 rounded-t-2xl`}>
                <h3 className="text-2xl font-bold text-black flex items-center gap-2">
                  <MessageSquare className="w-7 h-7" />
                  Chat con IA Especializada Tesla
                </h3>
                <p className="text-gray-800 mt-1">
                  {esCotizacion && `Cotizando: ${servicios.find(s => s.id === servicioSeleccionado)?.nombre}`}
                  {esProyecto && `Planificando: ${nombreProyecto || 'Proyecto'}`}
                  {esInforme && `Generando: Informe ${esComplejo ? 'Ejecutivo' : 'Simple'}`}
                </p>
              </div>
              
              {/* ÁREA DEL CHAT */}
              <div ref={chatContainerRef} className="flex-grow bg-gray-100 p-4 overflow-y-auto border-l-4 border-r-4 border-yellow-600">
                {conversacion.length === 0 ? (
                  <div className="text-center text-gray-600 mt-8">
                    <MessageSquare className="w-12 h-12 mx-auto mb-4 text-yellow-600" />
                    <p className="text-lg font-semibold">¡Hola! Soy Tesla IA 🤖</p>
                    <p className="text-sm mt-2">
                      {esCotizacion && "Te ayudo a crear la mejor cotización. ¿Empezamos?"}
                      {esProyecto && "Te ayudo a planificar tu proyecto paso a paso. ¿Empezamos?"}
                      {esInforme && "Te ayudo a generar un informe profesional. ¿Empezamos?"}
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {conversacion.map((mensaje, index) => (
                      <div key={index} className={`flex ${mensaje.tipo === 'usuario' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] p-4 rounded-2xl ${
                          mensaje.tipo === 'usuario' 
                            ? 'bg-yellow-600 text-black ml-8' 
                            : 'bg-white border-2 border-gray-300 text-gray-800 mr-8'
                        }`}>
                          <p className="text-sm font-medium">{mensaje.mensaje}</p>
                          {mensaje.tipo === 'asistente' && (
                            <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
                              <Zap className="w-3 h-3" />
                              Tesla IA
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                    
                    {analizando && (
                      <div className="flex justify-start">
                        <div className="bg-white border-2 border-gray-300 p-4 rounded-2xl mr-8">
                          <div className="flex items-center gap-2 text-gray-600">
                            <Loader className="w-4 h-4 animate-spin" />
                            <span className="text-sm">Tesla IA está analizando...</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* BOTONES CONTEXTUALES */}
              {botonesContextuales.length > 0 && (
                <div className="px-4 py-3 bg-gray-50 border-l-4 border-r-4 border-yellow-600">
                  <p className="text-xs font-semibold text-gray-600 mb-2">💡 Sugerencias rápidas:</p>
                  <div className="flex flex-wrap gap-2">
                    {botonesContextuales.map((boton, index) => (
                      <button
                        key={index}
                        onClick={() => enviarRespuestaRapida(boton)}
                        className="px-3 py-2 bg-yellow-100 hover:bg-yellow-200 text-gray-800 rounded-lg text-sm border border-yellow-300 transition-all duration-200 hover:scale-105">
                        {boton}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              
              {/* INPUT DEL CHAT */}
              <div className="p-4 bg-white border-l-4 border-r-4 border-b-4 border-yellow-600 rounded-b-2xl">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={inputChat}
                    onChange={(e) => setInputChat(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && !analizando && handleEnviarMensajeChat()}
                    placeholder="Escribe tu mensaje o usa los botones de sugerencias..."
                    className="flex-grow p-3 border-2 border-gray-300 rounded-xl focus:border-yellow-500 focus:outline-none text-gray-800"
                    disabled={analizando}
                  />
                  <button 
                    onClick={handleEnviarMensajeChat} 
                    disabled={analizando || !inputChat.trim()}
                    className="p-3 bg-yellow-600 hover:bg-yellow-500 disabled:bg-gray-400 text-black rounded-xl transition-all duration-300 hover:scale-105 disabled:scale-100">
                    <Send className="w-6 h-6" />
                  </button>
                </div>
                
                <div className="flex justify-between items-center mt-4">
                  <button 
                    onClick={() => setPaso(1)} 
                    className="px-4 py-2 bg-gray-300 hover:bg-gray-400 text-gray-800 rounded-lg transition-all">
                    ← Volver a Configuración
                  </button>
                  
                  <button 
                    onClick={() => setPaso(3)} 
                    disabled={!(cotizacion || proyecto || informe)}
                    className="px-6 py-2 bg-green-600 hover:bg-green-500 disabled:bg-gray-400 text-white font-bold rounded-lg transition-all disabled:cursor-not-allowed flex items-center gap-2">
                    <Edit className="w-5 h-5" />
                    {(cotizacion || proyecto || informe) ? 'Ir a Finalización' : `Esperando ${esCotizacion ? 'cotización' : esProyecto ? 'proyecto' : 'informe'}...`}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* PASO 3: FINALIZACIÓN */}
          {paso === 3 && (
            <div className="space-y-6">
              
              {/* FINALIZACIÓN DE COTIZACIÓN */}
              {cotizacion && (
                <div className="bg-white rounded-2xl p-8 shadow-xl border-4 border-yellow-600">
                  <div className="border-b-2 border-gray-200 pb-6 mb-6">
                    <div className="flex justify-between items-start">
                      <div>
                        <h2 className="text-3xl font-bold text-gray-800">COTIZACIÓN #{cotizacion.numero || 'COT-001'}</h2>
                        <p className="text-gray-600 mt-2">Cliente: <span className="font-semibold">{cotizacion.cliente || 'Cliente'}</span></p>
                        <p className="text-gray-600">Proyecto: <span className="font-semibold">{cotizacion.proyecto || 'Proyecto'}</span></p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">Fecha: {new Date().toLocaleDateString()}</p>
                        <p className="text-sm text-gray-600">Vigencia: 30 días</p>
                      </div>
                    </div>
                  </div>

                  {/* ITEMS DE LA COTIZACIÓN */}
                  <div className="space-y-4">
                    <h3 className="text-xl font-bold text-gray-800 border-b border-gray-200 pb-2">DETALLE DE LA COTIZACIÓN</h3>
                    {cotizacion.items && cotizacion.items.map((item, index) => (
                      <div key={index} className="bg-gray-50 p-4 rounded-xl border border-gray-200">
                        <div className="grid grid-cols-12 gap-4 items-center">
                          <div className="col-span-6">
                            <p className="font-semibold text-gray-800">{item.descripcion}</p>
                            {item.capitulo && <p className="text-sm text-gray-600">Capítulo: {item.capitulo}</p>}
                          </div>
                          <div className="col-span-2 text-center">
                            <input
                              type="number"
                              value={item.cantidad}
                              onChange={(e) => {
                                const newItems = [...cotizacion.items];
                                newItems[index].cantidad = parseFloat(e.target.value) || 0;
                                setCotizacion({...cotizacion, items: newItems});
                              }}
                              className="w-full p-2 border border-gray-300 rounded text-center"
                            />
                            <p className="text-xs text-gray-500 mt-1">Cantidad</p>
                          </div>
                          <div className="col-span-2 text-center">
                            <input
                              type="number"
                              step="0.01"
                              value={item.precioUnitario}
                              onChange={(e) => {
                                const newItems = [...cotizacion.items];
                                newItems[index].precioUnitario = parseFloat(e.target.value) || 0;
                                setCotizacion({...cotizacion, items: newItems});
                              }}
                              className="w-full p-2 border border-gray-300 rounded text-center"
                            />
                            <p className="text-xs text-gray-500 mt-1">Precio Unit.</p>
                          </div>
                          <div className="col-span-2 text-center">
                            <p className="font-bold text-gray-800">S/ {(item.cantidad * item.precioUnitario).toFixed(2)}</p>
                            <p className="text-xs text-gray-500 mt-1">Total</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* TOTALES */}
                  <div className="border-t-2 border-gray-200 pt-6 mt-6">
                    <div className="flex justify-end">
                      <div className="w-80">
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span>Subtotal:</span>
                            <span className="font-semibold">S/ {totales.subtotal}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>IGV (18%):</span>
                            <span className="font-semibold">S/ {totales.igv}</span>
                          </div>
                          <div className="border-t border-gray-300 pt-2 flex justify-between text-xl font-bold text-green-600">
                            <span>TOTAL:</span>
                            <span>S/ {totales.total}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* FINALIZACIÓN DE PROYECTO */}
              {proyecto && (
                <div className="bg-white rounded-2xl p-8 shadow-xl border-4 border-blue-600">
                  <div className="border-b-2 border-gray-200 pb-6 mb-6">
                    <h2 className="text-3xl font-bold text-gray-800 flex items-center gap-3">
                      <Layout className="w-8 h-8 text-blue-600" />
                      PROYECTO: {nombreProyecto || 'Nuevo Proyecto'}
                    </h2>
                    <p className="text-gray-600 mt-2">Cliente: <span className="font-semibold">{clienteProyecto}</span></p>
                    <p className="text-gray-600">ID: <span className="font-semibold">{proyecto.id || 'PROJ-' + Date.now()}</span></p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-blue-50 rounded-xl p-6 text-center">
                      <TrendingUp className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                      <p className="text-blue-800 font-bold text-2xl">S/ {presupuestoEstimado || '0'}</p>
                      <p className="text-blue-600 text-sm">Presupuesto</p>
                    </div>
                    <div className="bg-green-50 rounded-xl p-6 text-center">
                      <Clock className="w-8 h-8 text-green-600 mx-auto mb-2" />
                      <p className="text-green-800 font-bold text-2xl">{duracionMeses || '0'}</p>
                      <p className="text-green-600 text-sm">Meses</p>
                    </div>
                    <div className="bg-purple-50 rounded-xl p-6 text-center">
                      <Target className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                      <p className="text-purple-800 font-bold text-2xl">0%</p>
                      <p className="text-purple-600 text-sm">Avance</p>
                    </div>
                  </div>

                  <div className="mt-6 bg-gray-50 rounded-xl p-6">
                    <h3 className="text-lg font-bold text-gray-800 mb-3">📋 Descripción del Proyecto</h3>
                    <p className="text-gray-600">{contextoUsuario}</p>
                  </div>
                </div>
              )}

              {/* FINALIZACIÓN DE INFORME */}
              {informe && (
                <div className="bg-white rounded-2xl p-8 shadow-xl border-4 border-green-600">
                  <div className="border-b-2 border-gray-200 pb-6 mb-6">
                    <h2 className="text-3xl font-bold text-gray-800 flex items-center gap-3">
                      <BookOpen className="w-8 h-8 text-green-600" />
                      INFORME {esComplejo ? 'EJECUTIVO' : 'SIMPLE'}
                    </h2>
                    <p className="text-gray-600 mt-2">Proyecto Base: <span className="font-semibold">{proyectosMock.find(p => p.id === proyectoSeleccionado)?.nombre || 'General'}</span></p>
                    <p className="text-gray-600">Formato: <span className="font-semibold">{formatoInforme.toUpperCase()}</span></p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-green-50 rounded-xl p-6">
                      <h3 className="font-bold text-green-800 mb-3">📊 Contenido Incluido</h3>
                      <ul className="space-y-2 text-sm text-green-700">
                        <li className="flex items-center gap-2">
                          <CheckCircle className="w-4 h-4" />
                          Resumen ejecutivo
                        </li>
                        <li className="flex items-center gap-2">
                          <CheckCircle className="w-4 h-4" />
                          Análisis de datos
                        </li>
                        <li className="flex items-center gap-2">
                          <CheckCircle className="w-4 h-4" />
                          Conclusiones
                        </li>
                        {esComplejo && (
                          <>
                            <li className="flex items-center gap-2">
                              <CheckCircle className="w-4 h-4" />
                              Gráficos y tablas
                            </li>
                            <li className="flex items-center gap-2">
                              <CheckCircle className="w-4 h-4" />
                              Formato APA
                            </li>
                          </>
                        )}
                      </ul>
                    </div>
                    
                    <div className="bg-blue-50 rounded-xl p-6">
                      <h3 className="font-bold text-blue-800 mb-3">⚙️ Configuración</h3>
                      <div className="space-y-2 text-sm text-blue-700">
                        <p><span className="font-semibold">Formato:</span> {formatoInforme.toUpperCase()}</p>
                        <p><span className="font-semibold">Gráficos:</span> {incluirGraficos ? 'Incluidos' : 'No incluidos'}</p>
                        <p><span className="font-semibold">Páginas est.:</span> {esComplejo ? '15-25' : '5-10'}</p>
                        <p><span className="font-semibold">Tiempo gen.:</span> 2-3 minutos</p>
                      </div>
                    </div>
                  </div>

                  <div className="mt-6 bg-gray-50 rounded-xl p-6">
                    <h3 className="text-lg font-bold text-gray-800 mb-3">📋 Propósito del Informe</h3>
                    <p className="text-gray-600">{contextoUsuario}</p>
                  </div>
                </div>
              )}

              {/* BOTONES DE ACCIÓN UNIVERSALES */}
              <div className="flex gap-4">
                <button 
                  onClick={() => setPaso(2)} 
                  className="px-6 py-3 bg-gray-600 hover:bg-gray-500 text-white rounded-xl transition-all">
                  ← Volver al Chat
                </button>
                
                <div className="flex-1 flex gap-4">
                  <button 
                    onClick={() => handleDescargar(esCotizacion ? 'cotizacion' : esProyecto ? 'proyecto' : 'informe', 'pdf')} 
                    disabled={descargando?.includes('pdf')}
                    className="flex-1 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 disabled:from-gray-600 disabled:to-gray-500 text-white py-3 rounded-xl font-bold transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2">
                    {descargando?.includes('pdf') ? (
                      <>
                        <Loader className="w-5 h-5 animate-spin" />
                        Generando PDF...
                      </>
                    ) : (
                      <>
                        <FileText className="w-5 h-5" />
                        Descargar PDF
                      </>
                    )}
                  </button>
                  
                  <button 
                    onClick={() => handleDescargar(esCotizacion ? 'cotizacion' : esProyecto ? 'proyecto' : 'informe', 'word')} 
                    disabled={descargando?.includes('word')}
                    className="flex-1 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 disabled:from-gray-600 disabled:to-gray-500 text-white py-3 rounded-xl font-bold transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2">
                    {descargando?.includes('word') ? (
                      <>
                        <Loader className="w-5 h-5 animate-spin" />
                        Generando Word...
                      </>
                    ) : (
                      <>
                        <Download className="w-5 h-5" />
                        Descargar Word
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // ============================================
  // PANTALLA POR DEFECTO
  // ============================================
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6">
      <div className="max-w-5xl mx-auto text-center">
        <h1 className="text-4xl font-bold text-yellow-400 mb-4">Sistema Tesla v3.0</h1>
        <p className="text-gray-300 mb-6">Sistema profesional completamente funcional</p>
        <button 
          onClick={volverAlInicio} 
          className="px-6 py-3 bg-yellow-600 text-black rounded-lg font-bold hover:bg-yellow-500 transition-all">
          Ir al Inicio
        </button>
      </div>
    </div>
  );
};

export default CotizadorTesla30;