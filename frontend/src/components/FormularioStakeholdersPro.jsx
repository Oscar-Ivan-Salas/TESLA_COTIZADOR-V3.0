import React, { useState, useEffect } from 'react';
import { Users, Plus, Trash2, Save, UserCheck, Activity, Target } from 'lucide-react';

const FormularioStakeholdersPro = ({ onSubmit, valoresIniciales = [] }) => {
    const [stakeholders, setStakeholders] = useState([
        { id: 1, nombre: 'Cliente', rol: 'Patrocinador Principal', poder: 'Alto', interes: 'Alto' },
        { id: 2, nombre: 'Jefe de Proyecto', rol: 'Responsable de Ejecución', poder: 'Alto', interes: 'Alto' },
        { id: 3, nombre: 'Equipo Técnico', rol: 'Ejecutores', poder: 'Medio', interes: 'Alto' }
    ]);

    useEffect(() => {
        if (valoresIniciales && valoresIniciales.length > 0) {
            setStakeholders(valoresIniciales.map((s, i) => ({ ...s, id: i + 1 })));
        }
    }, [valoresIniciales]);

    const addStakeholder = () => {
        const newId = stakeholders.length > 0 ? Math.max(...stakeholders.map(s => s.id)) + 1 : 1;
        setStakeholders([...stakeholders, {
            id: newId,
            nombre: '',
            rol: '',
            poder: 'Medio',
            interes: 'Medio'
        }]);
    };

    const updateStakeholder = (id, field, value) => {
        setStakeholders(stakeholders.map(s =>
            s.id === id ? { ...s, [field]: value } : s
        ));
    };

    const removeStakeholder = (id) => {
        setStakeholders(stakeholders.filter(s => s.id !== id));
    };

    const handleSubmit = () => {
        // Validar que no haya campos vacíos importantes
        const validos = stakeholders.filter(s => s.nombre.trim() && s.rol.trim());
        if (validos.length === 0) return;
        onSubmit(validos);
    };

    const getNivelColor = (nivel) => {
        switch (nivel) {
            case 'Alto': return 'bg-red-500/20 text-red-400 border-red-500/30';
            case 'Medio': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
            case 'Bajo': return 'bg-green-500/20 text-green-400 border-green-500/30';
            default: return 'bg-gray-700 text-gray-400';
        }
    };

    return (
        <div className="bg-gray-900/95 p-6 rounded-2xl border border-purple-500/30 shadow-2xl w-full max-w-3xl animate-fadeIn backdrop-blur-xl">
            <div className="flex items-center gap-3 mb-6 border-b border-purple-500/20 pb-4">
                <div className="p-2 bg-purple-500/20 rounded-lg">
                    <Users className="w-6 h-6 text-purple-400" />
                </div>
                <div>
                    <h3 className="text-xl font-bold text-white">Registro de Stakeholders</h3>
                    <p className="text-xs text-purple-300">Identificación y Análisis de Interesados</p>
                </div>
            </div>

            <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar mb-6">
                {stakeholders.map((stk) => (
                    <div key={stk.id} className="bg-gray-800/50 p-4 rounded-xl border border-gray-700 hover:border-purple-500/30 transition-all group">
                        <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">

                            {/* Nombre y Rol */}
                            <div className="md:col-span-10 grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-1">
                                    <label className="text-[10px] uppercase font-bold text-gray-500">Nombre / Entidad</label>
                                    <div className="relative">
                                        <UserCheck className="absolute left-3 top-2.5 w-4 h-4 text-gray-500" />
                                        <input
                                            type="text"
                                            value={stk.nombre}
                                            onChange={(e) => updateStakeholder(stk.id, 'nombre', e.target.value)}
                                            placeholder="Ej: Juan Pérez"
                                            className="w-full bg-gray-900 border border-gray-600 rounded-lg py-2 pl-9 pr-3 text-sm text-white focus:outline-none focus:border-purple-500 transition-colors"
                                        />
                                    </div>
                                </div>
                                <div className="space-y-1">
                                    <label className="text-[10px] uppercase font-bold text-gray-500">Rol en el Proyecto</label>
                                    <div className="relative">
                                        <Target className="absolute left-3 top-2.5 w-4 h-4 text-gray-500" />
                                        <input
                                            type="text"
                                            value={stk.rol}
                                            onChange={(e) => updateStakeholder(stk.id, 'rol', e.target.value)}
                                            placeholder="Ej: Gerente General"
                                            className="w-full bg-gray-900 border border-gray-600 rounded-lg py-2 pl-9 pr-3 text-sm text-white focus:outline-none focus:border-purple-500 transition-colors"
                                        />
                                    </div>
                                </div>
                            </div>

                            {/* Botón Eliminar (Mobile: Top, Desktop: Right) */}
                            <div className="md:col-span-2 flex justify-end">
                                <button
                                    onClick={() => removeStakeholder(stk.id)}
                                    className="p-2 text-gray-500 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                                    title="Eliminar interesado"
                                >
                                    <Trash2 className="w-5 h-5" />
                                </button>
                            </div>
                        </div>

                        {/* Poder e Interés */}
                        <div className="mt-4 pt-4 border-t border-gray-700/50 flex flex-wrap gap-4">
                            <div className="flex items-center gap-3">
                                <span className="text-xs text-gray-400 font-medium flex items-center gap-1">
                                    <Activity className="w-3 h-3" /> Poder:
                                </span>
                                <div className="flex gap-1">
                                    {['Alto', 'Medio', 'Bajo'].map(nivel => (
                                        <button
                                            key={nivel}
                                            onClick={() => updateStakeholder(stk.id, 'poder', nivel)}
                                            className={`px-3 py-1 rounded-md text-xs font-bold border transition-all ${stk.poder === nivel ? getNivelColor(nivel) : 'bg-gray-800 border-gray-700 text-gray-500 hover:bg-gray-700'}`}
                                        >
                                            {nivel}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="w-px h-6 bg-gray-700 hidden md:block"></div>

                            <div className="flex items-center gap-3">
                                <span className="text-xs text-gray-400 font-medium flex items-center gap-1">
                                    <Target className="w-3 h-3" /> Interés:
                                </span>
                                <div className="flex gap-1">
                                    {['Alto', 'Medio', 'Bajo'].map(nivel => (
                                        <button
                                            key={nivel}
                                            onClick={() => updateStakeholder(stk.id, 'interes', nivel)}
                                            className={`px-3 py-1 rounded-md text-xs font-bold border transition-all ${stk.interes === nivel ? getNivelColor(nivel) : 'bg-gray-800 border-gray-700 text-gray-500 hover:bg-gray-700'}`}
                                        >
                                            {nivel}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                ))}

                <button
                    onClick={addStakeholder}
                    className="w-full py-3 border-2 border-dashed border-gray-700 rounded-xl text-gray-400 hover:border-purple-500 hover:text-purple-400 hover:bg-purple-500/5 transition-all flex items-center justify-center gap-2 text-sm font-semibold"
                >
                    <Plus className="w-5 h-5" />
                    Agregar Nuevo Interesado
                </button>
            </div>

            <button
                onClick={handleSubmit}
                disabled={stakeholders.length === 0}
                className="w-full py-4 font-bold rounded-xl shadow-lg transform transition-all flex items-center justify-center gap-2 text-lg bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white shadow-purple-600/20 hover:scale-[1.02] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
            >
                <Save className="w-5 h-5" />
                Guardar Stakeholders
            </button>
        </div>
    );
};

export default FormularioStakeholdersPro;
