import React, { useState, useRef } from 'react';
import { Upload, MessageSquare, FileText, Download, Zap, Send, Loader, Edit, Save, AlertCircle, CheckCircle, X, RefreshCw, Home, FolderOpen, Eye, EyeOff, Folder, Users, TrendingUp, Clock, BarChart3, FileCheck, Briefcase, ChevronDown, ChevronUp, Layout, Layers, BookOpen } from 'lucide-react';

const CotizadorTesla30 = () => {
  // ESTADOS PRINCIPALES
  const [pantallaActual, setPantallaActual] = useState('inicio');
  const [tipoFlujo, setTipoFlujo] = useState(null);
  
  // Estados de menús expandibles
  const [menuCotizaciones, setMenuCotizaciones] = useState(false);
  const [menuProyectos, setMenuProyectos] = useState(false);
  const [menuInformes, setMenuInformes] = useState(false);
  
  // Estados del flujo de cotización
  const [paso, setPaso] = useState(1);
  const [archivos, setArchivos] = useState([]);
  const [conversacion, setConversacion] = useState([]);
  const [contextoUsuario, setContextoUsuario] = useState('');
  const [inputChat, setInputChat] = useState('');
  const [analizando, setAnalizando] = useState(false);
  const [cotizacion, setCotizacion] = useState(null);
  const [modoEdicion, setModoEdicion] = useState(true);
  const [error, setError] = useState('');
  const [exito, setExito] = useState('');
  const [servicioSeleccionado, setServicioSeleccionado] = useState('');
  const [industriaSeleccionada, setIndustriaSeleccionada] = useState('');
  const [versionCotizacion, setVersionCotizacion] = useState(1.0);
  const [ocultarPreciosUnitarios, setOcultarPreciosUnitarios] = useState(false);
  const [ocultarTotalesPorItem, setOcultarTotalesPorItem] = useState(false);
  const [modoVisualizacionIGV, setModoVisualizacionIGV] = useState('sin-igv');
  
  // Estados para proyectos
  const [proyectoActual, setProyectoActual] = useState(null);
  const [vistaProyecto, setVistaProyecto] = useState('dashboard');
  
  const [datosEmpresa] = useState({
    nombre: 'TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.',
    ruc: '20601138787',
    direccion: 'Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos',
    telefono: '906315961',
    email: 'ingenieria.teslaelectricidad@gmail.com',
    ciudad: 'San Juan de Lurigancho, Lima - Perú'
  });

  const servicios = [
    { id: 'electricidad', nombre: '⚡ Electricidad', descripcion: 'Instalaciones eléctricas completas' },
    { id: 'itse', nombre: '📋 Certificado ITSE', descripcion: 'Inspección técnica de seguridad' },
    { id: 'puesta-tierra', nombre: '🔌 Puesta a Tierra', descripcion: 'Sistemas de protección eléctrica' },
    { id: 'contra-incendios', nombre: '🔥 Contra Incendios', descripcion: 'Sistemas de detección y extinción' },
    { id: 'domotica', nombre: '🏠 Domótica', descripcion: 'Automatización inteligente' },
    { id: 'cctv', nombre: '📹 CCTV', descripcion: 'Videovigilancia profesional' },
    { id: 'redes', nombre: '🌐 Redes', descripcion: 'Cableado estructurado' },
    { id: 'automatizacion-industrial', nombre: '⚙️ Automatización Industrial', descripcion: 'PLCs y control de procesos' },
  ];

  const industrias = [
    { id: 'construccion', nombre: '🏗️ Construcción' },
    { id: 'arquitectura', nombre: '🏢 Arquitectura' },
    { id: 'industrial', nombre: '⚙️ Industrial' },
    { id: 'mineria', nombre: '⛏️ Minería' },
    { id: 'educacion', nombre: '🎓 Educación' },
    { id: 'salud', nombre: '🏥 Salud' },
    { id: 'retail', nombre: '🏪 Retail' },
    { id: 'residencial', nombre: '🏘️ Residencial' },
  ];

  // DATOS MOCK
  const cotizacionMock = {
    cliente: {
      nombre: 'Empresa Demo S.A.C.',
      proyecto: 'Instalación Eléctrica Completa',
      direccion: 'Av. Principal 123, Lima',
      pisos: 5,
      departamentos: 20
    },
    items: [
      { capitulo: 'INSTALACIONES ELÉCTRICAS', descripcion: 'Punto de luz empotrado LED 18W', cantidad: 50, unidad: 'und', precioUnitario: 25.00, observacion: 'Incluye materiales y mano de obra' },
      { capitulo: 'INSTALACIONES ELÉCTRICAS', descripcion: 'Tomacorriente doble 220V', cantidad: 40, unidad: 'und', precioUnitario: 28.00, observacion: 'Con placa decorativa' },
      { capitulo: 'TABLEROS', descripcion: 'Tablero general trifásico 36 polos', cantidad: 1, unidad: 'und', precioUnitario: 2800.00, observacion: 'Incluye interruptores termomagnéticos' },
    ]
  };

  const proyectoMock = {
    id: 'PROJ-2025-001',
    nombre: 'Fibra Óptica Nacional 5000km',
    cliente: 'Ministerio de Transporte',
    tipo: 'instalacion',
    duracion_meses: 12,
    presupuesto_estimado: 5500000,
    avance: 35,
    archivos_count: 47,
    hitos: [
      { nombre: 'Fase 1: Zona Norte', completado: true },
      { nombre: 'Fase 2: Zona Centro', completado: false },
    ]
  };

  // FUNCIONES
  const volverAlInicio = () => {
    setPantallaActual('inicio');
    setTipoFlujo(null);
    setPaso(1);
    setProyectoActual(null);
    setExito('Sistema reiniciado');
    setTimeout(() => setExito(''), 2000);
  };

  const iniciarFlujo = (tipo) => {
    setTipoFlujo(tipo);
    setPantallaActual(tipo);
    setPaso(1);
  };

  const simularGenerarCotizacion = () => {
    setAnalizando(true);
    setTimeout(() => {
      setCotizacion(cotizacionMock);
      setPantallaActual('cotizacion-final');
      setAnalizando(false);
      setExito('✅ Cotización generada (DEMO)');
      setTimeout(() => setExito(''), 3000);
    }, 2000);
  };

  const simularCrearProyecto = () => {
    setAnalizando(true);
    setTimeout(() => {
      setProyectoActual(proyectoMock);
      setVistaProyecto('dashboard');
      setAnalizando(false);
      setExito('✅ Proyecto creado (DEMO)');
      setTimeout(() => setExito(''), 3000);
    }, 1500);
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

  const totales = calcularTotales();

  // ============================================
  // PANTALLA 1: INICIO CON MENÚS EXPANDIBLES
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
                        <p className="text-gray-400 text-sm">Gestión básica sin carpetas dedicadas</p>
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
                        <p className="text-gray-400 text-sm">Con carpetas, Gantt, hitos y seguimiento avanzado</p>
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
                        <p className="text-gray-400 text-sm">PDF básico con cotización estándar</p>
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
                        <p className="text-gray-400 text-sm">Word personalizable con tablas, gráficos y formato APA</p>
                      </div>
                    </div>
                  </button>
                </div>
              )}
            </div>

          </div>

          {/* INFORMACIÓN ADICIONAL */}
          <div className="mt-8 bg-gradient-to-br from-gray-900 to-black rounded-xl p-6 border border-gray-700">
            <p className="text-center text-gray-400 text-sm">
              💡 <span className="text-yellow-400 font-semibold">Tip:</span> Los flujos complejos incluyen funcionalidades avanzadas como IA contextual, gestión de archivos y seguimiento de hitos
            </p>
          </div>
        </div>

        <style jsx>{`
          @keyframes fadeIn {
            from {
              opacity: 0;
              transform: translateY(-10px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
          .animate-fadeIn {
            animation: fadeIn 0.3s ease-out;
          }
        `}</style>
      </div>
    );
  }

  // ============================================
  // PANTALLA 2: COTIZACIÓN RÁPIDA/COMPLEJA
  // ============================================
  if (pantallaActual === 'cotizacion-rapida' || pantallaActual === 'cotizacion-compleja') {
    const esCompleja = pantallaActual === 'cotizacion-compleja';
    
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6">
        <div className="max-w-7xl mx-auto">
          <button onClick={volverAlInicio}
            className="fixed top-6 right-6 z-50 bg-gradient-to-r from-red-900 to-red-800 hover:from-red-800 hover:to-red-700 text-yellow-400 px-4 py-2 rounded-lg font-semibold flex items-center gap-2 shadow-2xl border-2 border-yellow-600 backdrop-blur-md transition-all duration-300 hover:scale-105">
            <Home className="w-5 h-5" />
            Inicio
          </button>

          <div className="bg-gradient-to-r from-red-950 via-red-900 to-black rounded-2xl p-8 mb-6 border-2 border-yellow-600 shadow-2xl backdrop-blur-md bg-opacity-90 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-yellow-600/10 via-transparent to-yellow-600/10 animate-pulse"></div>
            <div className="relative z-10">
              <h1 className="text-4xl font-bold flex items-center gap-3 text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-yellow-300 to-yellow-500">
                {esCompleja ? <Layers className="w-10 h-10 text-purple-400" /> : <Zap className="w-10 h-10 text-yellow-400 animate-pulse" />}
                {esCompleja ? 'Cotización Compleja' : 'Cotización Rápida'}
              </h1>
              <p className="text-yellow-400 mt-2 font-semibold">
                {esCompleja ? 'Análisis detallado para proyectos de gran envergadura' : 'Proceso simplificado para proyectos estándar'}
              </p>
            </div>
          </div>

          {error && <Alerta tipo="error" mensaje={error} onClose={() => setError('')} />}
          {exito && <Alerta tipo="exito" mensaje={exito} onClose={() => setExito('')} />}

          <div className="space-y-6">
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-700 shadow-xl backdrop-blur-md bg-opacity-90">
              <h2 className="text-2xl font-bold mb-4 text-yellow-400">1. Tipo de Servicio</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {servicios.map(servicio => (
                  <button
                    key={servicio.id}
                    onClick={() => setServicioSeleccionado(servicio.id)}
                    className={`p-4 rounded-xl border-2 transition-all duration-300 text-left ${
                      servicioSeleccionado === servicio.id
                        ? 'border-yellow-500 bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl scale-105'
                        : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800'
                    }`}>
                    <div className="text-2xl mb-2">{servicio.nombre.split(' ')[0]}</div>
                    <div className="text-sm font-semibold">{servicio.nombre.split(' ').slice(1).join(' ')}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-700 shadow-xl backdrop-blur-md bg-opacity-90">
              <h2 className="text-2xl font-bold mb-4 text-yellow-400">2. Industria</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {industrias.map(industria => (
                  <button
                    key={industria.id}
                    onClick={() => setIndustriaSeleccionada(industria.id)}
                    className={`p-3 rounded-xl border-2 transition-all duration-300 ${
                      industriaSeleccionada === industria.id
                        ? 'border-yellow-500 bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl'
                        : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800'
                    }`}>
                    <div className="text-sm font-semibold">{industria.nombre}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-700 shadow-xl backdrop-blur-md bg-opacity-90">
              <h2 className="text-2xl font-bold mb-4 text-yellow-400">3. Información del Proyecto</h2>
              
              <textarea 
                value={contextoUsuario} 
                onChange={(e) => setContextoUsuario(e.target.value)}
                className={`w-full ${esCompleja ? 'h-48' : 'h-32'} px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none resize-none mb-4 text-white placeholder-gray-500`}
                placeholder={esCompleja 
                  ? "Describe el proyecto completo en detalle:\n- Alcance del trabajo\n- Requerimientos especiales\n- Plazos estimados\n- Restricciones o consideraciones importantes..." 
                  : "Describe tu proyecto brevemente... Ejemplo: Necesito instalación eléctrica para 5 departamentos..."} />

              {esCompleja && (
                <div className="mb-4 p-4 bg-purple-950 bg-opacity-50 border border-purple-700 rounded-xl">
                  <p className="text-sm text-purple-300 font-semibold mb-2">ℹ️ Cotización Compleja incluye:</p>
                  <ul className="text-xs text-gray-300 space-y-1">
                    <li>• Análisis detallado con IA avanzada</li>
                    <li>• Múltiples iteraciones de refinamiento</li>
                    <li>• Desglose por fases del proyecto</li>
                    <li>• Análisis de riesgos y contingencias</li>
                  </ul>
                </div>
              )}

              <div className="border-2 border-dashed border-gray-700 rounded-xl p-6 text-center hover:border-yellow-600 transition-all cursor-pointer bg-gray-950 bg-opacity-50">
                <Upload className="w-12 h-12 mx-auto mb-3 text-yellow-500" />
                <p className="text-sm text-gray-400 font-semibold">Sube documentos opcionales (máx 10MB)</p>
                <p className="text-xs text-gray-500 mt-2">PDF, Excel, Word, imágenes, JSON, TXT, CSV</p>
              </div>
            </div>

            <button 
              onClick={simularGenerarCotizacion} 
              disabled={!servicioSeleccionado || !industriaSeleccionada || analizando}
              className={`w-full ${esCompleja ? 'bg-gradient-to-r from-purple-600 via-purple-500 to-purple-600 hover:from-purple-500 hover:to-purple-400 border-purple-400' : 'bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 border-yellow-400'} disabled:from-gray-800 disabled:to-gray-700 disabled:cursor-not-allowed py-4 rounded-xl font-bold text-lg ${esCompleja ? 'text-white' : 'text-black'} shadow-2xl border-2 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-3`}>
              {analizando ? (
                <>
                  <Loader className="w-6 h-6 animate-spin" />
                  Generando cotización...
                </>
              ) : (
                <>
                  {esCompleja ? <Layers className="w-6 h-6" /> : <Zap className="w-6 h-6" />}
                  {esCompleja ? 'Generar Cotización Compleja' : 'Generar Cotización Rápida'}
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ============================================
  // PANTALLA 3: PROYECTO SIMPLE/COMPLEJO
  // ============================================
  if (pantallaActual === 'proyecto-simple' || pantallaActual === 'proyecto-complejo') {
    const esComplejo = pantallaActual === 'proyecto-complejo';

    if (!proyectoActual) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6">
          <div className="max-w-5xl mx-auto">
            <button onClick={volverAlInicio}
              className="fixed top-6 right-6 z-50 bg-gradient-to-r from-red-900 to-red-800 hover:from-red-800 hover:to-red-700 text-yellow-400 px-4 py-2 rounded-lg font-semibold flex items-center gap-2 shadow-2xl border-2 border-yellow-600 backdrop-blur-md transition-all duration-300 hover:scale-105">
              <Home className="w-5 h-5" />
              Inicio
            </button>

            <div className={`bg-gradient-to-r ${esComplejo ? 'from-purple-950 via-purple-900 to-black border-purple-600' : 'from-blue-950 via-blue-900 to-black border-blue-600'} rounded-2xl p-8 mb-6 border-2 shadow-2xl backdrop-blur-md bg-opacity-90`}>
              <h1 className={`text-4xl font-bold flex items-center gap-3 ${esComplejo ? 'text-purple-400' : 'text-blue-400'}`}>
                {esComplejo ? <Layout className="w-10 h-10" /> : <Folder className="w-10 h-10" />}
                {esComplejo ? 'Crear Proyecto Complejo' : 'Crear Proyecto Simple'}
              </h1>
              <p className={`${esComplejo ? 'text-purple-300' : 'text-blue-300'} mt-2 font-semibold`}>
                {esComplejo ? 'Gestión avanzada con carpetas, Gantt y seguimiento de hitos' : 'Gestión básica para proyectos estándar'}
              </p>
            </div>

            {error && <Alerta tipo="error" mensaje={error} onClose={() => setError('')} />}
            {exito && <Alerta tipo="exito" mensaje={exito} onClose={() => setExito('')} />}

            <div className={`bg-gradient-to-br from-gray-900 to-black rounded-2xl p-8 border-2 ${esComplejo ? 'border-purple-700' : 'border-blue-700'} shadow-xl backdrop-blur-md bg-opacity-90`}>
              <div className="space-y-6">
                <div>
                  <label className={`block ${esComplejo ? 'text-purple-400' : 'text-blue-400'} font-semibold mb-2`}>Nombre del Proyecto *</label>
                  <input 
                    type="text"
                    className={`w-full px-4 py-3 bg-gray-950 border ${esComplejo ? 'border-purple-700 focus:ring-purple-500' : 'border-blue-700 focus:ring-blue-500'} rounded-xl focus:ring-2 focus:outline-none text-white`}
                    placeholder="Ej: Instalación Eléctrica Torre Office"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className={`block ${esComplejo ? 'text-purple-400' : 'text-blue-400'} font-semibold mb-2`}>Cliente *</label>
                    <input 
                      type="text"
                      className={`w-full px-4 py-3 bg-gray-950 border ${esComplejo ? 'border-purple-700 focus:ring-purple-500' : 'border-blue-700 focus:ring-blue-500'} rounded-xl focus:ring-2 focus:outline-none text-white`}
                      placeholder="Nombre del cliente"
                    />
                  </div>
                  <div>
                    <label className={`block ${esComplejo ? 'text-purple-400' : 'text-blue-400'} font-semibold mb-2`}>Presupuesto Estimado (S/)</label>
                    <input 
                      type="number"
                      className={`w-full px-4 py-3 bg-gray-950 border ${esComplejo ? 'border-purple-700 focus:ring-purple-500' : 'border-blue-700 focus:ring-blue-500'} rounded-xl focus:ring-2 focus:outline-none text-white`}
                      placeholder="50000"
                    />
                  </div>
                </div>

                {esComplejo && (
                  <div className="bg-purple-950 bg-opacity-50 border border-purple-700 rounded-xl p-6">
                    <h3 className="text-purple-400 font-bold mb-3">🗂️ Sistema de Carpetas Automático</h3>
                    <p className="text-gray-300 text-sm mb-4">
                      Se creará una estructura organizada de carpetas:
                    </p>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
                      <div className="bg-gray-900 p-3 rounded-lg">📐 Planos</div>
                      <div className="bg-gray-900 p-3 rounded-lg">📋 Especificaciones</div>
                      <div className="bg-gray-900 p-3 rounded-lg">📜 Normativas</div>
                      <div className="bg-gray-900 p-3 rounded-lg">💰 Presupuestos</div>
                      <div className="bg-gray-900 p-3 rounded-lg">📸 Fotos</div>
                      <div className="bg-gray-900 p-3 rounded-lg">📄 Contratos</div>
                    </div>
                  </div>
                )}

                <button 
                  onClick={simularCrearProyecto}
                  disabled={analizando}
                  className={`w-full ${esComplejo ? 'bg-gradient-to-r from-purple-600 via-purple-500 to-purple-600 hover:from-purple-500 hover:to-purple-400 border-purple-400' : 'bg-gradient-to-r from-blue-600 via-blue-500 to-blue-600 hover:from-blue-500 hover:to-blue-400 border-blue-400'} disabled:from-gray-800 disabled:to-gray-700 disabled:cursor-not-allowed py-4 rounded-xl font-bold text-lg text-white shadow-2xl border-2 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-3`}>
                  {analizando ? (
                    <>
                      <Loader className="w-6 h-6 animate-spin" />
                      Creando proyecto...
                    </>
                  ) : (
                    <>
                      {esComplejo ? <Layout className="w-6 h-6" /> : <Folder className="w-6 h-6" />}
                      {esComplejo ? 'Crear Proyecto Complejo' : 'Crear Proyecto Simple'}
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    // Dashboard del proyecto creado
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6">
        <div className="max-w-7xl mx-auto">
          <button onClick={volverAlInicio}
            className="fixed top-6 right-6 z-50 bg-gradient-to-r from-red-900 to-red-800 hover:from-red-800 hover:to-red-700 text-yellow-400 px-4 py-2 rounded-lg font-semibold flex items-center gap-2 shadow-2xl border-2 border-yellow-600 backdrop-blur-md transition-all duration-300 hover:scale-105">
            <Home className="w-5 h-5" />
            Inicio
          </button>

          <div className={`bg-gradient-to-r ${esComplejo ? 'from-purple-950 via-purple-900 to-black border-purple-600' : 'from-blue-950 via-blue-900 to-black border-blue-600'} rounded-2xl p-8 mb-6 border-2 shadow-2xl backdrop-blur-md bg-opacity-90`}>
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  {esComplejo ? <Layout className="w-10 h-10 text-purple-400" /> : <Folder className="w-10 h-10 text-blue-400" />}
                  <div>
                    <h1 className={`text-3xl font-bold ${esComplejo ? 'text-purple-400' : 'text-blue-400'}`}>{proyectoActual.nombre}</h1>
                    <p className={`${esComplejo ? 'text-purple-300' : 'text-blue-300'} text-sm`}>{proyectoActual.cliente} • {proyectoActual.id}</p>
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="bg-blue-900 px-4 py-2 rounded-lg mb-2">
                  <p className="text-blue-300 text-xs">Avance</p>
                  <p className="text-white font-bold">{proyectoActual.avance}%</p>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-gradient-to-br from-blue-900 to-blue-800 rounded-xl p-6 border border-blue-700 shadow-xl">
              <div className="flex items-center justify-between mb-2">
                <FileText className="w-8 h-8 text-blue-300" />
                <span className="text-3xl font-bold text-white">{proyectoActual.archivos_count}</span>
              </div>
              <p className="text-blue-200 text-sm">Archivos</p>
            </div>

            <div className="bg-gradient-to-br from-green-900 to-green-800 rounded-xl p-6 border border-green-700 shadow-xl">
              <div className="flex items-center justify-between mb-2">
                <Clock className="w-8 h-8 text-green-300" />
                <span className="text-3xl font-bold text-white">{proyectoActual.duracion_meses}</span>
              </div>
              <p className="text-green-200 text-sm">Meses</p>
            </div>

            <div className="bg-gradient-to-br from-purple-900 to-purple-800 rounded-xl p-6 border border-purple-700 shadow-xl">
              <div className="flex items-center justify-between mb-2">
                <TrendingUp className="w-8 h-8 text-purple-300" />
                <span className="text-2xl font-bold text-white">S/ {(proyectoActual.presupuesto_estimado / 1000000).toFixed(1)}M</span>
              </div>
              <p className="text-purple-200 text-sm">Presupuesto</p>
            </div>
          </div>

          <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-purple-700 shadow-xl backdrop-blur-md bg-opacity-90">
            <h2 className="text-2xl font-bold text-purple-400 mb-4">🎯 Hitos del Proyecto</h2>
            <div className="space-y-3">
              {proyectoActual.hitos.map((hito, index) => (
                <div 
                  key={index}
                  className={`p-4 rounded-xl border-2 ${
                    hito.completado 
                      ? 'border-green-600 bg-green-950 bg-opacity-30' 
                      : 'border-gray-700 bg-gray-900'
                  }`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {hito.completado ? (
                        <CheckCircle className="w-6 h-6 text-green-400" />
                      ) : (
                        <Clock className="w-6 h-6 text-gray-400" />
                      )}
                      <p className="font-semibold text-white">{hito.nombre}</p>
                    </div>
                    {hito.completado && (
                      <span className="bg-green-600 text-white px-3 py-1 rounded-full text-xs font-bold">
                        Completado
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <button 
              onClick={simularGenerarCotizacion}
              className="w-full mt-6 bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 py-4 rounded-xl font-bold text-lg text-black shadow-2xl border-2 border-yellow-400 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-3">
              <FileCheck className="w-6 h-6" />
              Generar Cotización del Proyecto
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ============================================
  // PANTALLA 4: INFORMES
  // ============================================
  if (pantallaActual === 'informe-simple' || pantallaActual === 'informe-ejecutivo') {
    const esEjecutivo = pantallaActual === 'informe-ejecutivo';

    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6">
        <div className="max-w-5xl mx-auto">
          <button onClick={volverAlInicio}
            className="fixed top-6 right-6 z-50 bg-gradient-to-r from-red-900 to-red-800 hover:from-red-800 hover:to-red-700 text-yellow-400 px-4 py-2 rounded-lg font-semibold flex items-center gap-2 shadow-2xl border-2 border-yellow-600 backdrop-blur-md transition-all duration-300 hover:scale-105">
            <Home className="w-5 h-5" />
            Inicio
          </button>

          <div className={`bg-gradient-to-r ${esEjecutivo ? 'from-purple-950 via-purple-900 to-black border-purple-600' : 'from-green-950 via-green-900 to-black border-green-600'} rounded-2xl p-8 mb-6 border-2 shadow-2xl backdrop-blur-md bg-opacity-90`}>
            <h1 className={`text-4xl font-bold flex items-center gap-3 ${esEjecutivo ? 'text-purple-400' : 'text-green-400'}`}>
              {esEjecutivo ? <BarChart3 className="w-10 h-10" /> : <FileText className="w-10 h-10" />}
              {esEjecutivo ? 'Informe Ejecutivo' : 'Informe Simple'}
            </h1>
            <p className={`${esEjecutivo ? 'text-purple-300' : 'text-green-300'} mt-2 font-semibold`}>
              {esEjecutivo ? 'Documento Word personalizable con tablas, gráficos y formato APA' : 'PDF básico con cotización estándar'}
            </p>
          </div>

          {error && <Alerta tipo="error" mensaje={error} onClose={() => setError('')} />}
          {exito && <Alerta tipo="exito" mensaje={exito} onClose={() => setExito('')} />}

          <div className={`bg-gradient-to-br from-gray-900 to-black rounded-2xl p-8 border-2 ${esEjecutivo ? 'border-purple-700' : 'border-green-700'} shadow-xl backdrop-blur-md bg-opacity-90 mb-6`}>
            <h2 className={`text-2xl font-bold mb-6 ${esEjecutivo ? 'text-purple-400' : 'text-green-400'}`}>
              {esEjecutivo ? '📊 Configuración de Informe Ejecutivo' : '📄 Configuración de Informe Simple'}
            </h2>

            <div className="space-y-6">
              <div>
                <label className={`block ${esEjecutivo ? 'text-purple-400' : 'text-green-400'} font-semibold mb-2`}>Proyecto a Informar *</label>
                <select className={`w-full px-4 py-3 bg-gray-950 border ${esEjecutivo ? 'border-purple-700 focus:ring-purple-500' : 'border-green-700 focus:ring-green-500'} rounded-xl focus:ring-2 focus:outline-none text-white`}>
                  <option>Seleccionar proyecto existente...</option>
                  <option>Instalación Eléctrica Torre Office</option>
                  <option>Sistema CCTV Planta Industrial</option>
                </select>
              </div>

              {esEjecutivo && (
                <>
                  <div className="bg-purple-950 bg-opacity-50 border border-purple-700 rounded-xl p-6">
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
                          <p className="font-semibold text-white">Tablas Profesionales</p>
                          <p className="text-gray-400">Desglose de costos, cronogramas</p>
                        </div>
                      </div>
                      <div className="flex items-start gap-2">
                        <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                        <div>
                          <p className="font-semibold text-white">Gráficos Automáticos</p>
                          <p className="text-gray-400">Distribución de costos, timeline</p>
                        </div>
                      </div>
                      <div className="flex items-start gap-2">
                        <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                        <div>
                          <p className="font-semibold text-white">Análisis Financiero</p>
                          <p className="text-gray-400">ROI, flujo de caja proyectado</p>
                        </div>
                      </div>
                      <div className="flex items-start gap-2">
                        <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                        <div>
                          <p className="font-semibold text-white">100% Editable</p>
                          <p className="text-gray-400">Formato .docx para Word</p>
                        </div>
                      </div>
                      <div className="flex items-start gap-2">
                        <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                        <div>
                          <p className="font-semibold text-white">Logo Personalizado</p>
                          <p className="text-gray-400">Tu marca en cada página</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div>
                    <label className="block text-purple-400 font-semibold mb-2">Secciones a Incluir</label>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {['Resumen Ejecutivo', 'Análisis Técnico', 'Cronograma Detallado', 'Análisis Financiero', 'Riesgos y Mitigaciones', 'Recomendaciones'].map(seccion => (
                        <label key={seccion} className="flex items-center gap-2 bg-gray-900 p-3 rounded-lg cursor-pointer hover:bg-gray-800">
                          <input type="checkbox" defaultChecked className="w-4 h-4" />
                          <span className="text-sm">{seccion}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                </>
              )}

              <button 
                onClick={() => {
                  setAnalizando(true);
                  setTimeout(() => {
                    setAnalizando(false);
                    setExito(esEjecutivo ? '✅ Informe Ejecutivo generado en Word' : '✅ Informe Simple generado en PDF');
                    setTimeout(() => setExito(''), 3000);
                  }, 2000);
                }}
                disabled={analizando}
                className={`w-full ${esEjecutivo ? 'bg-gradient-to-r from-purple-600 via-purple-500 to-purple-600 hover:from-purple-500 hover:to-purple-400 border-purple-400' : 'bg-gradient-to-r from-green-600 via-green-500 to-green-600 hover:from-green-500 hover:to-green-400 border-green-400'} disabled:from-gray-800 disabled:to-gray-700 disabled:cursor-not-allowed py-4 rounded-xl font-bold text-lg text-white shadow-2xl border-2 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-3`}>
                {analizando ? (
                  <>
                    <Loader className="w-6 h-6 animate-spin" />
                    Generando informe...
                  </>
                ) : (
                  <>
                    <Download className="w-6 h-6" />
                    {esEjecutivo ? 'Generar Informe Ejecutivo (DOCX)' : 'Generar Informe Simple (PDF)'}
                  </>
                )}
              </button>
            </div>
          </div>

          {esEjecutivo && (
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-xl p-6 border border-purple-700">
              <h3 className="text-purple-400 font-bold mb-3">📋 Ejemplo de Estructura</h3>
              <div className="space-y-2 text-sm text-gray-300">
                <p>1. Portada con logo personalizado</p>
                <p>2. Índice automático</p>
                <p>3. Resumen Ejecutivo (1 página)</p>
                <p>4. Análisis Técnico con diagramas</p>
                <p>5. Tablas de costos profesionales</p>
                <p>6. Gráficos de distribución (generados con matplotlib)</p>
                <p>7. Cronograma con hitos</p>
                <p>8. Análisis financiero (ROI, VAN, TIR)</p>
                <p>9. Conclusiones y recomendaciones</p>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // ============================================
  // PANTALLA 5: COTIZACIÓN FINAL
  // ============================================
  if (pantallaActual === 'cotizacion-final' && cotizacion) {
    const itemsPorCapitulo = cotizacion.items.reduce((acc, item) => {
      const cap = item.capitulo || 'Sin clasificar';
      if (!acc[cap]) acc[cap] = [];
      acc[cap].push(item);
      return acc;
    }, {});

    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6">
        <div className="max-w-7xl mx-auto">
          <button onClick={volverAlInicio}
            className="fixed top-6 right-6 z-50 bg-gradient-to-r from-red-900 to-red-800 hover:from-red-800 hover:to-red-700 text-yellow-400 px-4 py-2 rounded-lg font-semibold flex items-center gap-2 shadow-2xl border-2 border-yellow-600 backdrop-blur-md transition-all duration-300 hover:scale-105">
            <Home className="w-5 h-5" />
            Inicio
          </button>

          <div className="bg-gradient-to-r from-red-950 via-red-900 to-black rounded-2xl p-8 mb-6 border-2 border-yellow-600 shadow-2xl backdrop-blur-md bg-opacity-90">
            <h1 className="text-4xl font-bold flex items-center gap-3 text-yellow-400">
              <FileCheck className="w-10 h-10" />
              Cotización Generada
            </h1>
            <p className="text-yellow-300 mt-2">Revisa y descarga tu cotización profesional</p>
          </div>

          {error && <Alerta tipo="error" mensaje={error} onClose={() => setError('')} />}
          {exito && <Alerta tipo="exito" mensaje={exito} onClose={() => setExito('')} />}

          <div className="bg-gradient-to-r from-yellow-900 to-yellow-800 border-2 border-yellow-500 rounded-2xl p-4 mb-6 backdrop-blur-md bg-opacity-90 shadow-2xl">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <h3 className="text-black font-bold text-lg">
                  {modoEdicion ? '✏️ MODO EDICIÓN' : '✅ VISTA FINAL'} v{versionCotizacion}
                </h3>
              </div>
              
              <div className="flex gap-3 flex-wrap">
                <button className="bg-blue-800 hover:bg-blue-700 text-white px-4 py-2 rounded-xl flex items-center gap-2 transition-all border-2 border-blue-600 shadow-xl">
                  <Download className="w-5 h-5" /> DOCX
                </button>
                
                <button className="bg-red-800 hover:bg-red-700 text-white px-4 py-2 rounded-xl flex items-center gap-2 transition-all border-2 border-red-600 shadow-xl">
                  <Download className="w-5 h-5" /> PDF
                </button>
                
                <button className="bg-green-800 hover:bg-green-700 text-white px-4 py-2 rounded-xl flex items-center gap-2 transition-all border-2 border-green-600 shadow-xl">
                  <Download className="w-5 h-5" /> HTML
                </button>

                <button 
                  onClick={() => setModoEdicion(!modoEdicion)}
                  className={`px-4 py-2 rounded-xl font-semibold flex items-center gap-2 transition-all border-2 shadow-xl ${
                    modoEdicion ? 'bg-green-800 hover:bg-green-700 border-green-600' : 'bg-blue-800 hover:bg-blue-700 border-blue-600'
                  } text-white`}>
                  {modoEdicion ? <><Save className="w-5 h-5" /> Finalizar</> : <><Edit className="w-5 h-5" /> Editar</>}
                </button>
              </div>
            </div>
          </div>

          <div className="bg-white text-gray-900 rounded-2xl p-8 shadow-2xl">
            <div className="border-b-4 border-red-900 pb-6 mb-6">
              <div className="flex justify-between">
                <div>
                  <h1 className="text-4xl font-bold text-red-900">{datosEmpresa.nombre}</h1>
                  <p className="text-gray-600 mt-2">RUC: {datosEmpresa.ruc}</p>
                  <p className="text-sm text-gray-500">{datosEmpresa.direccion}</p>
                  <p className="text-sm text-gray-500">{datosEmpresa.ciudad}</p>
                </div>
                <div className="text-right">
                  <div className="bg-gradient-to-r from-red-900 to-red-800 text-yellow-400 px-4 py-2 rounded-lg inline-block border-2 border-yellow-600">
                    <p className="text-sm font-bold">COTIZACIÓN</p>
                    <p className="text-2xl font-bold">v{versionCotizacion}</p>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">{new Date().toLocaleDateString('es-PE')}</p>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-6 mb-8">
              <div>
                <h3 className="font-bold text-red-900 mb-3">CLIENTE</h3>
                <p><b>Nombre:</b> {cotizacion.cliente.nombre}</p>
                <p><b>Proyecto:</b> {cotizacion.cliente.proyecto}</p>
                <p><b>Dirección:</b> {cotizacion.cliente.direccion}</p>
              </div>
              <div>
                <h3 className="font-bold text-red-900 mb-3">PROYECTO</h3>
                <p><b>Pisos:</b> {cotizacion.cliente.pisos}</p>
                <p><b>Departamentos:</b> {cotizacion.cliente.departamentos}</p>
              </div>
            </div>

            {Object.keys(itemsPorCapitulo).map(capitulo => (
              <div key={capitulo} className="mb-6">
                <h3 className="bg-gradient-to-r from-red-900 to-red-800 text-yellow-400 py-2 px-3 font-bold uppercase">{capitulo}</h3>
                <table className="w-full">
                  <thead>
                    <tr className="bg-gray-200">
                      <th className="text-left py-2 px-3 text-sm">DESCRIPCIÓN</th>
                      <th className="text-center py-2 px-3 text-sm">CANT.</th>
                      <th className="text-center py-2 px-3 text-sm">UND.</th>
                      {!ocultarPreciosUnitarios && <th className="text-right py-2 px-3 text-sm">P.U.</th>}
                      {!ocultarTotalesPorItem && <th className="text-right py-2 px-3 text-sm">TOTAL</th>}
                    </tr>
                  </thead>
                  <tbody>
                    {itemsPorCapitulo[capitulo].map((item, idx) => {
                      const subtotalItem = item.cantidad * item.precioUnitario;
                      return (
                        <tr key={idx} className={idx % 2 === 0 ? 'bg-gray-50' : ''}>
                          <td className="py-2 px-3 text-sm">
                            {item.descripcion}
                            {item.observacion && <span className="block text-xs text-gray-500 mt-1">{item.observacion}</span>}
                          </td>
                          <td className="text-center py-2 px-3">{item.cantidad}</td>
                          <td className="text-center py-2 px-3 text-sm">{item.unidad}</td>
                          {!ocultarPreciosUnitarios && (
                            <td className="text-right py-2 px-3">S/ {item.precioUnitario.toFixed(2)}</td>
                          )}
                          {!ocultarTotalesPorItem && (
                            <td className="text-right py-2 px-3 font-bold">S/ {subtotalItem.toFixed(2)}</td>
                          )}
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            ))}

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

            <div className="mt-8 pt-6 border-t-2 text-center text-sm text-gray-600">
              <p className="font-bold text-red-900">{datosEmpresa.nombre}</p>
              <p>📱 WhatsApp: {datosEmpresa.telefono}</p>
              <p>📧 {datosEmpresa.email}</p>
              <p>{datosEmpresa.direccion}</p>
              <p>{datosEmpresa.ciudad}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default CotizadorTesla30;