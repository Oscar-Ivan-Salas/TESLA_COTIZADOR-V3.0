import React, { useState, useRef, forwardRef, useImperativeHandle } from 'react';
import { Eye, EyeOff, Download, FileText, Edit, Save } from 'lucide-react';

// ✅ IMPORTAR COMPONENTE EDITABLE (PILOTO: COTIZACION_COMPLEJA)
import EDITABLE_COTIZACION_COMPLEJA from './EDITABLE_COTIZACION_COMPLEJA';

/**
 * VistaPrevia - Componente profesional con estilos de plantilla HTML
 * Mantiene funcionalidad editable + diseño profesional aprobado
 */
const VistaPreviaProfesional = forwardRef((props) => {
  const {
    cotizacion,
    proyecto,
    informe,
    onGenerarDocumento,
    tipoDocumento = 'cotizacion',
    htmlPreview = '',
    // Nuevos props para personalización
    esquemaColores = 'azul-tesla',
    logoBase64 = null,  // Cambiado de logoUrl a logoBase64
    fuenteDocumento = 'Calibri'
  } = props;

  // Estados principales
  const [modoEdicion, setModoEdicion] = useState(true);
  const [ocultarPreciosUnitarios, setOcultarPreciosUnitarios] = useState(false);
  const [ocultarTotalesPorItem, setOcultarTotalesPorItem] = useState(false);
  const [modoVisualizacionIGV, setModoVisualizacionIGV] = useState('sin-igv');

  // Estado editable de la cotización
  const [cotizacionEditable, setCotizacionEditable] = useState(cotizacion || proyecto || informe || {});

  // ✅ NUEVO: Callback para cuando cambian los datos en componente EDITABLE
  const handleDatosChange = (nuevosDatos) => {
    setCotizacionEditable(nuevosDatos);
    // Opcional: Notificar al componente padre si existe callback
    if (props.onCotizacionChange) {
      props.onCotizacionChange(nuevosDatos);
    }
  };

  const documentoRef = useRef(null);

  // Exponer métodos al componente padre
  useImperativeHandle(props.ref, () => ({
    getEditedHTML: () => {
      return documentoRef.current ? documentoRef.current.innerHTML : '';
    },
    isEditMode: () => modoEdicion,
    getEditedData: () => cotizacionEditable // ✅ Retorna datos del componente EDITABLE
  }));

  // Función para actualizar items (inline editing)
  const actualizarItem = (index, campo, valor) => {
    const nuevosItems = [...cotizacionEditable.items];
    nuevosItems[index][campo] = campo === 'descripcion' || campo === 'unidad'
      ? valor
      : parseFloat(valor) || 0;

    setCotizacionEditable({
      ...cotizacionEditable,
      items: nuevosItems
    });
  };

  // Calcular totales
  const calcularTotales = () => {
    const subtotal = cotizacionEditable.items?.reduce((sum, item) =>
      sum + (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || item.precioUnitario || 0)), 0
    ) || 0;
    const igv = subtotal * 0.18;
    const total = subtotal + igv;

    return {
      subtotal: subtotal.toFixed(2),
      igv: igv.toFixed(2),
      total: total.toFixed(2)
    };
  };

  const totales = calcularTotales();

  // Función para obtener título según tipo de documento
  const getTituloDocumento = () => {
    const titulos = {
      'cotizacion-simple': 'COTIZACIÓN DE SERVICIOS',
      'cotizacion-compleja': 'COTIZACIÓN DE SERVICIOS',
      'cotizacion': 'COTIZACIÓN DE SERVICIOS',
      'proyecto-simple': 'PROYECTO DE SERVICIOS',
      'proyecto-complejo': 'PLAN DE PROYECTO PMI',
      'proyecto': 'PROYECTO DE SERVICIOS',
      'informe-tecnico': 'INFORME TÉCNICO',
      'informe-ejecutivo': 'INFORME EJECUTIVO',
      'informe': 'INFORME TÉCNICO'
    };
    return titulos[tipoDocumento] || 'DOCUMENTO';
  };

  // Esquemas de colores profesionales
  const ESQUEMAS_COLORES = {
    'azul-tesla': {
      primario: '#0052A3',
      secundario: '#1E40AF',
      acento: '#3B82F6',
      claro: '#EFF6FF',
      claroBorde: '#DBEAFE'
    },
    'rojo-energia': {
      primario: '#8B0000',
      secundario: '#991B1B',
      acento: '#DC2626',
      claro: '#FEE2E2',
      claroBorde: '#FECACA'
    },
    'verde-ecologico': {
      primario: '#065F46',
      secundario: '#047857',
      acento: '#10B981',
      claro: '#D1FAE5',
      claroBorde: '#A7F3D0'
    },
    'dorado': {
      primario: '#D4AF37',
      secundario: '#B8860B',
      acento: '#FFD700',
      claro: '#FEF3C7',
      claroBorde: '#FDE68A'
    },
    'personalizado': {
      primario: '#9333EA',  // Morado/Lila
      secundario: '#7E22CE',  // Morado oscuro
      acento: '#A855F7',  // Morado claro
      claro: '#F3E8FF',  // Morado muy claro
      claroBorde: '#E9D5FF'  // Morado claro borde
    }
  };

  const colores = ESQUEMAS_COLORES[esquemaColores] || ESQUEMAS_COLORES['azul-tesla'];

  // Estilos profesionales dinámicos
  const estilosProfesionales = `
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    .cotizacion-profesional {
      font-family: '${fuenteDocumento}', 'Arial', sans-serif;
      color: #1f2937;
      line-height: 1.6;
      background: #ffffff;
      max-width: 210mm;
      margin: 0 auto;
      padding: 20mm;
    }

    /* Colores dinámicos */
    .color-primario { color: ${colores.primario} !important; }
    .color-secundario { color: ${colores.secundario} !important; }
    .color-acento { color: ${colores.acento} !important; }
    .bg-primario { background-color: ${colores.primario} !important; }
    .bg-secundario { background-color: ${colores.secundario} !important; }
    .bg-acento { background-color: ${colores.acento} !important; }
    .bg-claro { background-color: ${colores.claro} !important; }

    /* Cabecera */
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 30px;
      padding-bottom: 20px;
      border-bottom: 4px solid ${colores.primario};
    }

    .logo-section {
      width: 35%;
    }

    .logo-placeholder {
      width: 180px;
      height: 80px;
      background: linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: bold;
      font-size: 24px;
      margin-bottom: 10px;
      overflow: hidden;
    }

    .logo-placeholder img {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }

    .empresa-info {
      width: 65%;
      text-align: right;
    }

    .empresa-nombre {
      font-size: 20px;
      font-weight: bold;
      color: ${colores.primario};
      margin-bottom: 8px;
      text-transform: uppercase;
    }

    .empresa-detalles {
      font-size: 11px;
      color: #4b5563;
      line-height: 1.5;
    }

    /* Título documento */
    .titulo-documento {
      text-align: center;
      margin: 30px 0;
      padding: 20px;
      background: linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%);
      border-left: 6px solid ${colores.primario};
      border-radius: 4px;
    }

    .titulo-documento h1 {
      font-size: 28px;
      color: ${colores.primario};
      font-weight: bold;
      margin-bottom: 8px;
    }

    .numero-cotizacion {
      font-size: 16px;
      color: ${colores.secundario};
      font-weight: 600;
      background: transparent;
      border: none;
      text-align: center;
      width: 100%;
    }

    /* Sección información */
    .info-section {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin: 25px 0;
    }

    .info-box {
      padding: 15px;
      border: 2px solid ${colores.claroBorde};
      border-radius: 6px;
      background: #F9FAFB;
    }

    .info-box h3 {
      font-size: 14px;
      color: ${colores.primario};
      font-weight: bold;
      margin-bottom: 10px;
      text-transform: uppercase;
      border-bottom: 2px solid ${colores.primario};
      padding-bottom: 5px;
    }

    .info-box p {
      font-size: 12px;
      color: #374151;
      margin: 5px 0;
    }

    .info-label {
      font-weight: 600;
      color: ${colores.secundario};
      display: inline-block;
      min-width: 100px;
    }

    /* Tabla de items */
    .tabla-section {
      margin: 30px 0;
    }

    .tabla-section h2 {
      font-size: 18px;
      color: ${colores.primario};
      margin-bottom: 15px;
      padding-bottom: 8px;
      border-bottom: 3px solid ${colores.primario};
    }

    .tabla-items {
      width: 100%;
      border-collapse: collapse;
      margin: 15px 0;
      box-shadow: 0 2px 8px rgba(0, 82, 163, 0.1);
    }

    .tabla-items thead {
      background: linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%);
      color: white;
    }

    .tabla-items thead th {
      padding: 14px 10px;
      text-align: left;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .tabla-items thead th:last-child,
    .tabla-items thead th:nth-child(3),
    .tabla-items thead th:nth-child(4),
    .tabla-items thead th:nth-child(5) {
      text-align: right;
    }

    .tabla-items tbody tr {
      border-bottom: 1px solid #E5E7EB;
    }

    .tabla-items tbody tr:hover {
      background-color: ${colores.claro};
    }

    .tabla-items tbody tr:nth-child(even) {
      background-color: #F9FAFB;
    }

    .tabla-items tbody td {
      padding: 12px 10px;
      font-size: 11px;
      color: #374151;
    }

    .tabla-items tbody td:last-child,
    .tabla-items tbody td:nth-child(3),
    .tabla-items tbody td:nth-child(4),
    .tabla-items tbody td:nth-child(5) {
      text-align: right;
      font-weight: 600;
    }

    .tabla-items input {
      width: 100%;
      background: transparent;
      border: 1px solid transparent;
      padding: 4px;
      font-size: 11px;
      color: #374151;
    }

    .tabla-items input:focus {
      border-color: ${colores.acento};
      outline: none;
      background: white;
    }

    /* Totales */
    .totales-section {
      margin-top: 25px;
      display: flex;
      justify-content: flex-end;
    }

    .totales-box {
      width: 350px;
      border: 2px solid ${colores.primario};
      border-radius: 6px;
      overflow: hidden;
    }

    .totales-row {
      display: flex;
      justify-content: space-between;
      padding: 12px 20px;
      border-bottom: 1px solid ${colores.claroBorde};
    }

    .totales-row:last-child {
      border-bottom: none;
      background: linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%);
      color: white;
      font-weight: bold;
      font-size: 16px;
    }

    .totales-label {
      font-weight: 600;
      color: ${colores.secundario};
    }

    .totales-row:last-child .totales-label {
      color: white;
    }

    .totales-valor {
      font-weight: 700;
      color: ${colores.primario};
    }

    .totales-row:last-child .totales-valor {
      color: white;
    }

    /* Observaciones */
    .observaciones {
      margin: 30px 0;
      padding: 20px;
      background: #F9FAFB;
      border-left: 4px solid ${colores.acento};
      border-radius: 4px;
    }

    .observaciones h3 {
      font-size: 14px;
      color: ${colores.primario};
      font-weight: bold;
      margin-bottom: 12px;
      text-transform: uppercase;
    }

    .observaciones ul {
      list-style: none;
      padding: 0;
    }

    .observaciones li {
      font-size: 11px;
      color: #374151;
      margin: 8px 0;
      padding-left: 20px;
      position: relative;
    }

    .observaciones li:before {
      content: "✓";
      position: absolute;
      left: 0;
      color: ${colores.primario};
      font-weight: bold;
    }

    /* Pie de página */
    .footer {
      margin-top: 40px;
      padding-top: 20px;
      border-top: 3px solid ${colores.primario};
      text-align: center;
      font-size: 10px;
      color: #6B7280;
    }

    .footer-empresa {
      font-weight: bold;
      color: ${colores.primario};
      font-size: 12px;
      margin-bottom: 8px;
    }

    .footer-contacto {
      margin: 5px 0;
    }

    /* Panel de control (no se imprime) */
    @media print {
      .panel-control {
        display: none !important;
      }
    }

    .panel-control {
      background: linear-gradient(to right, #fbbf24, #f59e0b);
      border: 2px solid #d97706;
      border-radius: 16px;
      padding: 16px;
      margin-bottom: 24px;
    }

    .panel-control h3 {
      color: black;
      font-weight: bold;
      font-size: 18px;
      margin-bottom: 12px;
    }

    .panel-control button {
      padding: 8px 16px;
      border-radius: 8px;
      font-weight: 600;
      transition: all 0.3s;
      cursor: pointer;
    }
  `;

  // ✅ NUEVA FUNCIÓN: Renderizar componente EDITABLE según tipo de documento
  const renderDocumentoEditable = () => {
    // PILOTO: Para COTIZACION_COMPLEJA y COTIZACION genérica
    if (tipoDocumento === 'cotizacion-compleja' || tipoDocumento === 'cotizacion') {
      return (
        <EDITABLE_COTIZACION_COMPLEJA
          datos={cotizacionEditable}
          esquemaColores={esquemaColores}
          logoBase64={logoBase64}
          fuenteDocumento={fuenteDocumento}
          onDatosChange={handleDatosChange}
        />
      );
    }

    // Para otros tipos, retornar null para usar renderizado inline existente
    return null;
  };

  return (
    <div>
      {/* Inyectar estilos profesionales */}
      <style>{estilosProfesionales}</style>

      {/* PANEL DE CONTROL - NO SE IMPRIME */}
      <div className="panel-control">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <h3 style={{ margin: 0 }}>
            {modoEdicion ? '✏️ MODO EDICIÓN' : '✅ VISTA FINAL'}
          </h3>
          <button
            onClick={() => setModoEdicion(!modoEdicion)}
            style={{
              background: modoEdicion ? '#10b981' : '#3b82f6',
              color: 'white',
              border: 'none'
            }}
          >
            {modoEdicion ? <><Save size={16} /> Finalizar</> : <><Edit size={16} /> Editar</>}
          </button>
        </div>

        {/* Opciones de visualización */}
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <button
            onClick={() => setOcultarPreciosUnitarios(!ocultarPreciosUnitarios)}
            style={{
              background: ocultarPreciosUnitarios ? '#8b5cf6' : '#6b7280',
              color: 'white',
              border: 'none',
              fontSize: '12px'
            }}
          >
            {ocultarPreciosUnitarios ? '👁️ Mostrar P.U.' : '🚫 Ocultar P.U.'}
          </button>

          <button
            onClick={() => setOcultarTotalesPorItem(!ocultarTotalesPorItem)}
            style={{
              background: ocultarTotalesPorItem ? '#6366f1' : '#6b7280',
              color: 'white',
              border: 'none',
              fontSize: '12px'
            }}
          >
            {ocultarTotalesPorItem ? '👁️ Mostrar Totales' : '💎 Solo Total Final'}
          </button>

          {!modoEdicion && (
            <button
              onClick={() => onGenerarDocumento && onGenerarDocumento('word')}
              style={{
                background: '#059669',
                color: 'white',
                border: 'none'
              }}
            >
              <FileText size={16} /> Generar Word
            </button>
          )}
        </div>
      </div>

      {/* DOCUMENTO PROFESIONAL */}
      <div className="cotizacion-profesional" ref={documentoRef}>
        {/* ✅ RENDERIZAR COMPONENTE EDITABLE SI APLICA (PILOTO: COTIZACION_COMPLEJA) */}
        {renderDocumentoEditable() || (
          <>
            {/* CABECERA */}
            <div className="header">
              <div className="logo-section">
                <div className="logo-placeholder">
                  {logoBase64 ? (
                    <img src={logoBase64} alt="Logo empresa" />
                  ) : (
                    'TESLA'
                  )}
                </div>
                <p style={{ fontSize: '10px', color: '#6B7280' }}>Electricidad y Automatización</p>
              </div>

              <div className="empresa-info">
                <div className="empresa-nombre">
                  TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
                </div>
                <div className="empresa-detalles">
                  <div>RUC: 20601138787</div>
                  <div>Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div>
                  <div>Teléfono: 906 315 961</div>
                  <div>Email: ingenieria.teslaelectricidad@gmail.com</div>
                </div>
              </div>
            </div>

            {/* TÍTULO DOCUMENTO */}
            <div className="titulo-documento">
              <h1>{getTituloDocumento()}</h1>
              <input
                type="text"
                className="numero-cotizacion"
                value={cotizacionEditable.numero || 'COT-2025-001'}
                onChange={(e) => setCotizacionEditable({ ...cotizacionEditable, numero: e.target.value })}
                disabled={!modoEdicion}
              />
            </div>

            {/* CONTENIDO DINÁMICO SEGÚN TIPO DE DOCUMENTO */}
            {(tipoDocumento.includes('cotizacion')) ? (
              <>
                {/* INFORMACIÓN GENERAL - COTIZACIÓN */}
                <div className="info-section">
                  <div className="info-box">
                    <h3>Datos del Cliente</h3>
                    <p><span className="info-label">Cliente:</span> {typeof cotizacionEditable.cliente === 'object' ? cotizacionEditable.cliente?.nombre : cotizacionEditable.cliente || 'Cliente'}</p>
                    <p><span className="info-label">Proyecto:</span> {cotizacionEditable.proyecto || 'Proyecto'}</p>
                    <p><span className="info-label">Área:</span> {cotizacionEditable.area_m2 || '0'} m²</p>
                  </div>

                  <div className="info-box">
                    <h3>Datos de la Cotización</h3>
                    <p><span className="info-label">Fecha:</span> {cotizacionEditable.fecha || new Date().toLocaleDateString('es-PE')}</p>
                    <p><span className="info-label">Vigencia:</span> {cotizacionEditable.vigencia || '30 días'}</p>
                    <p><span className="info-label">Servicio:</span> {cotizacionEditable.servicio || 'Instalaciones Eléctricas'}</p>
                  </div>
                </div>

                {/* TABLA DE ITEMS - COTIZACIÓN */}
                <div className="tabla-section">
                  <h2>Detalle de la Cotización</h2>

                  <table className="tabla-items">
                    <thead>
                      <tr>
                        <th style={{ width: '8%' }}>ITEM</th>
                        <th style={{ width: '42%' }}>DESCRIPCIÓN</th>
                        <th style={{ width: '10%' }}>CANT.</th>
                        <th style={{ width: '10%' }}>UNIDAD</th>
                        {!ocultarPreciosUnitarios && <th style={{ width: '15%' }}>P. UNIT.</th>}
                        {!ocultarTotalesPorItem && <th style={{ width: '15%' }}>TOTAL</th>}
                      </tr>
                    </thead>
                    <tbody>
                      {cotizacionEditable.items?.map((item, index) => {
                        const subtotalItem = (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || item.precioUnitario || 0));

                        return (
                          <tr key={index}>
                            <td style={{ textAlign: 'center' }}>{String(index + 1).padStart(2, '0')}</td>
                            <td>
                              {modoEdicion ? (
                                <input
                                  type="text"
                                  value={item.descripcion || ''}
                                  onChange={(e) => actualizarItem(index, 'descripcion', e.target.value)}
                                />
                              ) : (
                                item.descripcion
                              )}
                            </td>
                            <td style={{ textAlign: 'right' }}>
                              {modoEdicion ? (
                                <input
                                  type="number"
                                  value={item.cantidad || 0}
                                  onChange={(e) => actualizarItem(index, 'cantidad', e.target.value)}
                                  style={{ textAlign: 'right' }}
                                />
                              ) : (
                                parseFloat(item.cantidad || 0).toFixed(2)
                              )}
                            </td>
                            <td style={{ textAlign: 'center' }}>
                              {modoEdicion ? (
                                <input
                                  type="text"
                                  value={item.unidad || 'und'}
                                  onChange={(e) => actualizarItem(index, 'unidad', e.target.value)}
                                  style={{ textAlign: 'center' }}
                                />
                              ) : (
                                item.unidad || 'und'
                              )}
                            </td>
                            {!ocultarPreciosUnitarios && (
                              <td style={{ textAlign: 'right' }}>
                                {modoEdicion ? (
                                  <input
                                    type="number"
                                    value={item.precio_unitario || item.precioUnitario || 0}
                                    onChange={(e) => actualizarItem(index, 'precio_unitario', e.target.value)}
                                    style={{ textAlign: 'right' }}
                                  />
                                ) : (
                                  `S/ ${parseFloat(item.precio_unitario || item.precioUnitario || 0).toFixed(2)}`
                                )}
                              </td>
                            )}
                            {!ocultarTotalesPorItem && (
                              <td style={{ textAlign: 'right', fontWeight: 'bold' }}>
                                S/ {subtotalItem.toFixed(2)}
                              </td>
                            )}
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>

                {/* TOTALES - COTIZACIÓN */}
                <div className="totales-section">
                  <div className="totales-box">
                    <div className="totales-row">
                      <span className="totales-label">SUBTOTAL:</span>
                      <span className="totales-valor">S/ {totales.subtotal}</span>
                    </div>
                    <div className="totales-row">
                      <span className="totales-label">IGV (18%):</span>
                      <span className="totales-valor">S/ {totales.igv}</span>
                    </div>
                    <div className="totales-row">
                      <span className="totales-label">TOTAL:</span>
                      <span className="totales-valor">S/ {totales.total}</span>
                    </div>
                  </div>
                </div>

                {/* OBSERVACIONES - COTIZACIÓN */}
                <div className="observaciones">
                  <h3>Observaciones Técnicas</h3>
                  <ul>
                    <li>Trabajos ejecutados según CNE - Código Nacional de Electricidad</li>
                    <li>Materiales de primera calidad con certificación</li>
                    <li>Mano de obra especializada</li>
                    <li>Garantía de 12 meses en mano de obra</li>
                    <li>Precios en soles peruanos (PEN)</li>
                    <li>Forma de pago: 50% adelanto, 50% contra entrega</li>
                    <li>Cotización válida por {cotizacionEditable.vigencia || '30 días'}</li>
                  </ul>
                </div>
              </>
            ) : tipoDocumento.includes('informe') ? (
              <>
                {/* CONTENIDO PARA INFORME TÉCNICO/EJECUTIVO */}
                <div className="resumen-ejecutivo" style={{
                  padding: '25px',
                  background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`,
                  borderLeft: `6px solid ${colores.primario}`,
                  borderRadius: '4px',
                  margin: '30px 0'
                }}>
                  <h3 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', textTransform: 'uppercase' }}>
                    Resumen Ejecutivo
                  </h3>
                  {modoEdicion ? (
                    <textarea
                      value={cotizacionEditable.resumen_ejecutivo || 'Resumen del informe...'}
                      onChange={(e) => setCotizacionEditable({ ...cotizacionEditable, resumen_ejecutivo: e.target.value })}
                      className="input-editable"
                      style={{ width: '100%', minHeight: '100px', fontSize: '13px', lineHeight: '1.8' }}
                    />
                  ) : (
                    <p style={{ fontSize: '13px', color: '#374151', lineHeight: '1.8', textAlign: 'justify' }}>
                      {cotizacionEditable.resumen_ejecutivo || 'Resumen del informe...'}
                    </p>
                  )}
                </div>

                {/* INTRODUCCIÓN */}
                <div className="seccion" style={{ margin: '35px 0' }}>
                  <h2 style={{
                    fontSize: '20px',
                    color: colores.primario,
                    marginBottom: '20px',
                    paddingBottom: '10px',
                    borderBottom: `3px solid ${colores.primario}`
                  }}>
                    1. INTRODUCCIÓN
                  </h2>
                  {modoEdicion ? (
                    <textarea
                      value={cotizacionEditable.introduccion || 'Introducción del informe...'}
                      onChange={(e) => setCotizacionEditable({ ...cotizacionEditable, introduccion: e.target.value })}
                      className="input-editable"
                      style={{ width: '100%', minHeight: '150px', fontSize: '12px', lineHeight: '1.8' }}
                    />
                  ) : (
                    <p style={{ fontSize: '12px', color: '#374151', lineHeight: '1.8', textAlign: 'justify' }}>
                      {cotizacionEditable.introduccion || 'Introducción del informe...'}
                    </p>
                  )}
                </div>

                {/* ANÁLISIS TÉCNICO */}
                <div className="seccion" style={{ margin: '35px 0' }}>
                  <h2 style={{
                    fontSize: '20px',
                    color: colores.primario,
                    marginBottom: '20px',
                    paddingBottom: '10px',
                    borderBottom: `3px solid ${colores.primario}`
                  }}>
                    2. ANÁLISIS TÉCNICO
                  </h2>
                  {modoEdicion ? (
                    <textarea
                      value={cotizacionEditable.analisis_tecnico || 'Análisis técnico detallado...'}
                      onChange={(e) => setCotizacionEditable({ ...cotizacionEditable, analisis_tecnico: e.target.value })}
                      className="input-editable"
                      style={{ width: '100%', minHeight: '200px', fontSize: '12px', lineHeight: '1.8' }}
                    />
                  ) : (
                    <p style={{ fontSize: '12px', color: '#374151', lineHeight: '1.8', textAlign: 'justify' }}>
                      {cotizacionEditable.analisis_tecnico || 'Análisis técnico detallado...'}
                    </p>
                  )}
                </div>

                {/* CONCLUSIONES */}
                <div className="conclusiones" style={{ margin: '30px 0' }}>
                  <div style={{
                    padding: '25px',
                    background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`,
                    borderLeft: `6px solid ${colores.primario}`,
                    borderRadius: '4px'
                  }}>
                    <h3 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px' }}>
                      CONCLUSIONES
                    </h3>
                    {modoEdicion ? (
                      <textarea
                        value={cotizacionEditable.conclusiones || 'Conclusiones del informe...'}
                        onChange={(e) => setCotizacionEditable({ ...cotizacionEditable, conclusiones: e.target.value })}
                        className="input-editable"
                        style={{ width: '100%', minHeight: '150px', fontSize: '12px', lineHeight: '1.6' }}
                      />
                    ) : (
                      <p style={{ fontSize: '12px', color: '#374151', lineHeight: '1.6' }}>
                        {cotizacionEditable.conclusiones || 'Conclusiones del informe...'}
                      </p>
                    )}
                  </div>
                </div>
              </>
            ) : tipoDocumento.includes('proyecto') ? (
              <>
                {/* CONTENIDO PARA PROYECTO SIMPLE/COMPLEJO */}
                <div className="resumen-ejecutivo" style={{
                  padding: '25px',
                  background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`,
                  borderLeft: `6px solid ${colores.primario}`,
                  borderRadius: '4px',
                  margin: '30px 0'
                }}>
                  <h3 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', textTransform: 'uppercase' }}>
                    Resumen del Proyecto
                  </h3>
                  {modoEdicion ? (
                    <textarea
                      value={cotizacionEditable.resumen || 'Resumen del proyecto...'}
                      onChange={(e) => setCotizacionEditable({ ...cotizacionEditable, resumen: e.target.value })}
                      className="input-editable"
                      style={{ width: '100%', minHeight: '100px', fontSize: '13px', lineHeight: '1.8' }}
                    />
                  ) : (
                    <p style={{ fontSize: '13px', color: '#374151', lineHeight: '1.8', textAlign: 'justify' }}>
                      {cotizacionEditable.resumen || 'Resumen del proyecto...'}
                    </p>
                  )}
                </div>

                {/* FASES DEL PROYECTO */}
                <div className="seccion" style={{ margin: '35px 0' }}>
                  <h2 style={{
                    fontSize: '20px',
                    color: colores.primario,
                    marginBottom: '20px',
                    paddingBottom: '10px',
                    borderBottom: `3px solid ${colores.primario}`
                  }}>
                    FASES DEL PROYECTO
                  </h2>
                  <p style={{ fontSize: '12px', color: '#374151', lineHeight: '1.8', marginBottom: '20px' }}>
                    El proyecto se desarrollará en las siguientes fases principales:
                  </p>
                  <ul style={{ listStyle: 'none', padding: 0 }}>
                    {(cotizacionEditable.fases || [{ descripcion: 'Fase 1', duracion: '1 semana', responsable: 'Por asignar' }]).map((fase, index) => (
                      <li key={index} style={{
                        fontSize: '12px',
                        color: '#374151',
                        margin: '12px 0',
                        paddingLeft: '30px',
                        position: 'relative',
                        lineHeight: '1.6'
                      }}>
                        <span style={{
                          position: 'absolute',
                          left: '10px',
                          color: colores.primario,
                          fontSize: '16px'
                        }}>●</span>
                        <strong>Fase {index + 1}:</strong> {fase.descripcion} - Duración: {fase.duracion} - Responsable: {fase.responsable}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* CRONOGRAMA */}
                <div className="seccion" style={{ margin: '35px 0' }}>
                  <h2 style={{
                    fontSize: '20px',
                    color: colores.primario,
                    marginBottom: '20px',
                    paddingBottom: '10px',
                    borderBottom: `3px solid ${colores.primario}`
                  }}>
                    CRONOGRAMA
                  </h2>
                  <div style={{ padding: '20px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, borderRadius: '4px' }}>
                    <p style={{ fontSize: '12px', marginBottom: '10px' }}>
                      <strong>Fecha de Inicio:</strong> {cotizacionEditable.cronograma?.fecha_inicio || '01/01/2025'}
                    </p>
                    <p style={{ fontSize: '12px', marginBottom: '10px' }}>
                      <strong>Fecha de Fin:</strong> {cotizacionEditable.cronograma?.fecha_fin || '31/12/2025'}
                    </p>
                    <p style={{ fontSize: '12px' }}>
                      <strong>Duración Total:</strong> {cotizacionEditable.cronograma?.duracion_total || '12 meses'}
                    </p>
                  </div>
                </div>
              </>
            ) : null}

            {/* PIE DE PÁGINA */}
            <div className="footer">
              <div className="footer-empresa">TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
              <div className="footer-contacto">RUC: 20601138787 | Teléfono: 906 315 961</div>
              <div className="footer-contacto">Email: ingenieria.teslaelectricidad@gmail.com</div>
              <div className="footer-contacto">Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div>
            </div>
          </>
        )}
      </div>
    </div>
  );
});

VistaPreviaProfesional.displayName = 'VistaPreviaProfesional';

export default VistaPreviaProfesional;
