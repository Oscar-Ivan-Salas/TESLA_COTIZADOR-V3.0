import React, { useState, useEffect } from 'react';
import { Search, Plus, Building, X, Users } from 'lucide-react';

/**
 * Componente para seleccionar cliente con autocompletado
 * Permite buscar clientes existentes o crear uno nuevo
 */
const ClienteSelector = ({ onClienteSeleccionado, clienteInicial = null }) => {
  const [busqueda, setBusqueda] = useState('');
  const [clientes, setClientes] = useState([]);
  const [buscando, setBuscando] = useState(false);
  const [mostrarNuevo, setMostrarNuevo] = useState(false);
  const [clienteSeleccionado, setClienteSeleccionado] = useState(clienteInicial);
  const [error, setError] = useState('');

  // Autocompletado - buscar mientras escribe
  useEffect(() => {
    if (busqueda.length >= 2) {
      setBuscando(true);
      setError('');

      const timer = setTimeout(async () => {
        try {
          const response = await fetch(
            `http://localhost:8000/api/clientes/search?q=${encodeURIComponent(busqueda)}`
          );

          if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
          }

          const data = await response.json();
          setClientes(data);
        } catch (err) {
          console.error('Error buscando clientes:', err);
          setError('Error al buscar clientes');
          setClientes([]);
        } finally {
          setBuscando(false);
        }
      }, 300); // Debounce de 300ms

      return () => clearTimeout(timer);
    } else {
      setClientes([]);
    }
  }, [busqueda]);

  const seleccionarCliente = (cliente) => {
    setClienteSeleccionado(cliente);
    onClienteSeleccionado(cliente);
    setBusqueda('');
    setClientes([]);
  };

  const limpiarSeleccion = () => {
    setClienteSeleccionado(null);
    onClienteSeleccionado(null);
    setBusqueda('');
  };

  // Si ya hay un cliente seleccionado, mostrar card
  if (clienteSeleccionado) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <Building className="w-5 h-5 text-green-600" />
              <h3 className="font-bold text-lg">{clienteSeleccionado.nombre}</h3>
            </div>
            <p className="text-sm text-gray-600">RUC: {clienteSeleccionado.ruc}</p>
            {clienteSeleccionado.direccion && (
              <p className="text-sm text-gray-600">📍 {clienteSeleccionado.direccion}</p>
            )}
            {clienteSeleccionado.email && (
              <p className="text-sm text-gray-600">📧 {clienteSeleccionado.email}</p>
            )}
            {clienteSeleccionado.telefono && (
              <p className="text-sm text-gray-600">📞 {clienteSeleccionado.telefono}</p>
            )}
            {clienteSeleccionado.total_cotizaciones > 0 && (
              <p className="text-xs text-blue-600 mt-2">
                📄 {clienteSeleccionado.total_cotizaciones} cotización(es) previa(s)
              </p>
            )}
          </div>
          <button
            onClick={limpiarSeleccion}
            className="text-gray-500 hover:text-red-600 transition-colors"
            title="Cambiar cliente"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <button
          onClick={limpiarSeleccion}
          className="mt-3 text-sm text-blue-600 hover:underline"
        >
          🔄 Cambiar cliente
        </button>
      </div>
    );
  }

  // Formulario de búsqueda/selección
  return (
    <div className="border-2 border-yellow-600 rounded-lg p-4 bg-gradient-to-br from-gray-900 to-gray-800">
      <h3 className="font-semibold mb-3 flex items-center gap-2 text-yellow-400">
        <Users className="w-5 h-5 text-yellow-400" />
        Seleccionar Cliente
      </h3>

      {/* Búsqueda */}
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
          placeholder="Buscar por nombre o RUC..."
          className="w-full pl-10 pr-4 py-2 bg-gray-800 border-2 border-gray-700 text-white rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
        />
      </div>

      {/* Estado de búsqueda */}
      {buscando && (
        <div className="text-center py-4 text-gray-300">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-500"></div>
          <p className="mt-2 text-sm">Buscando...</p>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-900 border border-red-700 text-red-200 p-3 rounded-lg mb-4">
          {error}
        </div>
      )}

      {/* Resultados de búsqueda */}
      {!buscando && clientes.length > 0 && (
        <div className="space-y-2 mb-4 max-h-60 overflow-y-auto">
          {clientes.map((cliente) => (
            <div
              key={cliente.id}
              onClick={() => seleccionarCliente(cliente)}
              className="p-3 border-2 border-gray-700 bg-gray-800 rounded-lg cursor-pointer hover:bg-gradient-to-r hover:from-yellow-900 hover:to-red-900 hover:border-yellow-600 transition-all"
            >
              <div className="font-semibold text-yellow-400">{cliente.nombre}</div>
              <div className="text-sm text-gray-300">RUC: {cliente.ruc}</div>
              {cliente.industria && (
                <div className="text-xs text-gray-400 mt-1">
                  🏢 {cliente.industria}
                </div>
              )}
              {cliente.total_cotizaciones > 0 && (
                <div className="text-xs text-yellow-500 mt-1">
                  📄 {cliente.total_cotizaciones} cotización(es) previa(s)
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Sin resultados */}
      {!buscando && busqueda.length >= 2 && clientes.length === 0 && !error && (
        <div className="text-center py-4 text-gray-400">
          <p>No se encontraron clientes</p>
          <p className="text-sm mt-1">Intenta con otro término o registra un nuevo cliente</p>
        </div>
      )}

      {/* Botón para nuevo cliente */}
      <button
        onClick={() => setMostrarNuevo(true)}
        className="w-full bg-gradient-to-r from-yellow-600 to-yellow-500 text-black font-bold py-2 px-4 rounded-lg hover:from-yellow-500 hover:to-yellow-400 flex items-center justify-center gap-2 transition-all shadow-lg"
      >
        <Plus className="w-5 h-5" />
        Registrar Nuevo Cliente
      </button>

      {/* Modal para nuevo cliente (se importará) */}
      {mostrarNuevo && (
        <ModalNuevoCliente
          onCancelar={() => setMostrarNuevo(false)}
          onGuardar={(nuevoCliente) => {
            seleccionarCliente(nuevoCliente);
            setMostrarNuevo(false);
          }}
        />
      )}
    </div>
  );
};

/**
 * Modal para registrar nuevo cliente
 * Componente inline para evitar imports circulares
 */
const ModalNuevoCliente = ({ onCancelar, onGuardar }) => {
  const [datos, setDatos] = useState({
    nombre: '',
    ruc: '',
    direccion: '',
    ciudad: '',
    telefono: '',
    email: '',
    industria: '',
    contacto_nombre: '',
    notas: ''
  });
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setGuardando(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/clientes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al guardar cliente');
      }

      const nuevoCliente = await response.json();
      onGuardar(nuevoCliente);
    } catch (err) {
      setError(err.message);
    } finally {
      setGuardando(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 p-4">
      <div className="bg-gradient-to-br from-gray-900 via-red-950 to-black border-2 border-yellow-600 rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <h2 className="text-2xl font-bold mb-4 flex items-center gap-2 text-yellow-400">
          <Users className="w-6 h-6 text-yellow-400" />
          Registrar Nuevo Cliente
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            {/* Nombre */}
            <div className="col-span-2">
              <label className="block font-semibold mb-1 text-yellow-400">
                Nombre/Razón Social *
              </label>
              <input
                type="text"
                required
                value={datos.nombre}
                onChange={(e) => setDatos({ ...datos, nombre: e.target.value })}
                className="w-full bg-gray-800 border-2 border-gray-700 text-white rounded px-3 py-2 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                placeholder="Ej: ACME Corporation SAC"
              />
            </div>

            {/* RUC */}
            <div>
              <label className="block font-semibold mb-1 text-yellow-400">RUC *</label>
              <input
                type="text"
                required
                pattern="[0-9]{11}"
                value={datos.ruc}
                onChange={(e) => setDatos({ ...datos, ruc: e.target.value })}
                className="w-full bg-gray-800 border-2 border-gray-700 text-white rounded px-3 py-2 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                placeholder="20123456789"
                maxLength="11"
              />
              <p className="text-xs text-gray-400 mt-1">11 dígitos numéricos</p>
            </div>

            {/* Teléfono */}
            <div>
              <label className="block font-semibold mb-1 text-yellow-400">Teléfono</label>
              <input
                type="text"
                value={datos.telefono}
                onChange={(e) => setDatos({ ...datos, telefono: e.target.value })}
                className="w-full bg-gray-800 border-2 border-gray-700 text-white rounded px-3 py-2 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                placeholder="999888777"
              />
            </div>

            {/* Dirección */}
            <div className="col-span-2">
              <label className="block font-semibold mb-1 text-yellow-400">Dirección</label>
              <input
                type="text"
                value={datos.direccion}
                onChange={(e) => setDatos({ ...datos, direccion: e.target.value })}
                className="w-full bg-gray-800 border-2 border-gray-700 text-white rounded px-3 py-2 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                placeholder="Av. Lima 123, San Isidro"
              />
            </div>

            {/* Ciudad */}
            <div>
              <label className="block font-semibold mb-1 text-yellow-400">Ciudad</label>
              <input
                type="text"
                value={datos.ciudad}
                onChange={(e) => setDatos({ ...datos, ciudad: e.target.value })}
                className="w-full bg-gray-800 border-2 border-gray-700 text-white rounded px-3 py-2 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                placeholder="Lima, Perú"
              />
            </div>

            {/* Email */}
            <div>
              <label className="block font-semibold mb-1 text-yellow-400">Email</label>
              <input
                type="email"
                value={datos.email}
                onChange={(e) => setDatos({ ...datos, email: e.target.value })}
                className="w-full bg-gray-800 border-2 border-gray-700 text-white rounded px-3 py-2 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                placeholder="contacto@cliente.com"
              />
            </div>

            {/* Industria */}
            <div>
              <label className="block font-semibold mb-1 text-yellow-400">Industria</label>
              <select
                value={datos.industria}
                onChange={(e) => setDatos({ ...datos, industria: e.target.value })}
                className="w-full bg-gray-800 border-2 border-gray-700 text-white rounded px-3 py-2 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
              >
                <option value="">Seleccionar...</option>
                <option value="construccion">Construcción</option>
                <option value="mineria">Minería</option>
                <option value="industrial">Industrial</option>
                <option value="comercial">Comercial</option>
                <option value="educacion">Educación</option>
                <option value="salud">Salud</option>
                <option value="retail">Retail</option>
                <option value="residencial">Residencial</option>
              </select>
            </div>

            {/* Contacto */}
            <div>
              <label className="block font-semibold mb-1 text-yellow-400">Persona de Contacto</label>
              <input
                type="text"
                value={datos.contacto_nombre}
                onChange={(e) => setDatos({ ...datos, contacto_nombre: e.target.value })}
                className="w-full bg-gray-800 border-2 border-gray-700 text-white rounded px-3 py-2 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                placeholder="Juan Pérez"
              />
            </div>

            {/* Notas */}
            <div className="col-span-2">
              <label className="block font-semibold mb-1 text-yellow-400">Notas (opcional)</label>
              <textarea
                value={datos.notas}
                onChange={(e) => setDatos({ ...datos, notas: e.target.value })}
                className="w-full bg-gray-800 border-2 border-gray-700 text-white rounded px-3 py-2 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                rows="2"
                placeholder="Información adicional sobre el cliente..."
              />
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="bg-red-900 border border-red-700 text-red-200 p-3 rounded">
              ❌ {error}
            </div>
          )}

          {/* Botones */}
          <div className="flex gap-3 pt-4 border-t-2 border-gray-700">
            <button
              type="button"
              onClick={onCancelar}
              className="flex-1 border-2 border-gray-600 text-gray-300 py-2 px-4 rounded-lg hover:bg-gray-800 transition-colors"
              disabled={guardando}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={guardando}
              className="flex-1 bg-gradient-to-r from-yellow-600 to-yellow-500 text-black font-bold py-2 px-4 rounded-lg hover:from-yellow-500 hover:to-yellow-400 disabled:opacity-50 transition-all shadow-lg"
            >
              {guardando ? '💾 Guardando...' : '💾 Guardar y Continuar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ClienteSelector;
