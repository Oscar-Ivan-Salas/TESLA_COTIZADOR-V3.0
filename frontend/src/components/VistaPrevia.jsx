import React from 'react';
import { Eye, Download, FileText, Calendar, User, Building } from 'lucide-react';

const VistaPrevia = ({ cotizacion, onGenerarDocumento }) => {
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
        
        <div className="flex gap-3">
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

      {/* Documento simulado */}
      <div className="bg-white rounded-xl p-12 shadow-2xl text-black">
        {/* Encabezado del documento */}
        <div className="text-center mb-8 pb-6 border-b-4 border-red-900">
          <h1 className="text-5xl font-black text-red-900 mb-2">
            COTIZACIÓN
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
                <th className="p-3 text-right border-2 border-red-800 w-32">P. Unit.</th>
                <th className="p-3 text-right border-2 border-red-800 w-32">Total</th>
              </tr>
            </thead>
            <tbody>
              {cotizacion.items && cotizacion.items.length > 0 ? (
                cotizacion.items.map((item, index) => (
                  <tr key={item.id || index} className="border-b-2 border-gray-300 hover:bg-gray-50">
                    <td className="p-3 border-2 border-gray-300">{item.descripcion}</td>
                    <td className="p-3 text-center border-2 border-gray-300">{item.cantidad}</td>
                    <td className="p-3 text-right border-2 border-gray-300">
                      S/ {parseFloat(item.precioUnitario || 0).toFixed(2)}
                    </td>
                    <td className="p-3 text-right font-bold border-2 border-gray-300">
                      S/ {parseFloat(item.total || 0).toFixed(2)}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="p-8 text-center text-gray-500 italic">
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
            <div className="flex justify-between text-xl border-b-2 border-gray-300 pb-3">
              <span className="font-semibold">Subtotal:</span>
              <span className="font-bold">S/ {cotizacion.subtotal || '0.00'}</span>
            </div>
            
            <div className="flex justify-between text-xl border-b-2 border-gray-300 pb-3">
              <span className="font-semibold">IGV (18%):</span>
              <span className="font-bold">S/ {cotizacion.igv || '0.00'}</span>
            </div>
            
            <div className="flex justify-between text-3xl bg-gradient-to-r from-red-900 to-red-800 text-white p-6 rounded-xl">
              <span className="font-black">TOTAL:</span>
              <span className="font-black">S/ {cotizacion.total || '0.00'}</span>
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
};

export default VistaPrevia;