/*
 * ===========================================
 * App.jsx (Versión Fusionada)
 * ===========================================
 * CONSERVA: Tu menú de 3 servicios (6 flujos).
 * AÑADE: La lógica de Chat, Upload y Edición del Artefacto.
 * CONECTA: Al backend real de FastAPI (http://localhost:8000).
 * ===========================================
 */
import React, { useState, useRef, useEffect } from 'react';
import { 
  Upload, MessageSquare, FileText, Download, Zap, Send, Loader, Edit, Save, 
  AlertCircle, CheckCircle, X, RefreshCw, Home, FolderOpen, Eye, EyeOff, 
  Folder, Users, TrendingUp, Clock, BarChart3, FileCheck, Briefcase, 
  ChevronDown, ChevronUp, Layout, Layers, BookOpen, UserPlus, HardDrive 
} from 'lucide-react';

// Importamos la API REAL que creamos
import { api } from './services/api'; 

const CotizadorTesla30 = () => {
  // === ESTADOS PRINCIPALES ===
  const [pantallaActual, setPantallaActual] = useState('inicio'); // inicio, flujo, admin
  const [tipoFlujo, setTipoFlujo] = useState(null); // 'cotizacion-simple', 'cotizacion-compleja', 'informe-simple', etc.
  
  // Estados de menús expandibles
  const [menuCotizaciones, setMenuCotizaciones] = useState(false);
  const [menuProyectos, setMenuProyectos] = useState(false);
  const [menuInformes, setMenuInformes] = useState(false);
  
  // === ESTADOS DEL FLUJO (Migrados del Artefacto) ===
  const [paso, setPaso] = useState(1); // 1: Config, 2: Chat, 3: Edición
  const [archivos, setArchivos] = useState([]); // Archivos subidos
  const [conversacion, setConversacion] = useState([]); // Historial del chat
  const [contextoUsuario, setContextoUsuario] = useState(''); // Textarea de descripción inicial
  const [inputChat, setInputChat] = useState('');
  const [analizando, setAnalizando] = useState(false); // Para mostrar loaders
  const [cotizacion, setCotizacion] = useState(null); // El objeto JSON de la cotización
  const [modoEdicion, setModoEdicion] = useState(true);
  
  // === NUEVOS ESTADOS (Para Clientes y Carpetas) ===
  const [nombreCliente, setNombreCliente] = useState('');
  const [clienteId, setClienteId] = useState(null);
  
  // Estados de UI (Descargas, Errores)
  const [error, setError] = useState('');
  const [exito, setExito] = useState('');
  const [descargando, setDescargando] = useState(null); // 'word', 'pdf'
  
  const fileInputRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Simulación de datos de empresa (puedes moverlos a un estado si es necesario)
  const datosEmpresa = {
    nombre: "TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.",
    ruc: "20601138787",
    telefono: "+51 987 654 321",
    email: "proyectos@tesla-autom.com",
    direccion: "Av. Principal 123, Lima, Perú",
  };

  // === EFECTOS ===
  useEffect(() => {
    // Scroll automático al final del chat
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [conversacion]);

  // === LÓGICA DE NAVEGACIÓN ===
  
  const seleccionarFlujo = (flujo) => {
    setTipoFlujo(flujo);
    setPantallaActual('flujo');
    setPaso(1); // Inicia en el Paso 1: Configuración
    
    // Reseteamos todo
    setArchivos([]);
    setConversacion([]);
    setContextoUsuario('');
    setCotizacion(null);
    setNombreCliente('');
    setClienteId(null);
    setError('');
    setExito('');
  };

  const volverAInicio = () => {
    setPantallaActual('inicio');
    setTipoFlujo(null);
  };

  // === LÓGICA DEL FLUJO (Migrada del Artefacto y CONECTADA) ===

  /**
   * PASO 1: Iniciar el flujo de chat
   */
  const handleIniciarChat = async () => {
    if (!contextoUsuario && archivos.length === 0) {
      setError('Por favor, añade una descripción o sube al menos un archivo.');
      return;
    }
    
    // Validar nombre del cliente
    if (!nombreCliente) {
      setError('Por favor, ingresa el nombre del Cliente o Proyecto para crear su carpeta.');
      return;
    }
    
    setAnalizando(true);
    setError('');
    
    // Mensaje inicial del sistema
    setConversacion([{ 
      role: 'system', 
      content: `Iniciando ${tipoFlujo}. Cliente: ${nombreCliente}. Archivos subidos: ${archivos.length}` 
    }]);

    try {
      // 1. Crear (o encontrar) el cliente en el backend
      // ESTE ES EL NUEVO PASO PARA CREAR CARPETAS
      const clienteData = await api.clientes.crearOEncontrar({ nombre: nombreCliente });
      setClienteId(clienteData.id);
      console.log(`Cliente procesado. ID: ${clienteData.id}, Carpeta: ${clienteData.carpeta_storage}`);

      // 2. Subir archivos iniciales (si los hay)
      const promesasUpload = archivos.map(file => 
        api.documentos.upload(file, clienteId, null) // Sube asociado al cliente
      );
      const resultadosUpload = await Promise.all(promesasUpload);
      
      const textosExtraidos = resultadosUpload.map(res => res.texto_extraido).filter(Boolean);
      
      // 3. Enviar primer mensaje a la IA
      const primerMensaje = `
        Iniciando un nuevo flujo de: ${tipoFlujo}.
        Cliente: ${nombreCliente} (ID: ${clienteId}).
        
        Descripción inicial del usuario:
        "${contextoUsuario}"
        
        Textos extraídos de ${textosExtraidos.length} archivos subidos:
        ${textosExtraidos.join('\n---\n')}
        
        Por favor, actúa como mi asistente experto de ${tipoFlujo}. 
        Analiza la información, hazme preguntas si es necesario, o genera la primera propuesta.
      `;
      
      // Añadir mensaje de usuario al chat
      setConversacion(prev => [...prev, { role: 'user', content: contextoUsuario || "Archivos subidos para análisis." }]);
      
      // Llamar al backend
      await enviarMensajeAlBackend(primerMensaje, clienteId);

      setPaso(2); // Mover al Paso 2: Chat
      
    } catch (err) {
      setError(`Error al iniciar el chat: ${err.message}`);
    } finally {
      setAnalizando(false);
    }
  };

  /**
   * PASO 2: Enviar mensaje en el chat
   */
  const handleEnviarMensajeChat = async () => {
    if (!inputChat.trim()) return;

    const mensajeUsuario = inputChat;
    setConversacion(prev => [...prev, { role: 'user', content: mensajeUsuario }]);
    setInputChat('');
    setAnalizando(true);

    await enviarMensajeAlBackend(mensajeUsuario, clienteId);
    
    setAnalizando(false);
  };

  /**
   * FUNCIÓN CENTRAL DE IA (reutilizable)
   */
  const enviarMensajeAlBackend = async (mensaje, cliente_id, historial = null) => {
    try {
      const historialChat = historial || conversacion;
      
      const res = await api.chat.enviarMensaje({
        mensaje: mensaje,
        historial_chat: historialChat,
        tipo_flujo: tipoFlujo,
        cliente_id: cliente_id
      });

      // Añadir respuesta de la IA
      setConversacion(prev => [...prev, { role: 'ia', content: res.respuesta_ia }]);

      // ¡CRÍTICO! Si la IA genera la cotización, la ponemos en estado
      if (res.cotizacion_generada) {
        console.log("¡Cotización generada por la IA!", res.cotizacion_generada);
        setCotizacion(res.cotizacion_generada);
        setPaso(3); // Mover automáticamente al Paso 3: Edición
        setExito('¡Propuesta generada! Puedes revisarla y editarla.');
      }
      
    } catch (err) {
      setError(`Error al comunicarse con la IA: ${err.message}`);
      setConversacion(prev => [...prev, { role: 'system', content: `Error: ${err.message}` }]);
    }
  };


  /**
   * Lógica de UPLOAD (del Artefacto)
   * Esta función solo añade archivos al estado local 'archivos'.
   * El upload real ocurre en handleIniciarChat.
   */
  const handleFileChange = (e) => {
    if (e.target.files) {
      const nuevosArchivos = Array.from(e.target.files);
      setArchivos(prev => [...prev, ...nuevosArchivos]);
      setError('');
    }
  };

  const eliminarArchivo = (index) => {
    setArchivos(prev => prev.filter((_, i) => i !== index));
  };


  // === PASO 3: LÓGICA DE EDICIÓN (Migrada del Artefacto) ===

  const handleEditarItem = (capIndex, itemIndex, campo, valor) => {
    setCotizacion(prev => {
      const nuevaCot = JSON.parse(JSON.stringify(prev)); // Copia profunda
      
      let item;
      if (capIndex === null) {
        item = nuevaCot.items[itemIndex];
      } else {
        item = nuevaCot.capitulos[capIndex].items[itemIndex];
      }

      // Actualizar valor
      item[campo] = valor;

      // Recalcular si es numérico
      if (campo === 'cantidad' || campo === 'precio_unitario') {
        const cantidad = parseFloat(item.cantidad) || 0;
        const precio = parseFloat(item.precio_unitario) || 0;
        item.total = (cantidad * precio).toFixed(2);
      }
      
      return recalcularTotales(nuevaCot);
    });
  };

  const recalcularTotales = (cot) => {
    let subtotal = 0;
    
    if (cot.capitulos && cot.capitulos.length > 0) {
      cot.capitulos.forEach(cap => {
        cap.items.forEach(item => {
          subtotal += parseFloat(item.total) || 0;
        });
      });
    } else {
      cot.items.forEach(item => {
        subtotal += parseFloat(item.total) || 0;
      });
    }

    cot.subtotal = subtotal.toFixed(2);
    cot.igv = (subtotal * 0.18).toFixed(2);
    cot.total = (subtotal * 1.18).toFixed(2);
    
    return cot;
  };
  
  const handleAgregarItem = (capIndex = null) => {
    const nuevoItem = {
      descripcion: "Nuevo Item",
      cantidad: 1,
      unidad: "und",
      precio_unitario: 0.0,
      total: 0.0,
    };
    
    setCotizacion(prev => {
      const nuevaCot = JSON.parse(JSON.stringify(prev));
      if (capIndex !== null) {
        nuevaCot.capitulos[capIndex].items.push(nuevoItem);
      } else {
        if (!nuevaCot.items) nuevaCot.items = [];
        nuevaCot.items.push(nuevoItem);
      }
      return nuevaCot;
    });
  };
  
  const handleEliminarItem = (capIndex, itemIndex) => {
     setCotizacion(prev => {
      const nuevaCot = JSON.parse(JSON.stringify(prev));
      if (capIndex !== null) {
        nuevaCot.capitulos[capIndex].items.splice(itemIndex, 1);
      } else {
        nuevaCot.items.splice(itemIndex, 1);
      }
      return recalcularTotales(nuevaCot);
    });
  };

  // === LÓGICA DE DESCARGA (¡CORREGIDA!) ===

  /**
   * Esta es la función rota de App.jsx, ahora CORREGIDA.
   * Guarda en la BD primero, luego descarga.
   */
  const handleDescargar = async (formato) => {
    if (!cotizacion) {
      setError('No hay cotización generada para descargar.');
      return;
    }

    setDescargando(formato);
    setError('');
    setExito('');

    try {
      let cotizacionAGuardar = { ...cotizacion };
      
      // 1. Verificar si la cotización ya existe en la BD (tiene ID)
      let cotizacionId = cotizacion.id;

      if (!cotizacionId) {
        // 2. Si NO tiene ID, la CREAMOS en la BD
        console.log("Guardando nueva cotización en la BD...");
        
        // Preparamos el payload para el backend
        const payload = {
          cliente: cotizacion.cliente || nombreCliente,
          proyecto: cotizacion.proyecto || "N/A",
          descripcion: cotizacion.descripcion || "N/A",
          items: cotizacion.items || (cotizacion.capitulos ? cotizacion.capitulos.flatMap(c => c.items) : []),
          subtotal: parseFloat(cotizacion.subtotal),
          igv: parseFloat(cotizacion.igv),
          total: parseFloat(cotizacion.total),
          observaciones: cotizacion.observaciones || "",
          vigencia: cotizacion.vigencia || "30 días",
          estado: "borrador",
          cliente_id: clienteId,
          // Añadir capítulos si existen
          metadata_adicional: cotizacion.capitulos ? { capitulos: cotizacion.capitulos } : {}
        };

        const cotizacionGuardada = await api.cotizaciones.crear(payload);
        cotizacionId = cotizacionGuardada.id;
        
        // Actualizamos el estado local
        setCotizacion(cotizacionGuardada);
        console.log(`Cotización guardada con ID: ${cotizacionId}`);
        
      } else {
        // 3. Si YA tiene ID, la ACTUALIZAMOS (opcional, por si hubo cambios)
        console.log(`Actualizando cotización ID: ${cotizacionId}`);
        // (Aquí iría la lógica de api.cotizaciones.actualizar(cotizacionId, payload))
      }
      
      // 4. Ahora que SÍ tenemos un ID, generamos el documento
      console.log(`Generando ${formato} para cotización ID: ${cotizacionId}`);
      
      let resultado;
      if (formato === 'word') {
        resultado = await api.cotizaciones.generarWord(cotizacionId, {}); // {} = opciones
      } else {
        resultado = await api.cotizaciones.generarPDF(cotizacionId, {}); // {} = opciones
      }

      if (resultado.success) {
        setExito(`✅ Documento ${formato.toUpperCase()} generado exitosamente.`);
      } else {
        setError(resultado.message || `Error al generar ${formato}`);
      }
      
    } catch (err) {
      console.error('Error en el flujo de descarga:', err);
      setError(`Error fatal: ${err.message}`);
    } finally {
      setDescargando(null);
    }
  };


  // === RENDERIZACIÓN ===

  const renderIconoFlujo = (flujo) => {
    if (flujo.includes('cotizacion')) return <BarChart3 className="w-8 h-8" />;
    if (flujo.includes('informe')) return <FileText className="w-8 h-8" />;
    if (flujo.includes('proyecto')) return <Briefcase className="w-8 h-8" />;
    return <FileCheck className="w-8 h-8" />;
  };

  /**
   * Pantalla de Inicio (Tu Menú de 3 Servicios)
   */
  const renderInicio = () => (
    <div className="max-w-6xl mx-auto p-8">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-black text-red-900">TESLA COTIZADOR v3.0</h1>
        <p className="text-xl text-gray-600 mt-2">Tu asistente inteligente para la generación de documentos</p>
      </div>
      
      <div className="grid md:grid-cols-3 gap-8">
        
        {/* Columna Cotizaciones */}
        <div className="bg-white p-6 rounded-2xl shadow-xl border-t-8 border-red-800">
          <div className="flex items-center text-red-800 mb-4">
            <Layers className="w-10 h-10 mr-3" />
            <h2 className="text-3xl font-bold">Cotizaciones</h2>
          </div>
          <p className="text-gray-600 mb-6">Genera cotizaciones profesionales, desde simples hasta complejas, con análisis de IA.</p>
          <button onClick={() => seleccionarFlujo('cotizacion-simple')} className="w-full text-left p-4 mb-3 bg-gray-100 hover:bg-red-100 rounded-lg flex items-center gap-3 transition-all">
            <Zap className="w-5 h-5 text-yellow-500" />
            <div>
              <span className="font-semibold">Cotización Simple</span>
              <p className="text-sm text-gray-500">Basada en descripción de texto.</p>
            </div>
          </button>
          <button onClick={() => seleccionarFlujo('cotizacion-compleja')} className="w-full text-left p-4 bg-gray-100 hover:bg-red-100 rounded-lg flex items-center gap-3 transition-all">
            <Upload className="w-5 h-5 text-red-700" />
            <div>
              <span className="font-semibold">Cotización Compleja</span>
              <p className="text-sm text-gray-500">Sube archivos (PDF, DOCX, XLSX).</p>
            </div>
          </button>
        </div>

        {/* Columna Informes */}
        <div className="bg-white p-6 rounded-2xl shadow-xl border-t-8 border-blue-800">
          <div className="flex items-center text-blue-800 mb-4">
            <BookOpen className="w-10 h-10 mr-3" />
            <h2 className="text-3xl font-bold">Informes</h2>
          </div>
          <p className="text-gray-600 mb-6">Crea informes ejecutivos, técnicos o de avance con formato profesional y análisis de datos.</p>
          <button onClick={() => seleccionarFlujo('informe-simple')} className="w-full text-left p-4 mb-3 bg-gray-100 hover:bg-blue-100 rounded-lg flex items-center gap-3 transition-all">
            <FileText className="w-5 h-5 text-blue-500" />
            <div>
              <span className="font-semibold">Informe Simple</span>
              <p className="text-sm text-gray-500">PDF estándar basado en texto.</p>
            </div>
          </button>
          <button onClick={() => seleccionarFlujo('informe-complejo')} className="w-full text-left p-4 bg-gray-100 hover:bg-blue-100 rounded-lg flex items-center gap-3 transition-all">
            <TrendingUp className="w-5 h-5 text-blue-700" />
            <div>
              <span className="font-semibold">Informe Ejecutivo</span>
              <p className="text-sm text-gray-500">Sube datos, genera gráficos y formato APA.</p>
            </div>
          </button>
        </div>
        
        {/* Columna Proyectos */}
        <div className="bg-white p-6 rounded-2xl shadow-xl border-t-8 border-gray-800">
          <div className="flex items-center text-gray-800 mb-4">
            <Briefcase className="w-10 h-10 mr-3" />
            <h2 className="text-3xl font-bold">Proyectos</h2>
          </div>
          <p className="text-gray-600 mb-6">Gestiona proyectos, crea carpetas de cliente y genera reportes de estado y cronogramas.</p>
          <button onClick={() => seleccionarFlujo('proyecto-simple')} className="w-full text-left p-4 mb-3 bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center gap-3 transition-all">
            <Folder className="w-5 h-5 text-gray-500" />
            <div>
              <span className="font-semibold">Proyecto Simple</span>
              <p className="text-sm text-gray-500">Gestión básica y estadísticas.</p>
            </div>
          </button>
          <button onClick={() => seleccionarFlujo('proyecto-complejo')} className="w-full text-left p-4 bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center gap-3 transition-all">
            <HardDrive className="w-5 h-5 text-gray-700" />
            <div>
              <span className="font-semibold">Proyecto Complejo</span>
              <p className="text-sm text-gray-500">Gestión de carpetas, RAG y Gantt.</p>
            </div>
          </button>
        </div>

      </div>
    </div>
  );

  /**
   * Pantalla del Flujo (Pasos 1, 2, 3)
   */
  const renderFlujo = () => (
    <div className="max-w-7xl mx-auto p-8">
      {/* Encabezado del Flujo */}
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center gap-4">
          <span className="p-3 bg-red-100 text-red-800 rounded-xl">
            {renderIconoFlujo(tipoFlujo)}
          </span>
          <div>
            <h1 className="text-3xl font-bold text-red-900 capitalize">
              {tipoFlujo.replace('-', ' ')}
            </h1>
            <p className="text-gray-500">Sigue los pasos para generar tu documento.</p>
          </div>
        </div>
        <button 
          onClick={volverAInicio}
          className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded-lg flex items-center gap-2"
        >
          <Home className="w-4 h-4" /> Volver al Inicio
        </button>
      </div>

      {/* Indicador de Pasos */}
      <div className="flex justify-between items-center w-full max-w-2xl mx-auto my-12">
        {['Configurar', 'Chatear', 'Editar'].map((label, i) => (
          <React.Fragment key={i}>
            <div className="flex flex-col items-center">
              <div 
                className={`w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold ${
                  paso > i+1 ? 'bg-red-800 text-white' : 
                  paso === i+1 ? 'bg-red-600 text-white' : 
                  'bg-gray-200 text-gray-500'
                }`}
              >
                {paso > i+1 ? <CheckCircle /> : i+1}
              </div>
              <span className={`mt-2 font-semibold ${paso >= i+1 ? 'text-red-800' : 'text-gray-500'}`}>{label}</span>
            </div>
            {i < 2 && <div className={`flex-1 h-1 mx-4 ${paso > i+1 ? 'bg-red-800' : 'bg-gray-200'}`}></div>}
          </React.Fragment>
        ))}
      </div>

      {/* Contenido del Paso */}
      {paso === 1 && renderPaso1()}
      {paso === 2 && renderPaso2()}
      {paso === 3 && renderPaso3()}
      
      {/* Mensajes de Error/Éxito */}
      {error && (
        <div className="mt-6 p-4 bg-red-100 text-red-700 border border-red-300 rounded-lg flex items-center gap-3">
          <AlertCircle /> {error} <button onClick={() => setError('')}><X className="w-5 h-5" /></button>
        </div>
      )}
      {exito && (
        <div className="mt-6 p-4 bg-green-100 text-green-700 border border-green-300 rounded-lg flex items-center gap-3">
          <CheckCircle /> {exito} <button onClick={() => setExito('')}><X className="w-5 h-5" /></button>
        </div>
      )}

    </div>
  );

  /**
   * PASO 1: Configuración y Upload
   */
  const renderPaso1 = () => (
    <div className="bg-white p-8 rounded-2xl shadow-xl">
      <h3 className="text-2xl font-bold text-gray-800 mb-6">Paso 1: Configuración Inicial</h3>
      
      {/* Input del Cliente (¡NUEVO!) */}
      <div className="mb-6">
        <label className="block text-lg font-semibold text-gray-700 mb-2" htmlFor="clienteNombre">
          <UserPlus className="w-5 h-5 inline-block mr-2" />
          Nombre del Cliente o Proyecto
        </label>
        <input
          id="clienteNombre"
          type="text"
          value={nombreCliente}
          onChange={(e) => setNombreCliente(e.target.value)}
          placeholder="Ej: Constructora ACME S.A.C."
          className="w-full p-4 border border-gray-300 rounded-lg text-lg"
        />
        <p className="text-sm text-gray-500 mt-1">Esto creará una carpeta única para organizar sus archivos.</p>
      </div>

      {/* Descripción */}
      <div className="mb-6">
        <label className="block text-lg font-semibold text-gray-700 mb-2" htmlFor="descripcion">
          <MessageSquare className="w-5 h-5 inline-block mr-2" />
          Descripción del {tipoFlujo.split('-')[0]}
        </label>
        <textarea
          id="descripcion"
          rows="5"
          value={contextoUsuario}
          onChange={(e) => setContextoUsuario(e.target.value)}
          placeholder={
            tipoFlujo.includes('cotizacion') ? "Ej: Necesito una cotización para la instalación de 50 puntos de luz y 30 tomacorrientes en una oficina de 100m²..." :
            tipoFlujo.includes('informe') ? "Ej: Generar un informe ejecutivo sobre el avance del Proyecto Alfa, incluyendo KPIs de este mes..." :
            "Ej: Iniciar la gestión del Proyecto 'Torre Beta', cliente ACME..."
          }
          className="w-full p-4 border border-gray-300 rounded-lg text-lg"
        />
      </div>

      {/* Upload (Opcional para 'simple', requerido para 'complejo') */}
      {tipoFlujo.includes('compleja') && (
        <div className="mb-6">
          <label className="block text-lg font-semibold text-gray-700 mb-2">
            <Upload className="w-5 h-5 inline-block mr-2" />
            Subir Documentos (PDF, DOCX, XLSX, JPG, PNG)
          </label>
          <div 
            onClick={() => fileInputRef.current && fileInputRef.current.click()}
            className="w-full p-10 border-2 border-dashed border-gray-300 rounded-lg text-center cursor-pointer hover:bg-gray-50"
          >
            <Upload className="w-12 h-12 mx-auto text-gray-400" />
            <p className="mt-2 text-gray-600">Arrastra archivos aquí o haz clic para seleccionar</p>
            <input
              type="file"
              ref={fileInputRef}
              multiple
              onChange={handleFileChange}
              className="hidden"
            />
          </div>
          <div className="mt-4">
            {archivos.map((file, index) => (
              <div key={index} className="flex justify-between items-center p-2 bg-gray-100 rounded-lg mb-2">
                <span className="text-gray-700 truncate"><FileText className="w-4 h-4 inline-block mr-2" />{file.name}</span>
                <button onClick={() => eliminarArchivo(index)} className="text-red-500 hover:text-red-700">
                  <X className="w-5 h-5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
      
      <button 
        onClick={handleIniciarChat}
        disabled={analizando}
        className="w-full p-4 bg-red-800 text-white text-xl font-bold rounded-lg hover:bg-red-700 transition-all flex items-center justify-center gap-3 disabled:bg-gray-400"
      >
        {analizando ? <Loader className="animate-spin" /> : <Zap />}
        Iniciar Asistente IA
      </button>
    </div>
  );
  
  /**
   * PASO 2: Chat Conversacional
   */
  const renderPaso2 = () => (
    <div className="bg-white p-8 rounded-2xl shadow-xl flex flex-col" style={{ height: '70vh' }}>
      <h3 className="text-2xl font-bold text-gray-800 mb-4 flex-shrink-0">Paso 2: Chat con Asistente IA</h3>
      
      {/* Contenedor del Chat */}
      <div 
        ref={chatContainerRef}
        className="flex-grow bg-gray-100 rounded-lg p-4 overflow-y-auto mb-4 border border-gray-300"
      >
        {conversacion.map((msg, index) => (
          <div key={index} className={`flex mb-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'ia' && <span className="w-10 h-10 rounded-full bg-red-800 text-white flex items-center justify-center font-bold text-lg mr-3 flex-shrink-0">IA</span>}
            <div 
              className={`p-4 rounded-2xl max-w-3xl ${
                msg.role === 'user' ? 'bg-blue-600 text-white rounded-br-none' : 
                msg.role === 'ia' ? 'bg-white text-gray-800 rounded-bl-none shadow' :
                'bg-yellow-100 text-yellow-800 text-sm italic w-full'
              }`}
            >
              {/* Aquí podríamos renderizar Markdown si la IA responde con él */}
              {msg.content}
            </div>
            {msg.role === 'user' && <span className="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-semibold text-lg ml-3 flex-shrink-0">TU</span>}
          </div>
        ))}
        {analizando && (
          <div className="flex justify-start mb-4">
            <span className="w-10 h-10 rounded-full bg-red-800 text-white flex items-center justify-center font-bold text-lg mr-3 flex-shrink-0">IA</span>
            <div className="p-4 rounded-2xl bg-white text-gray-800 rounded-bl-none shadow">
              <Loader className="animate-spin" />
            </div>
          </div>
        )}
      </div>

      {/* Input del Chat */}
      <div className="flex gap-2 flex-shrink-0">
        <input
          type="text"
          value={inputChat}
          onChange={(e) => setInputChat(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && !analizando && handleEnviarMensajeChat()}
          placeholder="Escribe tu respuesta o haz una pregunta..."
          className="flex-grow p-4 border border-gray-300 rounded-lg text-lg"
          disabled={analizando}
        />
        {/* Aquí iría el botón de Upload DENTRO del chat */}
        <button 
          onClick={handleEnviarMensajeChat}
          disabled={analizando}
          className="p-4 bg-red-800 text-white rounded-lg hover:bg-red-700 transition-all disabled:bg-gray-400"
        >
          <Send className="w-6 h-6" />
        </button>
      </div>
      <button 
        onClick={() => setPaso(3)}
        disabled={!cotizacion}
        className="w-full mt-4 p-3 bg-green-600 text-white font-bold rounded-lg hover:bg-green-500 transition-all disabled:bg-gray-400"
      >
        Ir a Edición/Revisión
      </button>
    </div>
  );

  /**
   * PASO 3: Edición y Descarga
   */
  const renderPaso3 = () => (
    <div className="bg-white p-8 rounded-2xl shadow-xl">
      <h3 className="text-2xl font-bold text-gray-800 mb-6">Paso 3: Revisión y Edición</h3>
      
      {/* Botones de Acción */}
      <div className="flex flex-wrap gap-4 mb-6 pb-6 border-b border-gray-300">
        <button 
          onClick={() => setModoEdicion(!modoEdicion)}
          className={`p-3 rounded-lg flex items-center gap-2 font-semibold ${
            modoEdicion ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-700'
          }`}
        >
          {modoEdicion ? <Eye /> : <Edit />}
          {modoEdicion ? 'Ver Vista Previa' : 'Activar Edición'}
        </button>
        <button 
          onClick={() => setPaso(2)}
          className="p-3 rounded-lg flex items-center gap-2 font-semibold bg-gray-100 text-gray-700"
        >
          <MessageSquare /> Volver al Chat
        </button>
        <button 
          onClick={() => handleDescargar('word')}
          disabled={descargando === 'word'}
          className="p-3 rounded-lg flex items-center gap-2 font-semibold bg-blue-600 text-white ml-auto disabled:bg-gray-400"
        >
          {descargando === 'word' ? <Loader className="animate-spin" /> : <Download />}
          Generar .DOCX
        </button>
        <button 
          onClick={() => handleDescargar('pdf')}
          disabled={descargando === 'pdf'}
          className="p-3 rounded-lg flex items-center gap-2 font-semibold bg-red-600 text-white disabled:bg-gray-400"
        >
          {descargando === 'pdf' ? <Loader className="animate-spin" /> : <Download />}
          Generar .PDF
        </button>
      </div>

      {/* Renderizado de la Cotización (o Informe/Proyecto) */}
      {!cotizacion ? (
        <div className="text-center p-12 bg-gray-50 rounded-lg">
          <Loader className="w-12 h-12 mx-auto text-gray-400 animate-spin" />
          <p className="mt-4 text-gray-600">Cargando cotización...</p>
        </div>
      ) : (
        renderCotizacionEditable(cotizacion)
      )}
    </div>
  );

  /**
   * Componente de Edición (del Artefacto)
   * ¡Este es el editor!
   */
  const renderCotizacionEditable = (cot) => {
    
    // Calcular totales (por si acaso)
    const totales = {
      subtotal: cot.subtotal || 0,
      igv: cot.igv || 0,
      total: cot.total || 0,
    };

    const renderCampo = (valor, capIndex, itemIndex, campo) => {
      if (modoEdicion) {
        return (
          <input
            type={campo === 'descripcion' ? 'text' : 'number'}
            value={valor}
            onChange={(e) => handleEditarItem(capIndex, itemIndex, campo, e.target.value)}
            className={`p-1 border rounded w-full ${campo === 'descripcion' ? 'text-left' : 'text-right'}`}
          />
        );
      }
      return valor;
    };
    
    const renderCampoHeader = (valor, campo) => {
      if (modoEdicion) {
        return (
          <input
            type="text"
            value={valor}
            onChange={(e) => setCotizacion(prev => ({...prev, [campo]: e.target.value}))}
            className="p-1 border rounded w-full text-lg"
          />
        );
      }
      return <span className="text-lg">{valor}</span>;
    };
    
    return (
      <div className="p-8 border border-gray-300 rounded-lg bg-white shadow-inner">
        {/* Cabecera */}
        <div className="flex justify-between items-start mb-8">
          <div>
            <h2 className="text-3xl font-bold text-red-900">{datosEmpresa.nombre}</h2>
            <p className="text-gray-600">{datosEmpresa.direccion}</p>
            <p className="text-gray-600">RUC: {datosEmpresa.ruc}</p>
          </div>
          <div className="text-right p-4 border-4 border-red-900 rounded-lg">
            <h3 className="text-3xl font-bold text-red-900">COTIZACIÓN</h3>
            <span className="text-2xl font-semibold text-gray-700">{cot.numero || "COT-XXXX-0000"}</span>
          </div>
        </div>
        
        {/* Info Cliente */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="text-sm font-bold text-red-800 mb-2">CLIENTE</h4>
            <div className="space-y-1">
              <div><strong>Nombre:</strong> {renderCampoHeader(cot.cliente, 'cliente')}</div>
              <div><strong>Proyecto:</strong> {renderCampoHeader(cot.proyecto, 'proyecto')}</div>
            </div>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="text-sm font-bold text-red-800 mb-2">DETALLES</h4>
            <div className="space-y-1">
              <div><strong>Fecha:</strong> {new Date(cot.fecha_creacion || Date.now()).toLocaleDateString()}</div>
              <div><strong>Vigencia:</strong> {renderCampoHeader(cot.vigencia, 'vigencia')}</div>
            </div>
          </div>
        </div>
        
        {/* Items */}
        <div className="mb-8">
          <table className="w-full border-collapse">
            <thead className="bg-gray-800 text-white">
              <tr>
                <th className="p-3 text-left font-semibold">Descripción</th>
                <th className="p-3 text-right font-semibold w-24">Cant.</th>
                <th className="p-3 text-right font-semibold w-24">Unidad</th>
                <th className="p-3 text-right font-semibold w-32">P. Unit.</th>
                <th className="p-3 text-right font-semibold w-32">Total</th>
                {modoEdicion && <th className="p-3 w-12"></th>}
              </tr>
            </thead>
            <tbody>
              {/* Lógica para renderizar capítulos o items simples */}
              {cot.capitulos ? (
                cot.capitulos.map((cap, cIndex) => (
                  <React.Fragment key={cIndex}>
                    <tr className="bg-gray-100">
                      <td colSpan={modoEdicion ? 6 : 5} className="p-2 font-bold text-gray-700">
                        {modoEdicion ? <input type="text" value={cap.nombre} onChange={(e) => {/* Lógica editar cap */}} className="w-full p-1 font-bold" /> : cap.nombre}
                      </td>
                    </tr>
                    {cap.items.map((item, iIndex) => (
                      <tr key={iIndex} className="border-b">
                        <td className="p-2">{renderCampo(item.descripcion, cIndex, iIndex, 'descripcion')}</td>
                        <td className="p-2 text-right">{renderCampo(item.cantidad, cIndex, iIndex, 'cantidad')}</td>
                        <td className="p-2 text-right">{renderCampo(item.unidad, cIndex, iIndex, 'unidad')}</td>
                        <td className="p-2 text-right">{renderCampo(item.precio_unitario, cIndex, iIndex, 'precio_unitario')}</td>
                        <td className="p-2 text-right font-semibold">S/ {parseFloat(item.total || 0).toFixed(2)}</td>
                        {modoEdicion && <td className="p-2 text-center"><button onClick={() => handleEliminarItem(cIndex, iIndex)} className="text-red-500"><X /></button></td>}
                      </tr>
                    ))}
                    {modoEdicion && <tr><td colSpan={6}><button onClick={() => handleAgregarItem(cIndex)} className="text-blue-500 p-1">+ Agregar Item</button></td></tr>}
                  </React.Fragment>
                ))
              ) : (
                cot.items.map((item, iIndex) => (
                  <tr key={iIndex} className="border-b">
                    <td className="p-2">{renderCampo(item.descripcion, null, iIndex, 'descripcion')}</td>
                    <td className="p-2 text-right">{renderCampo(item.cantidad, null, iIndex, 'cantidad')}</td>
                    <td className="p-2 text-right">{renderCampo(item.unidad, null, iIndex, 'unidad')}</td>
                    <td className="p-2 text-right">{renderCampo(item.precio_unitario, null, iIndex, 'precio_unitario')}</td>
                    <td className="p-2 text-right font-semibold">S/ {parseFloat(item.total || 0).toFixed(2)}</td>
                    {modoEdicion && <td className="p-2 text-center"><button onClick={() => handleEliminarItem(null, iIndex)} className="text-red-500"><X /></button></td>}
                  </tr>
                ))
              )}
              {modoEdicion && !cot.capitulos && <tr><td colSpan={6}><button onClick={() => handleAgregarItem(null)} className="text-blue-500 p-1">+ Agregar Item</button></td></tr>}
            </tbody>
          </table>
        </div>
        
        {/* Totales */}
        <div className="flex justify-end mb-8">
          <div className="w-full md:w-96">
            <div className="flex justify-between py-3 border-b-2 border-gray-300 text-lg">
              <span className="font-semibold">Subtotal:</span>
              <span className="font-bold">S/ {totales.subtotal}</span>
            </div>
            <div className="flex justify-between py-3 border-b-2 border-gray-300 text-lg">
              <span className="font-semibold">IGV (18%):</span>
              <span className="font-bold">S/ {totales.igv}</span>
            </div>
            <div className="flex justify-between py-6 bg-gradient-to-r from-red-900 via-red-800 to-red-900 text-yellow-400 px-6 rounded-2xl mt-4 shadow-2xl border-4 border-yellow-600">
              <span className="font-black text-3xl">TOTAL:</span>
              <span className="font-black text-5xl">S/ {totales.total}</span>
            </div>
          </div>
        </div>

        {/* Observaciones y Pie de Página */}
        <div className="mt-8 pt-6 border-t-2 text-sm text-gray-600">
          <h4 className="text-md font-bold text-red-800 mb-2">OBSERVACIONES</h4>
          {modoEdicion ? (
            <textarea 
              value={cot.observaciones}
              onChange={(e) => setCotizacion(prev => ({...prev, observaciones: e.target.value}))}
              className="w-full p-2 border rounded"
              rows="3"
            />
          ) : (
            <p className="whitespace-pre-wrap">{cot.observaciones}</p>
          )}

          <div className="mt-8 pt-6 border-t-2 text-center text-sm text-gray-600">
            <p className="font-bold text-red-900">{datosEmpresa.nombre}</p>
            <p>📱 WhatsApp: {datosEmpresa.telefono}</p>
            <p>📧 {datosEmpresa.email}</p>
            <p>{datosEmpresa.direccion}</p>
          </div>
        </div>
        
      </div>
    );
  };


  // Render principal de la App
  return (
    <div className="bg-gray-50 min-h-screen font-sans">
      <nav className="bg-white shadow-md w-full sticky top-0 z-50 no-print">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <div className="flex-shrink-0 flex items-center">
              {/* Aquí podrías poner el logo de Tesla */}
              <span className="font-black text-3xl text-red-900">TESLA</span>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <button 
                  onClick={volverAInicio}
                  className="text-gray-700 hover:bg-red-800 hover:text-white px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2"
                >
                  <Home className="w-4 h-4" /> Inicio
                </button>
                {/* Otros botones de navegación si los tuvieras */}
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="py-10">
        {pantallaActual === 'inicio' && renderInicio()}
        {pantallaActual === 'flujo' && renderFlujo()}
      </main>
    </div>
  );
};

export default CotizadorTesla30;