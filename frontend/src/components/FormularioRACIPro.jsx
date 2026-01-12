import React, { useState, useEffect } from 'react';
import { Table, CheckSquare, Save, Info } from 'lucide-react';

const FormularioRACIPro = ({ onSubmit, complejidad = 7 }) => {
    // Roles estándar
    const roles = [
        { id: 'PM', label: 'PM', full: 'Project Manager' },
        { id: 'Residente', label: 'Ing. Res', full: 'Ingeniero Residente' },
        { id: 'Tecnicos', label: 'Técnicos', full: 'Equipo Técnico' },
        { id: 'QA', label: 'Insp. QA', full: 'Inspector de Calidad/Seguridad' },
        { id: 'Cliente', label: 'Cliente', full: 'Cliente / Supervisor' }
    ];

    // Actividades según complejidad
    const getActividadesBase = (nivel) => {
        const base = [
            { id: 1, nombre: 'Planificación del Proyecto' },
            { id: 2, nombre: 'Diseño e Ingeniería' },
            { id: 3, nombre: 'Ejecución de Obra' },
            { id: 4, nombre: 'Control de Calidad' },
            { id: 5, nombre: 'Aprobación de Entregables' }
        ];

        if (nivel >= 7) {
            return [
                ...base,
                { id: 6, nombre: 'Gestión de Riesgos' },
                { id: 7, nombre: 'Cierre Administrativo' }
            ];
        }
        return base;
    };

    const [matriz, setMatriz] = useState([]);

    // Inicializar matriz vacía
    useEffect(() => {
        const actividades = getActividadesBase(complejidad);
        const inicial = actividades.map(act => {
            const row = { id: act.id, actividad: act.nombre };
            roles.forEach(rol => row[rol.id] = null); // null, 'R', 'A', 'C', 'I'
            return row;
        });

        // Precargar algunos valores lógicos por defecto para ayudar al usuario
        // R: Responsable, A: Aprobador, C: Consultado, I: Informado
        if (inicial.length > 0) {
            // Planificación: PM es Responsable, Cliente Aprueba
            inicial[0]['PM'] = 'A'; inicial[0]['Residente'] = 'R'; inicial[0]['Cliente'] = 'C';
            // Ejecución: Residente es Responsable, Técnicos Ejecutan (R/Asociado)
            inicial[2]['Residente'] = 'A'; inicial[2]['Tecnicos'] = 'R';
        }

        setMatriz(inicial);
    }, [complejidad]);

    const setRol = (actividadId, rolId, tipo) => {
        setMatriz(matriz.map(row =>
            row.id === actividadId ? { ...row, [rolId]: tipo } : row
        ));
    };

    const getCeldaClass = (tipo) => {
        switch (tipo) {
            case 'R': return 'bg-blue-600 text-white border-blue-500 font-bold'; // Responsible
            case 'A': return 'bg-red-600 text-white border-red-500 font-bold';  // Accountable
            case 'C': return 'bg-yellow-600 text-white border-yellow-500 font-bold'; // Consulted
            case 'I': return 'bg-green-600 text-white border-green-500 font-bold'; // Informed
            default: return 'bg-gray-800 text-gray-500 hover:bg-gray-700';
        }
    };

    const ciclos = ['R', 'A', 'C', 'I', null];

    const handleClickCelda = (actividadId, rolId) => {
        const fila = matriz.find(r => r.id === actividadId);
        const actual = fila[rolId];
        const nextIndex = (ciclos.indexOf(actual) + 1) % ciclos.length;
        setRol(actividadId, rolId, ciclos[nextIndex]);
    };

    const handleSubmit = () => {
        // Transformar al formato esperado por el backend/ProjectCharter
        // Formato: { actividad: "Nombre", roles: ["A", "R", "I", "C", "C"] } (orden según columnas)
        const raciFinal = matriz.map(row => ({
            actividad: row.actividad,
            roles: roles.map(r => row[r.id] || '-') // Usar guión si es null
        }));

        onSubmit(raciFinal);
    };

    return (
        <div className="bg-gray-900/95 p-6 rounded-2xl border border-blue-500/30 shadow-2xl w-full max-w-4xl animate-fadeIn backdrop-blur-xl">
            <div className="flex items-center justify-between mb-6 border-b border-blue-500/20 pb-4">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-500/20 rounded-lg">
                        <Table className="w-6 h-6 text-blue-400" />
                    </div>
                    <div>
                        <h3 className="text-xl font-bold text-white">Matriz RACI</h3>
                        <p className="text-xs text-blue-300">Asignación de Responsabilidades</p>
                    </div>
                </div>

                {/* Leyenda Compacta */}
                <div className="flex gap-2 text-[10px] font-bold">
                    <span className="px-2 py-1 bg-red-600/20 text-red-400 rounded border border-red-500/30" title="Accountable (Aprobador)">A: Aprobador</span>
                    <span className="px-2 py-1 bg-blue-600/20 text-blue-400 rounded border border-blue-500/30" title="Responsible (Responsable)">R: Responsable</span>
                    <span className="px-2 py-1 bg-yellow-600/20 text-yellow-400 rounded border border-yellow-500/30" title="Consulted (Consultado)">C: Consultado</span>
                    <span className="px-2 py-1 bg-green-600/20 text-green-400 rounded border border-green-500/30" title="Informed (Informado)">I: Informado</span>
                </div>
            </div>

            <div className="overflow-x-auto custom-scrollbar mb-6 rounded-xl border border-gray-700">
                <table className="w-full text-sm text-left">
                    <thead className="text-xs text-gray-400 uppercase bg-gray-800">
                        <tr>
                            <th scope="col" className="px-4 py-3 sticky left-0 bg-gray-800 z-10 w-1/3">Actividad</th>
                            {roles.map(rol => (
                                <th key={rol.id} scope="col" className="px-2 py-3 text-center min-w-[80px]" title={rol.full}>
                                    {rol.label}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {matriz.map((row) => (
                            <tr key={row.id} className="border-b border-gray-700 hover:bg-gray-800/50 transition-colors">
                                <td className="px-4 py-3 font-medium text-white sticky left-0 bg-gray-900 border-r border-gray-700 z-10">
                                    {row.actividad}
                                </td>
                                {roles.map(rol => (
                                    <td key={rol.id} className="p-1 text-center">
                                        <button
                                            onClick={() => handleClickCelda(row.id, rol.id)}
                                            className={`w-full h-10 rounded-lg border transition-all flex items-center justify-center text-sm shadow-sm ${getCeldaClass(row[rol.id])}`}
                                        >
                                            {row[rol.id] || <span className="opacity-10 text-xs">•</span>}
                                        </button>
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="flex items-center gap-2 mb-4 p-3 bg-blue-900/20 rounded-lg border border-blue-500/20">
                <Info className="w-4 h-4 text-blue-400 flex-shrink-0" />
                <p className="text-xs text-gray-300">
                    Haz clic repetidamente en las celdas para cambiar el rol:
                    <strong className="text-white ml-1">R ➝ A ➝ C ➝ I ➝ Vacío</strong>
                </p>
            </div>

            <button
                onClick={handleSubmit}
                className="w-full py-4 font-bold rounded-xl shadow-lg transform transition-all flex items-center justify-center gap-2 text-lg bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white shadow-blue-600/20 hover:scale-[1.02] active:scale-95"
            >
                <Save className="w-5 h-5" />
                Guardar Matriz RACI
            </button>
        </div>
    );
};

export default FormularioRACIPro;
