// @ts-nocheck
import React, { useState, useRef, useEffect } from 'react';
import { Upload, MessageSquare, FileText, Download, Zap, Send, Loader, Edit, Save, AlertCircle, CheckCircle, X, RefreshCw, Home, FolderOpen, Eye, EyeOff, Folder, Users, TrendingUp, Clock, BarChart3, FileCheck, Briefcase, ChevronDown, ChevronUp, Layout, Layers, BookOpen, Calculator, Calendar, Target, Archive, Settings, PieChart, Maximize2, Minimize2, Plus, Trash2, Building2, MapPin, Phone, Mail } from 'lucide-react';
import PiliAvatar from './components/PiliAvatar';
import ChatIA from './components/ChatIA';
import VistaPrevia from './components/VistaPrevia';

const CotizadorTesla30 = () => {
  // ============================================
  // ESTADOS PRINCIPALES
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
  const [error, setError] = useState('');
  const [exito, setExito] = useState('');
  const [servicioSeleccionado, setServicioSeleccionado] = useState('');
  const [industriaSeleccionada, setIndustriaSeleccionada] = useState('');
  const [descargando, setDescargando] = useState(null);
  const [logoBase64, setLogoBase64] = useState('');
  const [botonesContextuales, setBotonesContextuales] = useState([]);

  // Estados para vista previa HTML editable
  const [htmlPreview, setHtmlPreview] = useState('');
  const [mostrarPreview, setMostrarPreview] = useState(false);
  const [modoEdicion, setModoEdicion] = useState(true);  // ✅ TRUE por defecto para mostrar tabla editable
  const [datosEditables, setDatosEditables] = useState(null);
  const [ocultarIGV, setOcultarIGV] = useState(false);
  const [ocultarPreciosUnitarios, setOcultarPreciosUnitarios] = useState(false);

  // ✅ Estados para personalización de documentos (NEW)
  const [esquemaColores, setEsquemaColores] = useState('azul-tesla'); // azul-tesla, rojo-energia, verde-ecologico, personalizado
  const [fuenteDocumento, setFuenteDocumento] = useState('Calibri'); // Calibri, Arial, Times New Roman
  const [tamañoFuente, setTamañoFuente] = useState(11); // 10, 11, 12
  const [mostrarLogo, setMostrarLogo] = useState(true);
  const [posicionLogo, setPosicionLogo] = useState('center'); // left, center, right
  const [mostrarPanelPersonalizacion, setMostrarPanelPersonalizacion] = useState(false);

  // Estados específicos para cada tipo
  const [cotizacion, setCotizacion] = useState(null);
  const [proyecto, setProyecto] = useState(null);
  const [informe, setInforme] = useState(null);

  // Estados específicos para proyectos
  const [nombreProyecto, setNombreProyecto] = useState('');
  const [clienteProyecto, setClienteProyecto] = useState('');
  const [presupuestoEstimado, setPresupuestoEstimado] = useState('');
  const [duracionMeses, setDuracionMeses] = useState('');

  // Estados específicos para informes
  const [proyectoSeleccionado, setProyectoSeleccionado] = useState('');
  const [formatoInforme, setFormatoInforme] = useState('word');
  const [incluirGraficos, setIncluirGraficos] = useState(true);

  // ✅ Estados universales de cliente (para todos los 6 tipos de documentos)
  const [datosCliente, setDatosCliente] = useState({
    nombre: '',
    ruc: '',
    direccion: '',
    telefono: '',
    email: ''
  });
  const [clienteSeleccionadoId, setClienteSeleccionadoId] = useState(null);
  const [listaClientes, setListaClientes] = useState([]);
  const [guardandoCliente, setGuardandoCliente] = useState(false);

  // Referencias
  const chatContainerRef = useRef(null);
  const fileInputLogoRef = useRef(null);
  const previewRef = useRef(null);

  // ============================================
  // DATOS DE CONFIGURACIÓN
  // ============================================

  const [datosEmpresa] = useState({
    nombre: 'TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.',
    ruc: '20601138787',
    direccion: 'Jr. Los Narcisos Mz H lote 4 Urb. Los jardines de San Calos',
    telefono: '906315961',
    email: 'ingenieria.teslaelectricidad@gmail.com',
    ciudad: 'Huanacayo, Junin - Perú'
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

  const proyectosMock = [
    { id: 'PROJ-2025-001', nombre: 'Instalación Eléctrica Torre Office', cliente: 'Constructora Lima', tipo: 'electricidad' },
    { id: 'PROJ-2025-002', nombre: 'Sistema CCTV Planta Industrial', cliente: 'Industrial Perú S.A.', tipo: 'cctv' },
    { id: 'PROJ-2025-003', nombre: 'Automatización Línea Producción', cliente: 'Manufactura XYZ', tipo: 'automatizacion-industrial' }
  ];

  // ============================================
  // FUNCIONES PRINCIPALES
  // ============================================

  const volverAlInicio = () => {
    setPantallaActual('inicio');
    setTipoFlujo(null);
    setPaso(1);
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
    setHtmlPreview('');
    setMostrarPreview(false);
    setDatosEditables(null);
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
    setHtmlPreview('');
    setMostrarPreview(false);
    setDatosEditables(null);
  };

  // ============================================
  // ✅ FUNCIONES DE GESTIÓN DE CLIENTES
  // ============================================

  // Cargar lista de clientes desde la BD
  const cargarListaClientes = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/clientes/');
      if (response.ok) {
        const clientes = await response.json();
        setListaClientes(clientes);
      }
    } catch (error) {
      console.error('Error cargando clientes:', error);
    }
  };

  // Cargar datos de un cliente específico (auto-relleno)
  const cargarDatosCliente = async (e) => {
    const clienteId = e.target.value;

    if (!clienteId) {
      // Nuevo cliente - limpiar formulario
      setClienteSeleccionadoId(null);
      setDatosCliente({
        nombre: '',
        ruc: '',
        direccion: '',
        telefono: '',
        email: ''
      });
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/clientes/${clienteId}`);
      if (response.ok) {
        const cliente = await response.json();
        setClienteSeleccionadoId(cliente.id);
        setDatosCliente({
          nombre: cliente.nombre || '',
          ruc: cliente.ruc || '',
          direccion: cliente.direccion || '',
          telefono: cliente.telefono || '',
          email: cliente.email || ''
        });
        setExito('✅ Cliente cargado');
      }
    } catch (error) {
      console.error('Error cargando cliente:', error);
      setError('Error al cargar cliente');
    }
  };

  // Guardar cliente en la BD
  const guardarCliente = async () => {
    // Validación básica
    if (!datosCliente.nombre || !datosCliente.ruc) {
      setError('Nombre y RUC son obligatorios');
      return;
    }

    if (datosCliente.ruc.length !== 11) {
      setError('El RUC debe tener 11 dígitos');
      return;
    }

    setGuardandoCliente(true);

    try {
      const url = clienteSeleccionadoId
        ? `http://localhost:8000/api/clientes/${clienteSeleccionadoId}`
        : 'http://localhost:8000/api/clientes/';

      const method = clienteSeleccionadoId ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datosCliente)
      });

      if (response.ok) {
        const clienteGuardado = await response.json();
        setClienteSeleccionadoId(clienteGuardado.id);
        await cargarListaClientes(); // Recargar lista
        setExito(clienteSeleccionadoId ? '✅ Cliente actualizado' : '✅ Cliente guardado');
      } else {
        const errorData = await response.json();
        console.error('❌ Error del backend:', errorData);
        console.error('📋 Datos enviados:', datosCliente);
        throw new Error(JSON.stringify(errorData.detail || errorData) || 'Error al guardar');
      }
    } catch (error) {
      console.error('Error guardando cliente:', error);
      setError(error.message || 'Error al guardar cliente');
    } finally {
      setGuardandoCliente(false);
    }
  };

  // Manejar cambios en el formulario de cliente
  const handleClienteChange = (e) => {
    const { name, value } = e.target;
    setDatosCliente(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // ============================================
  // FUNCIONES DEL CHAT + VISTA PREVIA
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
        contextoPrincipal += `, Proyecto: ${proyectoSeleccionado}, Formato: ${formatoInforme}`;
      }

      const response = await fetch('http://localhost:8000/api/chat/chat-contextualizado', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tipo_flujo: tipoFlujo,
          mensaje: inputChat,
          historial: nuevaConversacion,
          contexto_adicional: contextoPrincipal,
          datos_cliente: datosCliente,  // ¡NUEVO! Enviar datos del cliente
          archivos_procesados: archivos.map(a => ({ nombre: a.nombre, contenido: a.contenidoTexto })),
          generar_html: true // Importante: pedimos HTML preview
        })
      });

      const data = await response.json();

      if (data.success) {
        const mensajeIA = { tipo: 'asistente', mensaje: data.respuesta };
        setConversacion(prev => [...prev, mensajeIA]);

        // ACTUALIZAR VISTA PREVIA HTML
        if (data.html_preview) {
          setHtmlPreview(data.html_preview);
          setMostrarPreview(true);
        }

        // Manejar datos según el tipo de flujo
        if (tipoFlujo.includes('cotizacion') && data.cotizacion_generada) {
          setCotizacion(data.cotizacion_generada);
          setDatosEditables(data.cotizacion_generada);
        } else if (tipoFlujo.includes('proyecto') && data.proyecto_generado) {
          setProyecto(data.proyecto_generado);
          setDatosEditables(data.proyecto_generado);
        } else if (tipoFlujo.includes('informe') && data.informe_generado) {
          setInforme(data.informe_generado);
          setDatosEditables(data.informe_generado);
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
  // FUNCIÓN DE GENERACIÓN DE DOCUMENTOS
  // ============================================

  const handleGenerarDocumento = async (formato) => {
    try {
      console.log(`📄 Generando ${formato.toUpperCase()}...`);

      // Determinar tipo de documento
      const tipoDocumento = tipoFlujo.includes('cotizacion') ? 'cotizacion' :
        tipoFlujo.includes('proyecto') ? 'proyecto' : 'informe';

      // Obtener datos actuales (USAR DATOS EDITADOS SI EXISTEN)
      const datosOriginales = tipoDocumento === 'cotizacion' ? cotizacion :
        tipoDocumento === 'proyecto' ? proyecto : informe;

      // CRÍTICO: Usar datosEditables si existen (tienen los cambios del usuario)
      const entidad = datosEditables || datosOriginales;

      // Extraer HTML editado de la vista previa
      const previewElement = previewRef.current;
      const htmlEditado = previewElement ? previewElement.innerHTML : htmlPreview;

      // Recalcular totales basados en items editados
      const itemsActuales = entidad.items || [];
      const subtotalCalculado = itemsActuales.reduce((sum, item) =>
        sum + (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || item.precioUnitario || 0)), 0
      );
      const igvCalculado = subtotalCalculado * 0.18;
      const totalCalculado = subtotalCalculado + igvCalculado;

      // Preparar datos para enviar
      const datosParaEnviar = {
        tipo_documento: tipoDocumento,
        numero: entidad.numero || `${tipoDocumento.toUpperCase()}-${Date.now()}`,
        cliente: entidad.cliente || { nombre: "[Cliente]" },
        proyecto: entidad.proyecto || "[Proyecto]",
        descripcion: entidad.descripcion || "",
        items: itemsActuales,
        subtotal: parseFloat(subtotalCalculado.toFixed(2)),
        igv: parseFloat(igvCalculado.toFixed(2)),
        total: parseFloat(totalCalculado.toFixed(2)),
        fecha: new Date().toLocaleDateString('es-PE'),
        vigencia: "30 días"
      };

      console.log('📦 DEBUG - Datos completos a enviar:');
      console.log('  - Cliente:', datosParaEnviar.cliente);
      console.log('  - Proyecto:', datosParaEnviar.proyecto);
      console.log('  - Items:', datosParaEnviar.items);
      console.log('  - Subtotal:', datosParaEnviar.subtotal);
      console.log('  - IGV:', datosParaEnviar.igv);
      console.log('  - Total:', datosParaEnviar.total);
      console.log('  - datosCliente originales:', datosCliente);

      console.log('📦 Datos a enviar:', datosParaEnviar);

      // Llamar al endpoint de generación directa
      const response = await fetch(
        `http://localhost:8000/api/generar-documento-directo?formato=${formato}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            datos: datosParaEnviar,
            html_editado: htmlEditado,
            tipo_plantilla: tipoFlujo  // ej: "cotizacion-simple"
          })
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      // DEBUG: Verificar Content-Type
      const contentType = response.headers.get('Content-Type');
      console.log('🔍 Content-Type recibido:', contentType);

      // Si es JSON, es un error del backend
      if (contentType && contentType.includes('application/json')) {
        const errorData = await response.json();
        throw new Error(`Backend devolvió error: ${JSON.stringify(errorData)}`);
      }

      // Descargar archivo
      const blob = await response.blob();
      console.log('💾 Blob recibido:', blob.size, 'bytes, tipo:', blob.type);

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${tipoDocumento}_${Date.now()}.${formato === 'word' ? 'docx' : 'pdf'}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      console.log(`✅ ${formato.toUpperCase()} descargado exitosamente`);
      alert(`✅ Documento ${formato.toUpperCase()} generado y descargado exitosamente`);

    } catch (error) {
      console.error('❌ Error al generar documento:', error);
      alert(`❌ Error al generar el documento: ${error.message}`);
    }
  };

  // ============================================
  // FUNCIONES DE EDICIÓN HTML
  // ============================================

  const actualizarItem = (index, campo, valor) => {
    if (!datosEditables?.items) return;

    const nuevosItems = [...datosEditables.items];

    // Normalizar nombre de campo (precioUnitario -> precio_unitario)
    const campoNormalizado = campo === 'precioUnitario' ? 'precio_unitario' : campo;

    // Actualizar el campo
    if (campoNormalizado === 'descripcion') {
      nuevosItems[index][campoNormalizado] = valor;
    } else {
      nuevosItems[index][campoNormalizado] = parseFloat(valor) || 0;
    }

    // Recalcular total del item
    if (campoNormalizado === 'cantidad' || campoNormalizado === 'precio_unitario') {
      const cantidad = nuevosItems[index].cantidad || 0;
      const precioUnitario = nuevosItems[index].precio_unitario || 0;
      nuevosItems[index].total = cantidad * precioUnitario;
    }

    const nuevosDatos = { ...datosEditables, items: nuevosItems };
    setDatosEditables(nuevosDatos);

    console.log(`✏️ Item ${index} editado - ${campoNormalizado}:`, valor, '| Item completo:', nuevosItems[index]);

    // Actualizar estado específico
    if (tipoFlujo.includes('cotizacion')) {
      setCotizacion(nuevosDatos);
    } else if (tipoFlujo.includes('proyecto')) {
      setProyecto(nuevosDatos);
    } else if (tipoFlujo.includes('informe')) {
      setInforme(nuevosDatos);
    }

    // Regenerar HTML
    regenerarHTML();
  };

  const agregarItem = () => {
    if (!datosEditables) return;

    const nuevoItem = {
      descripcion: 'Nuevo item',
      cantidad: 1,
      precioUnitario: 0,
      total: 0,
      capitulo: 'GENERAL'
    };

    const nuevosItems = [...(datosEditables.items || []), nuevoItem];
    const nuevosDatos = { ...datosEditables, items: nuevosItems };
    setDatosEditables(nuevosDatos);

    if (tipoFlujo.includes('cotizacion')) {
      setCotizacion(nuevosDatos);
    }

    regenerarHTML();
  };

  const eliminarItem = (index) => {
    if (!datosEditables?.items) return;

    const nuevosItems = datosEditables.items.filter((_, i) => i !== index);
    const nuevosDatos = { ...datosEditables, items: nuevosItems };
    setDatosEditables(nuevosDatos);

    if (tipoFlujo.includes('cotizacion')) {
      setCotizacion(nuevosDatos);
    }

    regenerarHTML();
  };

  const regenerarHTML = () => {
    if (!datosEditables) return;

    // Generar HTML actualizado basado en los datos editables
    let htmlActualizado = generarHTMLPreview(datosEditables);
    setHtmlPreview(htmlActualizado);
  };

  const generarHTMLPreview = (datos) => {
    if (tipoFlujo.includes('cotizacion')) {
      return generarHTMLCotizacion(datos);
    } else if (tipoFlujo.includes('proyecto')) {
      return generarHTMLProyecto(datos);
    } else if (tipoFlujo.includes('informe')) {
      return generarHTMLInforme(datos);
    }
    return '';
  };

  const generarHTMLCotizacion = (datos) => {
    const totales = calcularTotales(datos?.items || []);

    return `
      <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: white; color: #333;">
        <div style="border-bottom: 3px solid #8B0000; padding-bottom: 20px; margin-bottom: 20px;">
          <h1 style="color: #8B0000; margin: 0; font-size: 28px;">COTIZACIÓN</h1>
          <p style="color: #D4AF37; font-weight: bold; margin: 5px 0;">Tesla Electricidad y Automatización S.A.C.</p>
          <p style="color: #666; margin: 0;">RUC: 20601138787</p>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #8B0000; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">DETALLES DE LA COTIZACIÓN</h2>
          <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
            <thead>
              <tr style="background: #8B0000; color: white;">
                <th style="padding: 12px; text-align: left; border: 1px solid #8B0000;">DESCRIPCIÓN</th>
                <th style="padding: 12px; text-align: center; border: 1px solid #8B0000; width: 80px;">CANT.</th>
                ${!ocultarPreciosUnitarios ? '<th style="padding: 12px; text-align: center; border: 1px solid #8B0000; width: 100px;">P. UNIT.</th>' : ''}
                <th style="padding: 12px; text-align: center; border: 1px solid #8B0000; width: 100px;">TOTAL</th>
              </tr>
            </thead>
            <tbody>
              ${(datos?.items || []).map((item, index) => `
                <tr style="border-bottom: 1px solid #ddd;">
                  <td style="padding: 10px; border: 1px solid #ddd;">${item.descripcion}</td>
                  <td style="padding: 10px; text-align: center; border: 1px solid #ddd;">${item.cantidad}</td>
                  ${!ocultarPreciosUnitarios ? `<td style="padding: 10px; text-align: center; border: 1px solid #ddd;">S/ ${item.precioUnitario?.toFixed(2) || '0.00'}</td>` : ''}
                  <td style="padding: 10px; text-align: center; border: 1px solid #ddd; font-weight: bold;">S/ ${((item.cantidad || 0) * (item.precioUnitario || 0)).toFixed(2)}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
        
        <div style="margin-top: 30px; text-align: right;">
          <div style="display: inline-block; background: #f9f9f9; padding: 20px; border-radius: 8px; border: 2px solid #D4AF37;">
            <div style="margin-bottom: 10px;">
              <span style="font-weight: bold;">Subtotal:</span>
              <span style="margin-left: 20px; font-size: 18px;">S/ ${totales.subtotal}</span>
            </div>
            ${!ocultarIGV ? `
              <div style="margin-bottom: 10px;">
                <span style="font-weight: bold;">IGV (18%):</span>
                <span style="margin-left: 20px; font-size: 18px;">S/ ${totales.igv}</span>
              </div>
            ` : ''}
            <div style="border-top: 2px solid #8B0000; padding-top: 10px; margin-top: 15px;">
              <span style="font-weight: bold; font-size: 20px; color: #8B0000;">TOTAL:</span>
              <span style="margin-left: 20px; font-size: 24px; font-weight: bold; color: #8B0000;">S/ ${ocultarIGV ? totales.subtotal : totales.total}</span>
            </div>
          </div>
        </div>
        
        <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #D4AF37; color: #666; font-size: 14px;">
          <p><strong>Condiciones:</strong> Precios ${ocultarIGV ? 'no incluyen' : 'incluyen'} IGV. Válido por 30 días.</p>
          <p><strong>Contacto:</strong> ${datosEmpresa.telefono} | ${datosEmpresa.email}</p>
        </div>
      </div>
    `;
  };

  const generarHTMLProyecto = (datos) => {
    return `
      <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: white; color: #333;">
        <div style="border-bottom: 3px solid #2563eb; padding-bottom: 20px; margin-bottom: 20px;">
          <h1 style="color: #2563eb; margin: 0; font-size: 28px;">PROYECTO</h1>
          <p style="color: #D4AF37; font-weight: bold; margin: 5px 0;">Tesla Electricidad y Automatización S.A.C.</p>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2563eb; margin-bottom: 15px;">${nombreProyecto || 'Nuevo Proyecto'}</h2>
          <p><strong>Cliente:</strong> ${clienteProyecto}</p>
          <p><strong>Presupuesto:</strong> S/ ${presupuestoEstimado}</p>
          <p><strong>Duración:</strong> ${duracionMeses} meses</p>
        </div>
        
        <div style="margin-bottom: 30px; background: #f8fafc; padding: 20px; border-radius: 8px; border-left: 4px solid #2563eb;">
          <h3 style="color: #2563eb; margin-top: 0;">Descripción del Proyecto</h3>
          <p>${contextoUsuario}</p>
        </div>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #D4AF37; color: #666; font-size: 14px;">
          <p><strong>Contacto:</strong> ${datosEmpresa.telefono} | ${datosEmpresa.email}</p>
        </div>
      </div>
    `;
  };

  const generarHTMLInforme = (datos) => {
    return `
      <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: white; color: #333;">
        <div style="border-bottom: 3px solid #16a34a; padding-bottom: 20px; margin-bottom: 20px;">
          <h1 style="color: #16a34a; margin: 0; font-size: 28px;">INFORME ${tipoFlujo.includes('ejecutivo') ? 'EJECUTIVO' : 'SIMPLE'}</h1>
          <p style="color: #D4AF37; font-weight: bold; margin: 5px 0;">Tesla Electricidad y Automatización S.A.C.</p>
        </div>
        
        <div style="margin-bottom: 30px;">
          <p><strong>Proyecto:</strong> ${proyectosMock.find(p => p.id === proyectoSeleccionado)?.nombre || 'General'}</p>
          <p><strong>Fecha:</strong> ${new Date().toLocaleDateString()}</p>
          <p><strong>Formato:</strong> ${formatoInforme.toUpperCase()}</p>
        </div>
        
        <div style="margin-bottom: 30px; background: #f0fdf4; padding: 20px; border-radius: 8px; border-left: 4px solid #16a34a;">
          <h3 style="color: #16a34a; margin-top: 0;">Contenido del Informe</h3>
          <p>${contextoUsuario}</p>
        </div>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #D4AF37; color: #666; font-size: 14px;">
          <p><strong>Contacto:</strong> ${datosEmpresa.telefono} | ${datosEmpresa.email}</p>
        </div>
      </div>
    `;
  };

  const calcularTotales = (items = []) => {
    const subtotal = items.reduce((sum, item) => sum + ((item.cantidad || 0) * (item.precioUnitario || 0)), 0);
    return {
      subtotal: subtotal.toFixed(2),
      igv: (subtotal * 0.18).toFixed(2),
      total: (subtotal * 1.18).toFixed(2)
    };
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
  // FUNCIONES DE DESCARGA
  // ============================================

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
      console.log(`📄 Generando ${formato.toUpperCase()} con V2 (sin HTML parsing)...`);
      setExito(`Generando ${formato.toUpperCase()}...`);

      // Usar datos editables si existen
      const datosFinales = datosEditables || entidad;
      const itemsActuales = datosFinales?.items || [];

      // 🐛 DEBUG: Ver qué datos tenemos
      console.log('🔍 DEBUG COMPLETO handleDescargar:');
      console.log('  datosEditables:', datosEditables);
      console.log('  datosEditables?.items:', datosEditables?.items);
      console.log('  entidad:', entidad);
      console.log('  datosFinales:', datosFinales);
      console.log('  itemsActuales:', itemsActuales);

      // Recalcular totales
      const subtotalCalculado = itemsActuales.reduce((sum, item) =>
        sum + (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || item.precioUnitario || 0)), 0
      );
      const igvCalculado = subtotalCalculado * 0.18;
      const totalCalculado = subtotalCalculado + igvCalculado;

      // ✅ V2: Preparar datos JSON limpios (SIN HTML)
      const datosLimpios = {
        tipo_documento: tipoFlujo,  // cotizacion-simple, proyecto-complejo, informe-tecnico, etc.
        numero: datosFinales?.numero || `COT-${Date.now()}`,
        fecha: new Date().toLocaleDateString('es-PE'),
        vigencia: '30 días',

        // Cliente (como objeto completo)
        cliente: {
          nombre: datosCliente.nombre || '[Cliente]',
          ruc: datosCliente.ruc || '',
          direccion: datosCliente.direccion || '',
          telefono: datosCliente.telefono || '',
          email: datosCliente.email || ''
        },

        // Proyecto
        proyecto: nombreProyecto || '[Proyecto]',
        descripcion: contextoUsuario || '',

        // Items (desde datosEditables, NO desde HTML)
        items: itemsActuales.map(item => ({
          descripcion: item.descripcion || '',
          cantidad: parseFloat(item.cantidad || 0),
          unidad: item.unidad || 'und',
          precio_unitario: parseFloat(item.precio_unitario || item.precioUnitario || 0)
        })),

        // Totales
        subtotal: parseFloat(subtotalCalculado.toFixed(2)),
        igv: parseFloat(igvCalculado.toFixed(2)),
        total: parseFloat(totalCalculado.toFixed(2)),

        observaciones: datosFinales?.observaciones || 'Precios incluyen IGV',

        // ✅ Opciones de personalización profesional
        personalizacion: {
          esquema_colores: esquemaColores,  // azul-tesla, rojo-energia, verde-ecologico, personalizado
          fuente: fuenteDocumento,  // Calibri, Arial, Times New Roman
          tamano_fuente: tamañoFuente,  // 10, 11, 12
          mostrar_logo: mostrarLogo,
          posicion_logo: posicionLogo,  // left, center, right
          logo_base64: logoBase64 || null,
          ocultar_igv: ocultarIGV,
          ocultar_precios_unitarios: ocultarPreciosUnitarios
        }
      };

      console.log('📦 Datos limpios V2 a enviar:', datosLimpios);
      console.log('  - Tipo:', datosLimpios.tipo_documento);
      console.log('  - Cliente:', datosLimpios.cliente.nombre);
      console.log('  - Items:', datosLimpios.items.length);
      console.log('  - Items detalle:', datosLimpios.items);
      console.log('  - Total:', datosLimpios.total);
      console.log('  - Personalización:', datosLimpios.personalizacion);

      // ✅ V2: Llamar endpoint limpio (SIN HTML)
      const response = await fetch(
        `http://localhost:8000/api/generar-documento-v2?formato=${formato}&guardar_bd=false`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(datosLimpios)  // Solo JSON, sin HTML
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      // Descargar archivo
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `cotizacion_${datosLimpios.numero}.${formato === 'word' ? 'docx' : 'pdf'}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      console.log(`✅ ${formato.toUpperCase()} V2 descargado exitosamente`);
      setExito(`✅ ${formato.toUpperCase()} descargado exitosamente`);
      setTimeout(() => setExito(''), 4000);

    } catch (error) {
      console.error('❌ Error al descargar V2:', error);
      setError(`Error al generar el documento: ${error.message}`);
    } finally {
      setDescargando(null);
    }
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

  // ✅ Cargar lista de clientes al montar el componente
  useEffect(() => {
    cargarListaClientes();
  }, []);

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
                    onClick={() => iniciarFlujo('cotizacion-simple')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-yellow-900 hover:to-yellow-800 p-4 rounded-xl border-2 border-gray-700 hover:border-yellow-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <Zap className="w-6 h-6 text-yellow-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Cotización Simple</p>
                        <p className="text-gray-400 text-sm">Vista previa en tiempo real - 5 a 15 minutos</p>
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
                        <p className="text-gray-400 text-sm">Análisis detallado con edición avanzada</p>
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
                        <p className="text-gray-400 text-sm">Gestión básica con vista previa</p>
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
                        <p className="text-gray-400 text-sm">Gantt, hitos y seguimiento avanzado</p>
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
                        <p className="text-gray-400 text-sm">PDF básico con vista previa editable</p>
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
                        <p className="text-gray-400 text-sm">Word APA, tablas y gráficos automáticos</p>
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
  // PANTALLA: FLUJO DE PASOS MEJORADO
  // ============================================

  if (pantallaActual === 'flujo-pasos') {
    const esCotizacion = tipoFlujo.includes('cotizacion');
    const esProyecto = tipoFlujo.includes('proyecto');
    const esInforme = tipoFlujo.includes('informe');
    const esComplejo = tipoFlujo.includes('complejo') || tipoFlujo.includes('compleja') || tipoFlujo.includes('ejecutivo');

    let colores = { primary: 'yellow', border: 'yellow-700', bg: 'yellow-600' };
    if (esProyecto) colores = { primary: 'blue', border: 'blue-700', bg: 'blue-600' };
    else if (esInforme) colores = { primary: 'green', border: 'green-700', bg: 'green-600' };

    const configuracion = {
      'cotizacion-simple': { titulo: '⚡ Cotización Simple', desc: 'Vista previa en tiempo real - 5 a 15 minutos', icon: Zap },
      'cotizacion-compleja': { titulo: '📄 Cotización Compleja', desc: 'Análisis detallado con edición avanzada', icon: Layers },
      'proyecto-simple': { titulo: '📁 Proyecto Simple', desc: 'Gestión básica con vista previa', icon: Folder },
      'proyecto-complejo': { titulo: '🏗️ Proyecto Complejo', desc: 'Gantt, hitos y seguimiento avanzado', icon: Layout },
      'informe-simple': { titulo: '📄 Informe Simple', desc: 'PDF básico con vista previa editable', icon: FileText },
      'informe-ejecutivo': { titulo: '📊 Informe Ejecutivo', desc: 'Word APA, tablas y gráficos automáticos', icon: BarChart3 }
    };

    const config = configuracion[tipoFlujo];
    const IconoTitulo = config.icon;

    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white">
        <div className="max-w-full mx-auto">
          {/* HEADER FIJO */}
          <div className="bg-gradient-to-r from-red-950 via-red-900 to-black p-4 border-b-2 border-yellow-600 shadow-2xl">
            <div className="max-w-7xl mx-auto flex items-center justify-between">
              <div className="flex items-center gap-3">
                <IconoTitulo className="w-8 h-8 text-yellow-400" />
                <div>
                  <h1 className="text-2xl font-bold text-yellow-400">{config.titulo}</h1>
                  <p className="text-gray-300 text-sm">{config.desc}</p>
                </div>
              </div>

              {/* INDICADOR DE PASOS COMPACTO */}
              <div className="flex items-center gap-4">
                {[1, 2, 3].map(num => (
                  <div key={num} className="flex items-center gap-2">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${paso >= num ? 'bg-yellow-600 text-black' : 'border border-gray-600 text-gray-600'
                      }`}>
                      {num}
                    </div>
                    {num < 3 && <div className={`w-8 h-1 ${paso > num ? 'bg-yellow-600' : 'bg-gray-600'}`} />}
                  </div>
                ))}

                <button onClick={volverAlInicio} className="ml-6 px-4 py-2 bg-red-800 hover:bg-red-700 text-yellow-400 rounded-lg font-semibold flex items-center gap-2 transition-all">
                  <Home className="w-4 h-4" />
                  Inicio
                </button>
              </div>
            </div>
          </div>

          {/* ALERTAS */}
          <div className="max-w-7xl mx-auto px-6 pt-4">
            {error && <Alerta tipo="error" mensaje={error} onClose={() => setError('')} />}
            {exito && <Alerta tipo="exito" mensaje={exito} onClose={() => setExito('')} />}
          </div>

          {/* CONTENIDO PRINCIPAL */}
          <div className="p-6">
            {/* PASO 1: CONFIGURACIÓN */}
            {paso === 1 && (
              <div className="max-w-5xl mx-auto space-y-6">

                {/* LOGO UNIVERSAL (TODOS LOS SERVICIOS) */}
                <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-600 shadow-xl">
                  <h2 className="text-2xl font-bold mb-4 text-yellow-400 flex items-center gap-2">
                    🎨 Logo Empresa (Aparecerá en el documento final)
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
                        className="w-full bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 text-black px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-xl border-2 border-yellow-400 transition-all duration-300 hover:scale-105">
                        <Upload className="w-5 h-5" />
                        {logoBase64 ? 'Cambiar Logo' : 'Subir Logo'}
                      </button>
                      <p className="text-xs text-gray-400 mt-2 text-center">
                        PNG, JPG, WebP - Máx 2MB • Se integrará automáticamente en Word
                      </p>
                    </div>

                    {logoBase64 && (
                      <div className="bg-white rounded-xl p-3 border-2 border-yellow-400 shadow-lg">
                        <img src={logoBase64} alt="Logo" className="w-24 h-24 object-contain" />
                        <p className="text-xs text-gray-600 mt-2 text-center font-semibold">✅ Cargado</p>
                      </div>
                    )}
                  </div>
                </div>

                {/* ✅ FORMULARIO UNIVERSAL DE CLIENTE (TODOS LOS 6 TIPOS DE DOCUMENTOS) */}
                <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-600 shadow-xl">
                  <h2 className="text-2xl font-bold mb-6 text-yellow-400 flex items-center gap-3">
                    <Users className="w-7 h-7" />
                    Datos del Cliente
                  </h2>

                  {/* Selector de cliente existente o nuevo */}
                  <div className="mb-6">
                    <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2">
                      <Building2 className="w-5 h-5" />
                      Seleccionar Cliente
                    </label>
                    <select
                      value={clienteSeleccionadoId || ''}
                      onChange={cargarDatosCliente}
                      className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                    >
                      <option value="">+ Nuevo Cliente</option>
                      {listaClientes.map(c => (
                        <option key={c.id} value={c.id}>
                          {c.nombre} - RUC: {c.ruc}
                        </option>
                      ))}
                    </select>
                    <p className="text-xs text-gray-400 mt-1">
                      Selecciona un cliente existente o crea uno nuevo
                    </p>
                  </div>

                  {/* Campos del formulario */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div>
                      <label className="block text-yellow-400 font-semibold mb-2">
                        Nombre/Razón Social *
                      </label>
                      <input
                        type="text"
                        name="nombre"
                        value={datosCliente.nombre}
                        onChange={handleClienteChange}
                        className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                        placeholder="Ej: Constructora ABC S.A.C."
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-yellow-400 font-semibold mb-2">
                        RUC *
                      </label>
                      <input
                        type="text"
                        name="ruc"
                        value={datosCliente.ruc}
                        onChange={handleClienteChange}
                        className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                        placeholder="11 dígitos"
                        maxLength={11}
                        required
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2">
                        <MapPin className="w-4 h-4" />
                        Dirección
                      </label>
                      <input
                        type="text"
                        name="direccion"
                        value={datosCliente.direccion}
                        onChange={handleClienteChange}
                        className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                        placeholder="Ej: Av. Principal 123, Lima"
                      />
                    </div>

                    <div>
                      <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2">
                        <Phone className="w-4 h-4" />
                        Teléfono
                      </label>
                      <input
                        type="tel"
                        name="telefono"
                        value={datosCliente.telefono}
                        onChange={handleClienteChange}
                        className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                        placeholder="Ej: 987654321"
                      />
                    </div>

                    <div>
                      <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2">
                        <Mail className="w-4 h-4" />
                        Email
                      </label>
                      <input
                        type="email"
                        name="email"
                        value={datosCliente.email}
                        onChange={handleClienteChange}
                        className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                        placeholder="cliente@empresa.com"
                      />
                    </div>
                  </div>

                  {/* Botón guardar cliente */}
                  <button
                    onClick={guardarCliente}
                    disabled={guardandoCliente || !datosCliente.nombre || !datosCliente.ruc}
                    className="w-full bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 disabled:from-gray-800 disabled:to-gray-700 disabled:cursor-not-allowed text-black px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-xl border-2 border-yellow-400 transition-all duration-300 hover:scale-105"
                  >
                    {guardandoCliente ? (
                      <>
                        <Loader className="w-5 h-5 animate-spin" />
                        Guardando...
                      </>
                    ) : (
                      <>
                        <Save className="w-5 h-5" />
                        {clienteSeleccionadoId ? 'Actualizar Cliente' : 'Guardar Cliente'}
                      </>
                    )}
                  </button>
                </div>

                {/* CONFIGURACIÓN ESPECÍFICA POR TIPO */}
                {esProyecto && (
                  <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-blue-700 shadow-xl">
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
                  </div>
                )}

                {esInforme && (
                  <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-green-700 shadow-xl">
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
                          <option value="general">📋 Informe General</option>
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
                  </div>
                )}

                {/* SERVICIO E INDUSTRIA */}
                <div className={`bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-${colores.border} shadow-xl`}>
                  <h2 className={`text-2xl font-bold mb-4 text-${colores.primary}-400`}>⚙️ Tipo de Servicio</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {servicios.map(servicio => (
                      <button
                        key={servicio.id}
                        onClick={() => setServicioSeleccionado(servicio.id)}
                        className={`p-4 rounded-xl border-2 transition-all duration-300 text-left ${servicioSeleccionado === servicio.id
                          ? 'border-yellow-500 bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl scale-105'
                          : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800'
                          }`}>
                        <div className="text-2xl mb-2">{servicio.icon}</div>
                        <div className="text-sm font-semibold">{servicio.nombre.split(' ').slice(1).join(' ')}</div>
                      </button>
                    ))}
                  </div>
                </div>

                <div className={`bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-${colores.border} shadow-xl`}>
                  <h2 className={`text-2xl font-bold mb-4 text-${colores.primary}-400`}>🏢 Industria</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {industrias.map(industria => (
                      <button
                        key={industria.id}
                        onClick={() => setIndustriaSeleccionada(industria.id)}
                        className={`p-3 rounded-xl border-2 transition-all duration-300 ${industriaSeleccionada === industria.id
                          ? 'border-yellow-500 bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl'
                          : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800'
                          }`}>
                        <div className="text-sm font-semibold">{industria.nombre}</div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* DESCRIPCIÓN */}
                <div className={`bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-${colores.border} shadow-xl`}>
                  <h2 className={`text-2xl font-bold mb-4 text-${colores.primary}-400`}>📝 Descripción Detallada</h2>

                  {esCotizacion && servicioSeleccionado && basePreciosUniversal[servicioSeleccionado] && (
                    <div className="mb-4 p-4 bg-blue-950 bg-opacity-50 border border-blue-700 rounded-xl">
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
                    <h3 className="text-lg font-semibold mb-3 text-gray-300">Documentos (Opcional)</h3>
                    <div className="border-2 border-dashed border-gray-700 rounded-xl p-6 text-center hover:border-yellow-600 transition-all cursor-pointer mb-4 bg-gray-950 bg-opacity-50">
                      <input type="file" multiple onChange={handleFileUpload} className="hidden" id="fileInput" accept=".pdf,.png,.jpg,.jpeg,.gif,.webp,.xlsx,.xls,.docx,.doc,.html,.json,.txt,.csv" />
                      <label htmlFor="fileInput" className="cursor-pointer">
                        <Upload className="w-12 h-12 mx-auto mb-3 text-yellow-500" />
                        <p className="text-sm text-gray-400 font-semibold">Sube documentos (máx 10MB)</p>
                      </label>
                    </div>

                    {archivos.length > 0 && (
                      <div className="space-y-2">
                        <p className="text-sm font-semibold text-yellow-400 mb-2">📁 Archivos:</p>
                        {archivos.map((archivo, index) => (
                          <div key={index} className="flex items-center justify-between bg-gray-950 bg-opacity-70 p-3 rounded-xl border border-gray-800">
                            <div className="flex items-center gap-2">
                              <FileText className="w-5 h-5 text-yellow-500" />
                              <span className="text-sm font-semibold">{archivo.nombre}</span>
                            </div>
                            <button
                              onClick={() => setArchivos(prev => prev.filter((_, i) => i !== index))}
                              className="text-red-400 hover:text-red-300">
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
                  className="w-full bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 disabled:from-gray-800 disabled:to-gray-700 disabled:cursor-not-allowed py-4 rounded-xl font-bold text-lg text-black shadow-2xl border-2 border-yellow-400 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-3">
                  <MessageSquare className="w-6 h-6" />
                  Comenzar Chat con Vista Previa
                </button>
              </div>
            )}

            {/* PASO 2: CHAT + VISTA PREVIA SPLIT-SCREEN */}
            {paso === 2 && (
              <div className="max-w-full mx-auto h-[calc(100vh-200px)]">
                <div className="grid grid-cols-12 h-full gap-4">

                  {/* CHAT (IZQUIERDA) */}
                  <div className="col-span-6 bg-white rounded-2xl shadow-xl flex flex-col">
                    <div className="bg-gradient-to-r from-yellow-600 to-yellow-500 p-4 rounded-t-2xl">
                      <h3 className="text-xl font-bold text-black flex items-center gap-2">
                        <div className="bg-white p-1 rounded-full">
                          <PiliAvatar size={24} showCrown={true} />
                        </div>
                        👑 PILI - {servicios.find(s => s.id === servicioSeleccionado)?.nombre}
                      </h3>
                    </div>

                    {/* CONVERSACIÓN */}
                    <div ref={chatContainerRef} className="flex-grow bg-gray-100 p-4 overflow-y-auto">
                      {conversacion.length === 0 ? (
                        <div className="text-center text-gray-600 mt-8">
                          <div className="inline-block bg-yellow-600 p-3 rounded-full mb-3">
                            <PiliAvatar size={32} showCrown={true} />
                          </div>
                          <p className="font-semibold text-lg">¡Hola! Soy 👑 PILI - Tu Asistente IA</p>
                          <p className="text-xs text-gray-500 mb-2">Procesadora Inteligente de Licitaciones Industriales v3.0</p>
                          <p className="text-sm mt-1">
                            {esCotizacion && "Empezemos con tu cotización..."}
                            {esProyecto && "Vamos a planificar tu proyecto..."}
                            {esInforme && "Generemos tu informe profesional..."}
                          </p>
                        </div>
                      ) : (
                        <div className="space-y-3">
                          {conversacion.map((mensaje, index) => (
                            <div key={index} className={`flex ${mensaje.tipo === 'usuario' ? 'justify-end' : 'justify-start'}`}>
                              <div className={`max-w-[85%] p-3 rounded-2xl ${mensaje.tipo === 'usuario'
                                ? 'bg-yellow-600 text-black'
                                : 'bg-white border-2 border-gray-300 text-gray-800'
                                }`}>
                                <p className="text-sm">{mensaje.mensaje}</p>
                              </div>
                            </div>
                          ))}

                          {analizando && (
                            <div className="flex justify-start">
                              <div className="bg-white border-2 border-gray-300 p-3 rounded-2xl">
                                <div className="flex items-center gap-2 text-gray-600">
                                  <div className="bg-yellow-600 p-1 rounded-full animate-pulse">
                                    <PiliAvatar size={16} showCrown={true} />
                                  </div>
                                  <Loader className="w-4 h-4 animate-spin text-yellow-600" />
                                  <span className="text-sm font-medium">PILI está pensando... 🤔</span>
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    {/* BOTONES CONTEXTUALES */}
                    {botonesContextuales.length > 0 && (
                      <div className="px-4 py-2 bg-gray-50 border-t">
                        <div className="flex flex-wrap gap-2">
                          {botonesContextuales.map((boton, index) => (
                            <button
                              key={index}
                              onClick={() => enviarRespuestaRapida(boton)}
                              className="px-3 py-1 bg-yellow-100 hover:bg-yellow-200 text-gray-800 rounded-lg text-xs border border-yellow-300 transition-all">
                              {boton}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* INPUT CHAT */}
                    <div className="p-4 bg-white border-t rounded-b-2xl">
                      <div className="flex gap-2">
                        <input
                          type="text"
                          value={inputChat}
                          onChange={(e) => setInputChat(e.target.value)}
                          onKeyPress={(e) => e.key === 'Enter' && !analizando && handleEnviarMensajeChat()}
                          placeholder="Escribe aquí..."
                          className="flex-grow p-2 border-2 border-gray-300 rounded-xl focus:border-yellow-500 focus:outline-none text-gray-800"
                          disabled={analizando}
                        />
                        <button
                          onClick={handleEnviarMensajeChat}
                          disabled={analizando || !inputChat.trim()}
                          className="p-2 bg-yellow-600 hover:bg-yellow-500 disabled:bg-gray-400 text-black rounded-xl transition-all">
                          <Send className="w-5 h-5" />
                        </button>
                      </div>

                      <div className="flex justify-between items-center mt-3">
                        <button
                          onClick={() => setPaso(1)}
                          className="px-3 py-1 bg-gray-300 hover:bg-gray-400 text-gray-800 rounded-lg text-sm">
                          ← Configuración
                        </button>
                        <button
                          onClick={() => setPaso(3)}
                          disabled={!mostrarPreview}
                          className="px-4 py-1 bg-green-600 hover:bg-green-500 disabled:bg-gray-400 text-white font-bold rounded-lg text-sm">
                          Finalizar →
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* VISTA PREVIA (DERECHA) */}
                  <div className="col-span-6 bg-white rounded-2xl shadow-xl flex flex-col">
                    <div className="bg-gradient-to-r from-blue-600 to-blue-500 p-4 rounded-t-2xl flex justify-between items-center">
                      <div className="flex items-center gap-2">
                        <Eye className="w-6 h-6 text-white" />
                        <h3 className="text-xl font-bold text-white">Vista Previa</h3>
                      </div>

                      {mostrarPreview && (
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => setModoEdicion(!modoEdicion)}
                            className="px-3 py-1 bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded-lg text-sm flex items-center gap-1">
                            <Edit className="w-4 h-4" />
                            {modoEdicion ? 'Ver' : 'Editar'}
                          </button>

                          {esCotizacion && (
                            <div className="flex gap-2">
                              <button
                                onClick={() => setOcultarIGV(!ocultarIGV)}
                                className="px-2 py-1 bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded text-xs">
                                {ocultarIGV ? 'Mostrar' : 'Ocultar'} IGV
                              </button>
                              <button
                                onClick={() => setOcultarPreciosUnitarios(!ocultarPreciosUnitarios)}
                                className="px-2 py-1 bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded text-xs">
                                P. Unit
                              </button>
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    <div className="flex-grow p-4 overflow-y-auto bg-white">
                      {!mostrarPreview ? (
                        <div className="text-center text-gray-500 mt-20">
                          <Eye className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                          <p className="text-lg">Vista Previa</p>
                          <p className="text-sm">Aparecerá cuando la IA genere contenido</p>
                        </div>
                      ) : (() => {
                        // DEBUG: Ver qué datos tenemos
                        console.log('🔍 DEBUG - cotizacion:', cotizacion);
                        console.log('🔍 DEBUG - cotizacion?.items:', cotizacion?.items);
                        console.log('🔍 DEBUG - datosEditables:', datosEditables);
                        console.log('🔍 DEBUG - datosEditables?.items:', datosEditables?.items);

                        return (cotizacion?.items || datosEditables?.items) ? (
                          /* TABLA EDITABLE INLINE - ALTO CONTRASTE - SIEMPRE VISIBLE */
                          <div className="space-y-4">
                            {/* Encabezado */}
                            <div className="border-b-4 border-red-900 pb-4 mb-4">
                              <h2 className="text-2xl font-bold text-red-900">COTIZACIÓN ELÉCTRICA</h2>
                              <p className="text-gray-700 mt-1">Cliente: {datosEditables.cliente?.nombre || cotizacion?.cliente?.nombre || 'Cliente Demo'}</p>
                            </div>

                            {/* Mensaje de ayuda */}
                            <div className="bg-blue-50 border-2 border-blue-500 rounded-lg p-3 mb-4">
                              <p className="text-sm font-semibold text-blue-900">
                                ✏️ Haz clic en las celdas para editar. Los totales se calculan automáticamente.
                              </p>
                            </div>

                            {/* TABLA EDITABLE */}
                            <div className="overflow-x-auto border-2 border-gray-400 rounded-lg">
                              <table className="w-full border-collapse">
                                <thead>
                                  <tr className="bg-red-900 text-white">
                                    <th className="py-3 px-3 text-left border-r-2 border-red-800 font-bold">DESCRIPCIÓN</th>
                                    <th className="py-3 px-3 text-center border-r-2 border-red-800 font-bold w-24">CANT.</th>
                                    <th className="py-3 px-3 text-center border-r-2 border-red-800 font-bold w-20">UND.</th>
                                    {!ocultarPreciosUnitarios && (
                                      <th className="py-3 px-3 text-right border-r-2 border-red-800 font-bold w-32">P.U. (S/)</th>
                                    )}
                                    <th className="py-3 px-3 text-right border-r-2 border-red-800 font-bold w-32">TOTAL (S/)</th>
                                    <th className="py-3 px-3 text-center font-bold w-16">🗑️</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {datosEditables.items.map((item, index) => {
                                    const subtotalItem = (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || item.precioUnitario || 0));

                                    return (
                                      <tr key={index} className="border-b-2 border-gray-300 hover:bg-gray-50">
                                        {/* Descripción - EDITABLE */}
                                        <td className="py-2 px-2 border-r border-gray-300">
                                          <input
                                            type="text"
                                            value={item.descripcion}
                                            onChange={(e) => actualizarItem(index, 'descripcion', e.target.value)}
                                            className="w-full px-2 py-2 border-2 border-gray-400 rounded focus:border-red-600 focus:outline-none text-gray-900 font-medium bg-white"
                                            style={{ color: '#000000' }}
                                          />
                                        </td>

                                        {/* Cantidad - EDITABLE */}
                                        <td className="py-2 px-2 border-r border-gray-300">
                                          <input
                                            type="number"
                                            step="0.01"
                                            value={item.cantidad}
                                            onChange={(e) => actualizarItem(index, 'cantidad', e.target.value)}
                                            className="w-full px-2 py-2 text-center border-2 border-gray-400 rounded focus:border-red-600 focus:outline-none text-gray-900 font-bold bg-white"
                                            style={{ color: '#000000' }}
                                          />
                                        </td>

                                        {/* Unidad */}
                                        <td className="py-2 px-2 text-center border-r border-gray-300">
                                          <span className="text-gray-900 font-medium">{item.unidad || 'pto'}</span>
                                        </td>

                                        {/* Precio Unitario - EDITABLE */}
                                        {!ocultarPreciosUnitarios && (
                                          <td className="py-2 px-2 border-r border-gray-300">
                                            <input
                                              type="number"
                                              step="0.01"
                                              value={item.precio_unitario || item.precioUnitario || 0}
                                              onChange={(e) => actualizarItem(index, 'precioUnitario', e.target.value)}
                                              className="w-full px-2 py-2 text-right border-2 border-gray-400 rounded focus:border-red-600 focus:outline-none text-gray-900 font-bold bg-white"
                                              style={{ color: '#000000' }}
                                            />
                                          </td>
                                        )}

                                        {/* Total - CALCULADO */}
                                        <td className="py-2 px-2 text-right border-r border-gray-300">
                                          <span className="text-red-900 font-bold text-lg">
                                            S/ {subtotalItem.toFixed(2)}
                                          </span>
                                        </td>

                                        {/* Botón Eliminar */}
                                        <td className="py-2 px-2 text-center">
                                          <button
                                            onClick={() => eliminarItem(index)}
                                            disabled={datosEditables.items.length === 1}
                                            className={`p-2 rounded ${datosEditables.items.length === 1
                                              ? 'text-gray-400 cursor-not-allowed'
                                              : 'text-red-600 hover:bg-red-100'
                                              }`}
                                          >
                                            <Trash2 size={18} />
                                          </button>
                                        </td>
                                      </tr>
                                    );
                                  })}
                                </tbody>
                              </table>
                            </div>

                            {/* Botón Agregar Ítem */}
                            <button
                              onClick={agregarItem}
                              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg font-bold hover:bg-green-700 transition-all"
                            >
                              <Plus size={20} />
                              Agregar Ítem
                            </button>

                            {/* TOTALES */}
                            <div className="bg-gray-100 rounded-lg p-4 border-2 border-gray-400">
                              <div className="flex justify-end">
                                <div className="w-full md:w-1/2 space-y-3">
                                  {!ocultarIGV && (
                                    <>
                                      <div className="flex justify-between text-lg border-b-2 border-gray-400 pb-2">
                                        <span className="font-semibold text-gray-900">Subtotal:</span>
                                        <span className="font-bold text-gray-900">
                                          S/ {calcularTotales(datosEditables.items || []).subtotal}
                                        </span>
                                      </div>
                                      <div className="flex justify-between text-lg border-b-2 border-gray-400 pb-2">
                                        <span className="font-semibold text-gray-900">IGV (18%):</span>
                                        <span className="font-bold text-gray-900">
                                          S/ {calcularTotales(datosEditables.items || []).igv}
                                        </span>
                                      </div>
                                    </>
                                  )}
                                  <div className="flex justify-between bg-gradient-to-r from-red-900 to-red-800 text-yellow-400 p-4 rounded-lg">
                                    <span className="font-black text-2xl">TOTAL:</span>
                                    <span className="font-black text-3xl">
                                      S/ {calcularTotales(datosEditables.items || [])[ocultarIGV ? 'subtotal' : 'total']}
                                    </span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        ) : (
                          /* VISTA PREVIA HTML PARA TODOS LOS DOCUMENTOS */
                          <div
                            ref={previewRef}
                            className="w-full h-full"
                            dangerouslySetInnerHTML={{ __html: htmlPreview }}
                          />
                        );
                      })()}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* PASO 3: FINALIZACIÓN */}
            {paso === 3 && (
              <div className="max-w-5xl mx-auto space-y-6">
                <div className="bg-white rounded-2xl p-8 shadow-xl border-4 border-green-600">
                  <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
                    <CheckCircle className="w-8 h-8 text-green-600" />
                    Documento Listo para Generar
                  </h2>

                  <div className="bg-green-50 p-6 rounded-xl mb-6">
                    <h3 className="text-lg font-bold text-green-800 mb-3">✅ Lo que se incluirá:</h3>
                    <div className="grid grid-cols-2 gap-4 text-sm text-green-700">
                      <div className="space-y-1">
                        <p>• Contenido generado por IA</p>
                        <p>• Datos personalizados</p>
                        <p>• Formato profesional Tesla</p>
                      </div>
                      <div className="space-y-1">
                        {logoBase64 && <p>• Logo de la empresa</p>}
                        <p>• Colores corporativos</p>
                        <p>• Información de contacto</p>
                      </div>
                    </div>
                  </div>

                  {/* VISTA PREVIA CON BOTONES DE GENERACIÓN */}
                  <VistaPrevia
                    cotizacion={cotizacion || proyecto || informe || {}}
                    onGenerarDocumento={handleDescargar}
                    tipoDocumento={tipoFlujo}
                    htmlPreview={htmlPreview}
                  />

                  {/* ✅ PANEL DE PERSONALIZACIÓN */}
                  <div className="mb-6 border-2 border-blue-500 rounded-xl overflow-hidden">
                    {/* Header del Panel */}
                    <button
                      onClick={() => setMostrarPanelPersonalizacion(!mostrarPanelPersonalizacion)}
                      className="w-full bg-gradient-to-r from-blue-600 to-blue-500 p-4 flex items-center justify-between hover:from-blue-700 hover:to-blue-600 transition-all">
                      <div className="flex items-center gap-3">
                        <Settings className="w-6 h-6 text-white" />
                        <h3 className="text-lg font-bold text-white">Personalización del Documento</h3>
                      </div>
                      {mostrarPanelPersonalizacion ? (
                        <ChevronUp className="w-5 h-5 text-white" />
                      ) : (
                        <ChevronDown className="w-5 h-5 text-white" />
                      )}
                    </button>

                    {/* Contenido del Panel (Colapsable) */}
                    {mostrarPanelPersonalizacion && (
                      <div className="bg-gray-900 p-6 space-y-6">
                        {/* Sección: Esquema de Colores */}
                        <div>
                          <label className="block text-blue-400 font-semibold mb-3 flex items-center gap-2">
                            <PieChart className="w-5 h-5" />
                            Esquema de Colores
                          </label>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                            <button
                              onClick={() => setEsquemaColores('azul-tesla')}
                              className={`p-3 rounded-lg border-2 transition-all ${esquemaColores === 'azul-tesla'
                                ? 'border-blue-500 bg-blue-900 text-white'
                                : 'border-gray-700 bg-gray-800 text-gray-300 hover:border-blue-600'
                                }`}>
                              <div className="flex items-center gap-2 mb-1">
                                <div className="w-4 h-4 rounded-full bg-blue-500"></div>
                                <span className="font-semibold">Azul Tesla</span>
                              </div>
                              <span className="text-xs">Corporativo</span>
                            </button>
                            <button
                              onClick={() => setEsquemaColores('rojo-energia')}
                              className={`p-3 rounded-lg border-2 transition-all ${esquemaColores === 'rojo-energia'
                                ? 'border-red-500 bg-red-900 text-white'
                                : 'border-gray-700 bg-gray-800 text-gray-300 hover:border-red-600'
                                }`}>
                              <div className="flex items-center gap-2 mb-1">
                                <div className="w-4 h-4 rounded-full bg-red-500"></div>
                                <span className="font-semibold">Rojo Energía</span>
                              </div>
                              <span className="text-xs">Vibrante</span>
                            </button>
                            <button
                              onClick={() => setEsquemaColores('verde-ecologico')}
                              className={`p-3 rounded-lg border-2 transition-all ${esquemaColores === 'verde-ecologico'
                                ? 'border-green-500 bg-green-900 text-white'
                                : 'border-gray-700 bg-gray-800 text-gray-300 hover:border-green-600'
                                }`}>
                              <div className="flex items-center gap-2 mb-1">
                                <div className="w-4 h-4 rounded-full bg-green-500"></div>
                                <span className="font-semibold">Verde Eco</span>
                              </div>
                              <span className="text-xs">Sostenible</span>
                            </button>
                            <button
                              onClick={() => setEsquemaColores('personalizado')}
                              className={`p-3 rounded-lg border-2 transition-all ${esquemaColores === 'personalizado'
                                ? 'border-purple-500 bg-purple-900 text-white'
                                : 'border-gray-700 bg-gray-800 text-gray-300 hover:border-purple-600'
                                }`}>
                              <div className="flex items-center gap-2 mb-1">
                                <div className="w-4 h-4 rounded-full bg-gradient-to-r from-purple-500 to-pink-500"></div>
                                <span className="font-semibold">Personalizado</span>
                              </div>
                              <span className="text-xs">A medida</span>
                            </button>
                          </div>
                        </div>

                        {/* Sección: Fuente */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div>
                            <label className="block text-blue-400 font-semibold mb-3">Fuente del Documento</label>
                            <select
                              value={fuenteDocumento}
                              onChange={(e) => setFuenteDocumento(e.target.value)}
                              className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors">
                              <option value="Calibri">Calibri (Recomendada)</option>
                              <option value="Arial">Arial</option>
                              <option value="Times New Roman">Times New Roman</option>
                            </select>
                          </div>

                          <div>
                            <label className="block text-blue-400 font-semibold mb-3">Tamaño de Fuente</label>
                            <select
                              value={tamañoFuente}
                              onChange={(e) => setTamañoFuente(Number(e.target.value))}
                              className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors">
                              <option value={10}>10 pt (Pequeña)</option>
                              <option value={11}>11 pt (Normal)</option>
                              <option value={12}>12 pt (Grande)</option>
                            </select>
                          </div>
                        </div>

                        {/* Sección: Logo */}
                        <div>
                          <label className="block text-blue-400 font-semibold mb-3 flex items-center gap-2">
                            <Upload className="w-5 h-5" />
                            Logo de la Empresa
                          </label>
                          <div className="flex items-center gap-4">
                            <button
                              onClick={() => setMostrarLogo(!mostrarLogo)}
                              className={`px-4 py-2 rounded-lg font-semibold transition-all ${mostrarLogo
                                ? 'bg-green-600 text-white'
                                : 'bg-gray-700 text-gray-300'
                                }`}>
                              {mostrarLogo ? '✓ Mostrar Logo' : '✕ Ocultar Logo'}
                            </button>
                            <input
                              ref={fileInputLogoRef}
                              type="file"
                              accept="image/*"
                              onChange={cargarLogo}
                              className="hidden"
                            />
                            <button
                              onClick={() => fileInputLogoRef.current?.click()}
                              className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-500 transition-all flex items-center gap-2">
                              <Upload className="w-4 h-4" />
                              {logoBase64 ? 'Cambiar Logo' : 'Subir Logo'}
                            </button>
                            {logoBase64 && (
                              <span className="text-green-400 text-sm">✓ Logo cargado</span>
                            )}
                          </div>
                        </div>

                        {/* Sección: Opciones de Visualización */}
                        <div>
                          <label className="block text-blue-400 font-semibold mb-3">Opciones de Visualización</label>
                          <div className="flex flex-wrap gap-4">
                            <button
                              onClick={() => setOcultarIGV(!ocultarIGV)}
                              className={`px-4 py-2 rounded-lg font-semibold transition-all ${ocultarIGV
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-700 text-gray-300'
                                }`}>
                              {ocultarIGV ? '✓ IGV Oculto' : 'Mostrar IGV'}
                            </button>
                            <button
                              onClick={() => setOcultarPreciosUnitarios(!ocultarPreciosUnitarios)}
                              className={`px-4 py-2 rounded-lg font-semibold transition-all ${ocultarPreciosUnitarios
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-700 text-gray-300'
                                }`}>
                              {ocultarPreciosUnitarios ? '✓ P. Unit. Ocultos' : 'Mostrar P. Unitarios'}
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* BOTONES DE ACCIÓN */}
                  <div className="flex gap-4">
                    <button
                      onClick={() => setPaso(2)}
                      className="px-6 py-3 bg-gray-600 hover:bg-gray-500 text-white rounded-xl transition-all">
                      ← Volver al Chat
                    </button>

                    <div className="flex-1 flex gap-4">
                      <button
                        onClick={() => handleDescargar('pdf')}
                        disabled={descargando === 'pdf'}
                        className="flex-1 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 disabled:from-gray-600 disabled:to-gray-500 text-white py-3 rounded-xl font-bold transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2">
                        {descargando === 'pdf' ? (
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
                        onClick={() => handleDescargar('word')}
                        disabled={descargando === 'word'}
                        className="flex-1 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 disabled:from-gray-600 disabled:to-gray-500 text-white py-3 rounded-xl font-bold transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2">
                        {descargando === 'word' ? (
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
              </div>
            )}
          </div>
        </div>
      </div >
    );
  }

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