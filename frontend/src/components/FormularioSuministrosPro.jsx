import React, { useState, useEffect, useRef } from 'react';
import { Wrench, Plus, X, Zap, Check, Calculator } from 'lucide-react';

/**
 * FormularioSuministrosPro - Formulario PROFESIONAL para suministros eléctricos
 * ✨ Features: Cantidades calculadas por área + Smart defaults + Keyboard shortcuts
 */
const FormularioSuministrosPro = ({
    onSubmit,
    tipoProyecto = 'residencial',
    presupuesto = 0,
    area = 0
}) => {

    // 🎯 CÁLCULO INTELIGENTE: Cantidades basadas en área del proyecto
    const calcularCantidad = (item, areaM2) => {
        if (!areaM2 || areaM2 <= 0) return 0;

        const calculos = {
            tableros: Math.ceil(areaM2 / 200),      // 1 tablero cada 200m²
            cables: Math.ceil(areaM2 * 2.5),        // 2.5m de cable por m²
            protecciones: Math.ceil(areaM2 / 50),   // 1 protección cada 50m²
            puesta_tierra: 1,                        // Siempre 1 sistema
            luminarias: Math.ceil(areaM2 / 10),     // 1 luminaria cada 10m²
            transformador: Math.ceil(areaM2 / 1000), // 1 transformador cada 1000m²
            ups: Math.ceil(areaM2 / 500),           // 1 UPS cada 500m²
            generador: Math.ceil(areaM2 / 2000),    // 1 generador cada 2000m²
            conduit: Math.ceil(areaM2 * 1.5),       // 1.5m de conduit por m²
            bandejas: Math.ceil(areaM2 * 0.8)       // 0.8m de bandeja por m²
        };

        return calculos[item] || 1;
    };

    // 🎯 TEMPLATES: Suministros por tipo de proyecto
    const TEMPLATES = {
        residencial: {
            nombre: 'Suministros Residencial',
            suministros: ['tableros', 'cables', 'protecciones', 'puesta_tierra', 'luminarias'],
            descripcion: '5 suministros básicos'
        },
        industrial: {
            nombre: 'Suministros Industrial',
            suministros: ['tableros', 'cables', 'protecciones', 'puesta_tierra', 'luminarias', 'transformador', 'ups', 'generador', 'conduit', 'bandejas'],
            descripcion: '10 suministros completos'
        },
        comercial: {
            nombre: 'Suministros Comercial',
            suministros: ['tableros', 'cables', 'protecciones', 'puesta_tierra', 'luminarias', 'ups', 'conduit', 'bandejas'],
            descripcion: '8 suministros + UPS'
        }
    };

    const templateActual = TEMPLATES[tipoProyecto] || TEMPLATES.residencial;
    const suministrosDefault = templateActual.suministros;

    const [suministros, setSuministros] = useState({
        tableros: {
            checked: suministrosDefault.includes('tableros'),
            nombre: 'Tableros eléctricos certificados',
            cantidad: area > 0 ? calcularCantidad('tableros', area) : 5,
            unidad: 'und',
            esencial: true
        },
        cables: {
            checked: suministrosDefault.includes('cables'),
            nombre: 'Cables THW/THHN',
            cantidad: area > 0 ? calcularCantidad('cables', area) : 500,
            unidad: 'm',
            esencial: true
        },
        protecciones: {
            checked: suministrosDefault.includes('protecciones'),
            nombre: 'Protecciones termomagnéticas',
            cantidad: area > 0 ? calcularCantidad('protecciones', area) : 20,
            unidad: 'und',
            esencial: true
        },
        puesta_tierra: {
            checked: suministrosDefault.includes('puesta_tierra'),
            nombre: 'Sistema de puesta a tierra',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        luminarias: {
            checked: suministrosDefault.includes('luminarias'),
            nombre: 'Luminarias LED',
            cantidad: area > 0 ? calcularCantidad('luminarias', area) : 50,
            unidad: 'und',
            esencial: true
        },
        transformador: {
            checked: suministrosDefault.includes('transformador'),
            nombre: 'Transformador',
            cantidad: area > 0 ? calcularCantidad('transformador', area) : 1,
            unidad: 'und',
            esencial: false
        },
        ups: {
            checked: suministrosDefault.includes('ups'),
            nombre: 'UPS',
            cantidad: area > 0 ? calcularCantidad('ups', area) : 2,
            unidad: 'und',
            esencial: false
        },
        generador: {
            checked: suministrosDefault.includes('generador'),
            nombre: 'Generador eléctrico',
            cantidad: area > 0 ? calcularCantidad('generador', area) : 1,
            unidad: 'und',
            esencial: false
        },
        conduit: {
            checked: suministrosDefault.includes('conduit'),
            nombre: 'Tubería conduit',
            cantidad: area > 0 ? calcularCantidad('conduit', area) : 200,
            unidad: 'm',
            esencial: false
        },
        bandejas: {
            checked: suministrosDefault.includes('bandejas'),
            nombre: 'Bandejas portacables',
            cantidad: area > 0 ? calcularCantidad('bandejas', area) : 100,
            unidad: 'm',
            esencial: false
        }
    });

    const [personalizados, setPersonalizados] = useState([]);
    const [nuevoSuministro, setNuevoSuministro] = useState('');
    const inputRef = useRef(null);

    // 🎯 BOTÓN: Seleccionar esenciales
    const seleccionarEsenciales = () => {
        setSuministros(prev => {
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
        setSuministros(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                nuevo[key].checked = false;
            });
            return nuevo;
        });
    };

    // 🎯 BOTÓN: Recalcular cantidades
    const recalcularCantidades = () => {
        if (area <= 0) return;

        setSuministros(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                const cantidadCalculada = calcularCantidad(key, area);
                if (cantidadCalculada > 0) {
                    nuevo[key].cantidad = cantidadCalculada;
                }
            });
            return nuevo;
        });
    };

    // 🎯 BOTÓN: Aplicar template
    const aplicarTemplate = (tipo) => {
        const template = TEMPLATES[tipo];
        setSuministros(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                nuevo[key].checked = template.suministros.includes(key);
            });
            return nuevo;
        });
    };

    // ⌨️ KEYBOARD SHORTCUTS
    useEffect(() => {
        const handleKeyDown = (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
                e.preventDefault();
                handleSubmit();
            }
            if ((e.metaKey || e.ctrlKey) && e.key === 'a') {
                e.preventDefault();
                seleccionarEsenciales();
            }
            if ((e.metaKey || e.ctrlKey) && e.key === 'd') {
                e.preventDefault();
                deseleccionarTodos();
            }
            if ((e.metaKey || e.ctrlKey) && e.key === 'r') {
                e.preventDefault();
                recalcularCantidades();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [suministros, personalizados, area]);

    const handleCheckChange = (key) => {
        setSuministros(prev => ({
            ...prev,
            [key]: { ...prev[key], checked: !prev[key].checked }
        }));
    };

    const handleCantidadChange = (key, valor) => {
        const num = parseInt(valor) || 0;
        if (num < 0 || num > 9999) return;

        setSuministros(prev => ({
            ...prev,
            [key]: { ...prev[key], cantidad: num }
        }));
    };

    const agregarPersonalizado = () => {
        if (nuevoSuministro.trim()) {
            setPersonalizados(prev => [...prev, {
                id: Date.now(),
                nombre: nuevoSuministro.trim(),
                cantidad: 1,
                unidad: 'und',
                checked: true
            }]);
            setNuevoSuministro('');
            inputRef.current?.focus();
        }
    };

    const eliminarPersonalizado = (id) => {
        setPersonalizados(prev => prev.filter(s => s.id !== id));
    };

    const handleSubmit = () => {
        const seleccionados = Object.entries(suministros)
            .filter(([key, val]) => val.checked)
            .map(([key, val]) => ({
                nombre: val.nombre,
                cantidad: val.cantidad,
                unidad: val.unidad
            }));

        const todosSuministros = [
            ...seleccionados,
            ...personalizados.filter(s => s.checked)
        ];

        onSubmit(todosSuministros);
    };

    const totalSeleccionados = Object.values(suministros).filter(s => s.checked).length +
        personalizados.filter(s => s.checked).length;

    return (
        <div className="bg-gradient-to-br from-orange-50 to-yellow-50 rounded-2xl p-6 border-2 border-orange-200 shadow-lg">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className="bg-orange-600 p-3 rounded-xl">
                        <Wrench className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h3 className="text-xl font-bold text-gray-800">🔧 Suministros Eléctricos</h3>
                        <p className="text-sm text-gray-600">
                            Template: <span className="font-semibold text-orange-600">{templateActual.nombre}</span>
                            {' '}• {templateActual.descripcion}
                            {area > 0 && <span className="ml-2 text-blue-600">• Área: {area}m²</span>}
                        </p>
                    </div>
                </div>
            </div>

            {/* Botones Rápidos */}
            <div className="flex flex-wrap gap-2 mb-6">
                <button
                    onClick={seleccionarEsenciales}
                    className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg transition-colors flex items-center gap-2"
                >
                    <Check className="w-4 h-4" />
                    ✓ Seleccionar Esenciales
                    <span className="text-xs opacity-75">(Cmd+A)</span>
                </button>
                <button
                    onClick={deseleccionarTodos}
                    className="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
                >
                    Deseleccionar Todos
                    <span className="text-xs opacity-75 ml-2">(Cmd+D)</span>
                </button>
                {area > 0 && (
                    <button
                        onClick={recalcularCantidades}
                        className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition-colors flex items-center gap-2"
                    >
                        <Calculator className="w-4 h-4" />
                        Recalcular por Área
                        <span className="text-xs opacity-75">(Cmd+R)</span>
                    </button>
                )}

                {/* Templates */}
                <div className="flex gap-2 ml-auto">
                    {Object.entries(TEMPLATES).map(([key, template]) => (
                        <button
                            key={key}
                            onClick={() => aplicarTemplate(key)}
                            className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${tipoProyecto === key
                                    ? 'bg-orange-600 text-white'
                                    : 'bg-white text-gray-700 hover:bg-orange-100'
                                }`}
                        >
                            {template.nombre}
                        </button>
                    ))}
                </div>
            </div>

            {/* Lista de suministros */}
            <div className="space-y-3 mb-6 max-h-[500px] overflow-y-auto pr-2">
                {Object.entries(suministros).map(([key, item]) => (
                    <div
                        key={key}
                        className={`flex items-center gap-3 p-4 rounded-xl border-2 transition-all cursor-pointer ${item.checked
                                ? 'bg-white border-orange-400 shadow-md'
                                : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                            }`}
                        onClick={() => handleCheckChange(key)}
                    >
                        <input
                            type="checkbox"
                            checked={item.checked}
                            onChange={() => { }}
                            className="w-5 h-5 text-orange-600 rounded focus:ring-2 focus:ring-orange-500 pointer-events-none"
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
                                    max="9999"
                                    value={item.cantidad}
                                    onChange={(e) => handleCantidadChange(key, e.target.value)}
                                    className="w-24 px-3 py-2 border-2 border-orange-300 rounded-lg text-center font-bold focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                                />
                                <span className="text-sm text-gray-600 min-w-[50px]">{item.unidad}</span>
                            </div>
                        )}
                    </div>
                ))}

                {/* Suministros personalizados */}
                {personalizados.map((item) => (
                    <div
                        key={item.id}
                        className="flex items-center gap-3 p-4 rounded-xl border-2 bg-yellow-50 border-yellow-400 shadow-md"
                    >
                        <input
                            type="checkbox"
                            checked={item.checked}
                            onChange={() => {
                                setPersonalizados(prev => prev.map(s =>
                                    s.id === item.id ? { ...s, checked: !s.checked } : s
                                ));
                            }}
                            className="w-5 h-5 text-yellow-600 rounded focus:ring-2 focus:ring-yellow-500"
                        />
                        <span className="flex-1 font-medium text-gray-800">
                            {item.nombre}
                            <span className="ml-2 text-xs bg-yellow-200 text-yellow-700 px-2 py-1 rounded">
                                Personalizado
                            </span>
                        </span>
                        <div className="flex items-center gap-2">
                            <input
                                type="number"
                                min="1"
                                max="9999"
                                value={item.cantidad}
                                onChange={(e) => {
                                    const num = parseInt(e.target.value) || 0;
                                    if (num >= 0 && num <= 9999) {
                                        setPersonalizados(prev => prev.map(s =>
                                            s.id === item.id ? { ...s, cantidad: num } : s
                                        ));
                                    }
                                }}
                                className="w-24 px-3 py-2 border-2 border-yellow-300 rounded-lg text-center font-bold focus:ring-2 focus:ring-yellow-500"
                            />
                            <span className="text-sm text-gray-600 min-w-[50px]">{item.unidad}</span>
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
                        value={nuevoSuministro}
                        onChange={(e) => setNuevoSuministro(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && agregarPersonalizado()}
                        placeholder="Agregar suministro personalizado... (Enter para agregar)"
                        className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    />
                    <button
                        onClick={agregarPersonalizado}
                        disabled={!nuevoSuministro.trim()}
                        className="px-6 py-3 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition-colors flex items-center gap-2"
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
                className="w-full py-4 bg-gradient-to-r from-orange-600 to-yellow-600 hover:from-orange-700 hover:to-yellow-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-bold text-lg rounded-xl shadow-lg transition-all transform hover:scale-105 disabled:scale-100 flex items-center justify-center gap-2"
            >
                <Zap className="w-5 h-5" />
                ✅ Continuar con estos suministros
                <span className="text-sm opacity-75">(Cmd+Enter)</span>
            </button>

            {/* Resumen */}
            <div className="mt-4 space-y-2">
                <div className="p-4 bg-white rounded-lg border-2 border-orange-200">
                    <p className="text-sm text-gray-600">
                        <span className="font-bold text-orange-600 text-lg">{totalSeleccionados}</span> tipos de suministros seleccionados
                    </p>
                </div>

                <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                    <p className="text-xs text-gray-600 font-mono">
                        💡 <span className="font-semibold">Shortcuts:</span>
                        {' '}Cmd+A (Esenciales) • Cmd+D (Deseleccionar) • Cmd+R (Recalcular) • Cmd+Enter (Continuar)
                    </p>
                </div>
            </div>
        </div>
    );
};

export default FormularioSuministrosPro;
