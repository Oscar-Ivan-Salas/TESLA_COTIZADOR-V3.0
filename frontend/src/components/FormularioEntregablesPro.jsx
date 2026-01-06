import React, { useState, useEffect, useRef } from 'react';
import { Package, Plus, X, Zap, Check } from 'lucide-react';

/**
 * FormularioEntregablesPro - Formulario PROFESIONAL con smart defaults
 * ✨ Features: Smart defaults + Keyboard shortcuts + Templates + Validación
 */
const FormularioEntregablesPro = ({
    onSubmit,
    tipoProyecto = 'residencial',
    presupuesto = 0,
    area = 0
}) => {

    // 🎯 TEMPLATES: Smart defaults por tipo de proyecto
    const TEMPLATES = {
        residencial: {
            nombre: 'Proyecto Residencial',
            entregables: ['diseno', 'suministro', 'instalacion', 'pruebas', 'documentacion'],
            descripcion: '5 entregables estándar'
        },
        industrial: {
            nombre: 'Proyecto Industrial',
            entregables: ['diseno', 'suministro', 'instalacion', 'scada', 'pruebas', 'documentacion', 'capacitacion'],
            descripcion: '7 entregables + SCADA'
        },
        comercial: {
            nombre: 'Proyecto Comercial',
            entregables: ['diseno', 'suministro', 'instalacion', 'pruebas', 'documentacion', 'capacitacion'],
            descripcion: '6 entregables + capacitación'
        }
    };

    const templateActual = TEMPLATES[tipoProyecto] || TEMPLATES.residencial;
    const defaultsActivos = templateActual.entregables;

    const [entregables, setEntregables] = useState({
        diseno: {
            checked: defaultsActivos.includes('diseno'),
            nombre: 'Diseño e ingeniería eléctrica completa',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        suministro: {
            checked: defaultsActivos.includes('suministro'),
            nombre: 'Suministro de materiales certificados',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        instalacion: {
            checked: defaultsActivos.includes('instalacion'),
            nombre: 'Instalación de sistema eléctrico',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        scada: {
            checked: defaultsActivos.includes('scada'),
            nombre: 'Sistema de automatización y control SCADA',
            cantidad: 1,
            unidad: 'glb',
            esencial: false
        },
        pruebas: {
            checked: defaultsActivos.includes('pruebas'),
            nombre: 'Pruebas FAT/SAT',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        documentacion: {
            checked: defaultsActivos.includes('documentacion'),
            nombre: 'Documentación técnica as-built',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        capacitacion: {
            checked: defaultsActivos.includes('capacitacion'),
            nombre: 'Capacitación al personal',
            cantidad: 1,
            unidad: 'sesión',
            esencial: false
        },
        garantia: {
            checked: defaultsActivos.includes('garantia'),
            nombre: 'Garantía',
            cantidad: 24,
            unidad: 'meses',
            esencial: false
        }
    });

    const [personalizados, setPersonalizados] = useState([]);
    const [nuevoEntregable, setNuevoEntregable] = useState('');
    const [focusedIndex, setFocusedIndex] = useState(0);
    const inputRef = useRef(null);

    // 🎯 BOTÓN: Seleccionar todos los comunes
    const seleccionarComunes = () => {
        setEntregables(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                if (nuevo[key].esencial) {
                    nuevo[key].checked = true;
                }
            });
            return nuevo;
        });
    };

    // 🎯 BOTÓN: Deseleccionar todos
    const deseleccionarTodos = () => {
        setEntregables(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                nuevo[key].checked = false;
            });
            return nuevo;
        });
    };

    // 🎯 BOTÓN: Aplicar template
    const aplicarTemplate = (tipo) => {
        const template = TEMPLATES[tipo];
        setEntregables(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                nuevo[key].checked = template.entregables.includes(key);
            });
            return nuevo;
        });
    };

    // ⌨️ KEYBOARD SHORTCUTS
    useEffect(() => {
        const handleKeyDown = (e) => {
            // Cmd/Ctrl + Enter: Submit
            if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
                e.preventDefault();
                handleSubmit();
            }

            // Cmd/Ctrl + A: Seleccionar comunes
            if ((e.metaKey || e.ctrlKey) && e.key === 'a') {
                e.preventDefault();
                seleccionarComunes();
            }

            // Cmd/Ctrl + D: Deseleccionar todos
            if ((e.metaKey || e.ctrlKey) && e.key === 'd') {
                e.preventDefault();
                deseleccionarTodos();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [entregables, personalizados]);

    const handleCheckChange = (key) => {
        setEntregables(prev => ({
            ...prev,
            [key]: { ...prev[key], checked: !prev[key].checked }
        }));
    };

    const handleCantidadChange = (key, valor) => {
        const num = parseInt(valor) || 0;
        if (num < 0 || num > 999) return; // Validación

        setEntregables(prev => ({
            ...prev,
            [key]: { ...prev[key], cantidad: num }
        }));
    };

    const agregarPersonalizado = () => {
        if (nuevoEntregable.trim()) {
            setPersonalizados(prev => [...prev, {
                id: Date.now(),
                nombre: nuevoEntregable.trim(),
                cantidad: 1,
                unidad: 'und',
                checked: true
            }]);
            setNuevoEntregable('');
            inputRef.current?.focus();
        }
    };

    const eliminarPersonalizado = (id) => {
        setPersonalizados(prev => prev.filter(e => e.id !== id));
    };

    const handleSubmit = () => {
        const seleccionados = Object.entries(entregables)
            .filter(([key, val]) => val.checked)
            .map(([key, val]) => ({
                nombre: val.nombre,
                cantidad: val.cantidad,
                unidad: val.unidad
            }));

        const todosEntregables = [
            ...seleccionados,
            ...personalizados.filter(e => e.checked)
        ];

        onSubmit(todosEntregables);
    };

    const totalSeleccionados = Object.values(entregables).filter(e => e.checked).length +
        personalizados.filter(e => e.checked).length;

    return (
        <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-2xl p-6 border-2 border-purple-200 shadow-lg">
            {/* Header con Template Info */}
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className="bg-purple-600 p-3 rounded-xl">
                        <Package className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h3 className="text-xl font-bold text-gray-800">📦 Entregables del Proyecto</h3>
                        <p className="text-sm text-gray-600">
                            Template: <span className="font-semibold text-purple-600">{templateActual.nombre}</span>
                            {' '}• {templateActual.descripcion}
                        </p>
                    </div>
                </div>
            </div>

            {/* Botones Rápidos */}
            <div className="flex flex-wrap gap-2 mb-6">
                <button
                    onClick={seleccionarComunes}
                    className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg transition-colors flex items-center gap-2"
                >
                    <Check className="w-4 h-4" />
                    ✓ Seleccionar Comunes
                    <span className="text-xs opacity-75">(Cmd+A)</span>
                </button>
                <button
                    onClick={deseleccionarTodos}
                    className="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
                >
                    Deseleccionar Todos
                    <span className="text-xs opacity-75 ml-2">(Cmd+D)</span>
                </button>

                {/* Templates Rápidos */}
                <div className="flex gap-2 ml-auto">
                    {Object.entries(TEMPLATES).map(([key, template]) => (
                        <button
                            key={key}
                            onClick={() => aplicarTemplate(key)}
                            className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${tipoProyecto === key
                                    ? 'bg-purple-600 text-white'
                                    : 'bg-white text-gray-700 hover:bg-purple-100'
                                }`}
                        >
                            {template.nombre}
                        </button>
                    ))}
                </div>
            </div>

            {/* Lista de entregables */}
            <div className="space-y-3 mb-6">
                {Object.entries(entregables).map(([key, item], index) => (
                    <div
                        key={key}
                        className={`flex items-center gap-3 p-4 rounded-xl border-2 transition-all cursor-pointer ${item.checked
                                ? 'bg-white border-purple-400 shadow-md'
                                : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                            }`}
                        onClick={() => handleCheckChange(key)}
                    >
                        <input
                            type="checkbox"
                            checked={item.checked}
                            onChange={() => { }} // Handled by div click
                            className="w-5 h-5 text-purple-600 rounded focus:ring-2 focus:ring-purple-500 pointer-events-none"
                        />
                        <div className="flex-1">
                            <span className={`font-medium ${item.checked ? 'text-gray-800' : 'text-gray-400'}`}>
                                {item.nombre}
                            </span>
                            {item.esencial && (
                                <span className="ml-2 text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                                    Esencial
                                </span>
                            )}
                        </div>
                        {item.checked && (
                            <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                                <input
                                    type="number"
                                    min="1"
                                    max="999"
                                    value={item.cantidad}
                                    onChange={(e) => handleCantidadChange(key, e.target.value)}
                                    className="w-20 px-3 py-2 border-2 border-purple-300 rounded-lg text-center font-bold focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                                />
                                <span className="text-sm text-gray-600 min-w-[60px]">{item.unidad}</span>
                            </div>
                        )}
                    </div>
                ))}

                {/* Entregables personalizados */}
                {personalizados.map((item) => (
                    <div
                        key={item.id}
                        className="flex items-center gap-3 p-4 rounded-xl border-2 bg-blue-50 border-blue-400 shadow-md"
                    >
                        <input
                            type="checkbox"
                            checked={item.checked}
                            onChange={() => {
                                setPersonalizados(prev => prev.map(e =>
                                    e.id === item.id ? { ...e, checked: !e.checked } : e
                                ));
                            }}
                            className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                        />
                        <span className="flex-1 font-medium text-gray-800">
                            {item.nombre}
                            <span className="ml-2 text-xs bg-blue-200 text-blue-700 px-2 py-1 rounded">
                                Personalizado
                            </span>
                        </span>
                        <div className="flex items-center gap-2">
                            <input
                                type="number"
                                min="1"
                                max="999"
                                value={item.cantidad}
                                onChange={(e) => {
                                    const num = parseInt(e.target.value) || 0;
                                    if (num >= 0 && num <= 999) {
                                        setPersonalizados(prev => prev.map(ent =>
                                            ent.id === item.id ? { ...ent, cantidad: num } : ent
                                        ));
                                    }
                                }}
                                className="w-20 px-3 py-2 border-2 border-blue-300 rounded-lg text-center font-bold focus:ring-2 focus:ring-blue-500"
                            />
                            <span className="text-sm text-gray-600 min-w-[60px]">{item.unidad}</span>
                            <button
                                onClick={() => eliminarPersonalizado(item.id)}
                                className="p-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {/* Agregar personalizado */}
            <div className="mb-6">
                <div className="flex gap-2">
                    <input
                        ref={inputRef}
                        type="text"
                        value={nuevoEntregable}
                        onChange={(e) => setNuevoEntregable(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && agregarPersonalizado()}
                        placeholder="Agregar entregable personalizado... (Enter para agregar)"
                        className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                    />
                    <button
                        onClick={agregarPersonalizado}
                        disabled={!nuevoEntregable.trim()}
                        className="px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition-colors flex items-center gap-2"
                    >
                        <Plus className="w-5 h-5" />
                        Agregar
                    </button>
                </div>
            </div>

            {/* Botón continuar */}
            <button
                onClick={handleSubmit}
                disabled={totalSeleccionados === 0}
                className="w-full py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-bold text-lg rounded-xl shadow-lg transition-all transform hover:scale-105 disabled:scale-100 flex items-center justify-center gap-2"
            >
                <Zap className="w-5 h-5" />
                ✅ Continuar con estos entregables
                <span className="text-sm opacity-75">(Cmd+Enter)</span>
            </button>

            {/* Resumen y Shortcuts */}
            <div className="mt-4 space-y-2">
                <div className="p-4 bg-white rounded-lg border-2 border-purple-200">
                    <p className="text-sm text-gray-600">
                        <span className="font-bold text-purple-600 text-lg">{totalSeleccionados}</span> entregables seleccionados
                    </p>
                </div>

                <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <p className="text-xs text-gray-600 font-mono">
                        💡 <span className="font-semibold">Shortcuts:</span>
                        {' '}Cmd+A (Seleccionar comunes) • Cmd+D (Deseleccionar) • Cmd+Enter (Continuar)
                    </p>
                </div>
            </div>
        </div>
    );
};

export default FormularioEntregablesPro;
