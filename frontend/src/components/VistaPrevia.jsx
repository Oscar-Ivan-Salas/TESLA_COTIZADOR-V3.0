import React, { useState, useRef, forwardRef, useImperativeHandle } from 'react';
import { Eye, EyeOff, Download, FileText, Calendar, User, Building, Edit, Calculator } from 'lucide-react';


const VistaPrevia = forwardRef(({ cotizacion, onGenerarDocumento, tipoDocumento = 'cotizacion', htmlPreview = '' }, ref) => {
  const [modoEdicion, setModoEdicion] = useState(false);
  const documentoRef = useRef(null);

  // Exponer métodos al componente padre
  useImperativeHandle(ref, () => ({
    getEditedHTML: () => {
      return documentoRef.current ? documentoRef.current.innerHTML : '';
    },
    isEditMode: () => modoEdicion
  }));

  // FASE 1: Estados específicos para COTIZACIONES
  const [ocultarPreciosUnitarios, setOcultarPreciosUnitarios] = useState(false);
  const [ocultarTotalesPorItem, setOcultarTotalesPorItem] = useState(false);
  const [modoVisualizacionIGV, setModoVisualizacionIGV] = useState('sin-igv'); // 'sin-igv' | 'con-igv' | 'ocultar-igv'

  const fechaActual = new Date().toLocaleDateString('es-PE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  const generarPDF = () => {
    onGenerarDocumento('pdf');
  };

  const generarWord = () => {
    onGenerarDocumento('word');
  };

  // Determinar título según tipo de documento
  const obtenerTituloDocumento = () => {
    if (tipoDocumento.includes('proyecto')) return 'PROYECTO';
    if (tipoDocumento.includes('informe')) return 'INFORME TÉCNICO';
    return 'COTIZACIÓN';
  };

  // FASE 1: Funciones de cálculo IGV para cotizaciones
  const calcularPrecioConIGV = (precio) => {
    const precioNum = parseFloat(precio || 0);
    if (modoVisualizacionIGV === 'con-igv') {
      return (precioNum * 1.18).toFixed(2);
    }
    return precioNum.toFixed(2);
  };

  const calcularTotalConIGV = (total) => {
    const totalNum = parseFloat(total || 0);
    if (modoVisualizacionIGV === 'con-igv') {
      return (totalNum * 1.18).toFixed(2);
    }
    return totalNum.toFixed(2);
  };

  return (
    <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-8 border-2 border-yellow-600">
      {/* Header */}
      <div className="flex items-center justify-between mb-8 pb-6 border-b-2 border-yellow-600">
        <div className="flex items-center gap-3">
          <Eye className="text-yellow-400" size={32} />
          <h2 className="text-3xl font-black text-yellow-400">
            Vista Previa
          </h2>
        </div>

        <div className="flex gap-3 flex-wrap">
          <button
            onClick={() => setModoEdicion(!modoEdicion)}
            className={`px-6 py-3 rounded-xl font-bold hover:scale-105 transition-all flex items-center gap-2 ${modoEdicion
              ? 'bg-gradient-to-r from-green-600 to-green-500 text-white'
              : 'bg-gradient-to-r from-gray-600 to-gray-500 text-white'
              }`}
          >
            <Edit size={20} />
            {modoEdicion ? 'Modo Edición ON' : 'Activar Edición'}
          </button>

          {/* FASE 1: Botones específicos para COTIZACIONES */}
          {tipoDocumento.includes('cotizacion') && (
            <>
              {/* Botón: Ocultar/Mostrar Precios Unitarios */}
              <button
                onClick={() => setOcultarPreciosUnitarios(!ocultarPreciosUnitarios)}
                className={`px-6 py-3 rounded-xl font-bold hover:scale-105 transition-all flex items-center gap-2 ${ocultarPreciosUnitarios
                  ? 'bg-gradient-to-r from-purple-600 to-purple-500 text-white'
                  : 'bg-gradient-to-r from-gray-600 to-gray-500 text-white'
                  }`}
                title={ocultarPreciosUnitarios ? 'Mostrar precios unitarios' : 'Ocultar precios unitarios'}
              >
                {ocultarPreciosUnitarios ? (
                  <>
                    <Eye size={20} />
                    Mostrar P.U.
                  </>
                ) : (
                  <>
                    <EyeOff size={20} />
                    Ocultar P.U.
                  </>
                )}
              </button>

              {/* Botón: Ocultar/Mostrar Totales por Ítem */}
              <button
                onClick={() => setOcultarTotalesPorItem(!ocultarTotalesPorItem)}
                className={`px-6 py-3 rounded-xl font-bold hover:scale-105 transition-all flex items-center gap-2 ${ocultarTotalesPorItem
                  ? 'bg-gradient-to-r from-indigo-600 to-indigo-500 text-white'
                  : 'bg-gradient-to-r from-gray-600 to-gray-500 text-white'
                  }`}
                title={ocultarTotalesPorItem ? 'Mostrar totales por ítem' : 'Ocultar totales por ítem'}
              >
                {ocultarTotalesPorItem ? (
                  <>
                    <Eye size={20} />
                    Mostrar Totales
                  </>
                ) : (
                  <>
                    <EyeOff size={20} />
                    Ocultar Totales
                  </>
                )}
              </button>

              {/* Dropdown: Modo Visualización IGV */}
              <div className="relative group">
                <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-xl font-bold hover:scale-105 transition-all flex items-center gap-2">
                  <Calculator size={20} />
                  Vista IGV
                </button>
                <div className="absolute top-full mt-2 right-0 bg-gray-900 border-2 border-blue-600 rounded-xl shadow-2xl hidden group-hover:block z-50 min-w-64">
                  <div className="p-2">
                    <button
                      onClick={() => setModoVisualizacionIGV('sin-igv')}
                      className={`w-full text-left px-4 py-2 rounded-lg mb-1 ${modoVisualizacionIGV === 'sin-igv' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-800'
                        }`}
                    >
                      📊 Precios SIN IGV (por defecto)
                    </button>
                    <button
                      onClick={() => setModoVisualizacionIGV('con-igv')}
                      className={`w-full text-left px-4 py-2 rounded-lg mb-1 ${modoVisualizacionIGV === 'con-igv' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-800'
                        }`}
                    >
                      💵 Precios CON IGV incluido
                    </button>
                    <button
                      onClick={() => setModoVisualizacionIGV('ocultar-igv')}
                      className={`w-full text-left px-4 py-2 rounded-lg ${modoVisualizacionIGV === 'ocultar-igv' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-800'
                        }`}
                    >
                      🔒 Ocultar desglose IGV
                    </button>
                  </div>
                </div>
              </div>
            </>
          )}

          <button
            onClick={generarPDF}
            className="bg-gradient-to-r from-red-600 to-red-500 text-white px-6 py-3 rounded-xl font-bold hover:scale-105 transition-all flex items-center gap-2"
          >
            <Download size={20} />
            Generar PDF
          </button>

          <button
            onClick={generarWord}
            className="bg-gradient-to-r from-blue-600 to-blue-500 text-white px-6 py-3 rounded-xl font-bold hover:scale-105 transition-all flex items-center gap-2"
          >
            <FileText size={20} />
            Generar Word
          </button>
        </div>
      </div>

      {/* Documento - Renderizar HTML del backend si existe, sino JSX */}
      {htmlPreview ? (
        <div
          ref={documentoRef}
          className="bg-white rounded-xl p-12 shadow-2xl text-black"
          contentEditable={modoEdicion}
          suppressContentEditableWarning={true}
          dangerouslySetInnerHTML={{ __html: htmlPreview }}
          style={{
            outline: modoEdicion ? '2px solid #10b981' : 'none',
            cursor: modoEdicion ? 'text' : 'default'
          }}
        />
      ) : (
        <div
          ref={documentoRef}
          className="bg-white rounded-xl p-12 shadow-2xl text-black"
          contentEditable={modoEdicion}
          suppressContentEditableWarning={true}
          style={{
            outline: modoEdicion ? '2px solid #10b981' : 'none',
            cursor: modoEdicion ? 'text' : 'default'
          }}
        >
          {/* Encabezado del documento */}
          <div className="text-center mb-8 pb-6 border-b-4 border-red-900">
            <h1 className="text-5xl font-black text-red-900 mb-2">
              {obtenerTituloDocumento()}
            </h1>
            <div className="flex items-center justify-center gap-2 text-gray-600">
              <Calendar size={18} />
              <p className="text-lg">{fechaActual}</p>
            </div>
          </div>

          {/* Información del cliente */}
          <div className="grid grid-cols-2 gap-8 mb-8">
            <div className="bg-gray-100 rounded-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <User className="text-red-900" size={24} />
                <h3 className="text-xl font-bold text-red-900">Cliente</h3>
              </div>
              <p className="text-2xl font-bold text-gray-800">
                {cotizacion.cliente || 'Sin especificar'}
              </p>
            </div>

            <div className="bg-gray-100 rounded-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Building className="text-red-900" size={24} />
                <h3 className="text-xl font-bold text-red-900">Proyecto</h3>
              </div>
              <p className="text-2xl font-bold text-gray-800">
                {cotizacion.proyecto || 'Sin especificar'}
              </p>
            </div>
          </div>

          {/* Tabla de items */}
          <div className="mb-8">
            <h3 className="text-2xl font-black text-red-900 mb-4">
              Detalle de Servicios
            </h3>

            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-red-900 text-white">
                  <th className="p-3 text-left border-2 border-red-800">Descripción</th>
                  <th className="p-3 text-center border-2 border-red-800 w-24">Cant.</th>
                  {!ocultarPreciosUnitarios && (
                    <th className="p-3 text-right border-2 border-red-800 w-32">P. Unit.</th>
                  )}
                  {!ocultarTotalesPorItem && (
                    <th className="p-3 text-right border-2 border-red-800 w-32">Total</th>
                  )}
                </tr>
              </thead>
              <tbody>
                {cotizacion.items && cotizacion.items.length > 0 ? (
                  cotizacion.items.map((item, index) => (
                    <tr key={item.id || index} className="border-b-2 border-gray-300 hover:bg-gray-50">
                      <td className="p-3 border-2 border-gray-300">{item.descripcion}</td>
                      <td className="p-3 text-center border-2 border-gray-300">{item.cantidad}</td>
                      {!ocultarPreciosUnitarios && (
                        <td className="p-3 text-right border-2 border-gray-300">
                          S/ {calcularPrecioConIGV(item.precioUnitario)}
                        </td>
                      )}
                      {!ocultarTotalesPorItem && (
                        <td className="p-3 text-right font-bold border-2 border-gray-300">
                          S/ {calcularTotalConIGV(item.total)}
                        </td>
                      )}
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td
                      colSpan={2 + (!ocultarPreciosUnitarios ? 1 : 0) + (!ocultarTotalesPorItem ? 1 : 0)}
                      className="p-8 text-center text-gray-500 italic"
                    >
                      No hay items en la cotización
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* Totales */}
          <div className="flex justify-end">
            <div className="w-1/2 space-y-4">
              {modoVisualizacionIGV !== 'ocultar-igv' && (
                <>
                  <div className="flex justify-between text-xl border-b-2 border-gray-300 pb-3">
                    <span className="font-semibold">Subtotal:</span>
                    <span className="font-bold">S/ {cotizacion.subtotal || '0.00'}</span>
                  </div>

                  <div className="flex justify-between text-xl border-b-2 border-gray-300 pb-3">
                    <span className="font-semibold">IGV (18%):</span>
                    <span className="font-bold">S/ {cotizacion.igv || '0.00'}</span>
                  </div>
                </>
              )}

              <div className="flex justify-between text-3xl bg-gradient-to-r from-red-900 to-red-800 text-white p-6 rounded-xl">
                <span className="font-black">TOTAL:</span>
                <span className="font-black">
                  S/ {modoVisualizacionIGV === 'con-igv'
                    ? (parseFloat(cotizacion.total || 0) * 1.18).toFixed(2)
                    : (cotizacion.total || '0.00')}
                </span>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-12 pt-6 border-t-2 border-gray-300 text-center text-gray-600">
            <p className="font-bold text-red-900 text-xl mb-2">TESLA COTIZADOR PRO</p>
            <p>📱 WhatsApp: +51 999 888 777</p>
            <p>📧 ventas@teslacotizador.com</p>
            <p>📍 Lima, Perú</p>
          </div>
        </div>
      )}

      {/* Información adicional */}
      <div className="mt-6 bg-yellow-900/20 border-2 border-yellow-600 rounded-xl p-6">
        <div className="flex items-start gap-3">
          <div className="bg-yellow-600 rounded-full p-2 mt-1">
            <FileText className="text-black" size={20} />
          </div>
          <div>
            <h4 className="text-yellow-400 font-bold text-lg mb-2">
              Formatos disponibles
            </h4>
            <ul className="text-gray-300 space-y-1">
              <li>• <strong>PDF:</strong> Para envío profesional al cliente</li>
              <li>• <strong>Word:</strong> Para edición y personalización posterior</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
});

export default VistaPrevia;