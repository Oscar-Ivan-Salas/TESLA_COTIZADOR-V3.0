import React, { useState, useEffect } from 'react';

const EDITABLE_PROYECTO_COMPLEJO = ({ datos = {}, esquemaColores = 'azul-tesla', logoBase64 = null, fuenteDocumento = 'Calibri', onDatosChange = () => { } }) => {
    // ✅ NUEVO: Detectar complejidad del proyecto (5, 6 o 7 fases)
    const complejidad = datos.complejidad || 7;

    // Estado inicial extendido con listas que antes eran estáticas
    const [datosEditables, setDatosEditables] = useState({
        nombre_proyecto: datos.nombre_proyecto || 'SISTEMA DE INSTALACIÓN ELÉCTRICA INDUSTRIAL',
        codigo_proyecto: datos.codigo_proyecto || 'PROY-PMI-001',
        cliente: datos.cliente || '',
        duracion_total: datos.duracion_total || 60,
        fecha_inicio: datos.fecha_inicio || new Date().toLocaleDateString('es-PE'),
        fecha_fin: datos.fecha_fin || '',
        presupuesto: datos.presupuesto || '75,000',
        spi: datos.spi || '1.05',
        cpi: datos.cpi || '0.98',
        ev_k: datos.ev_k || '45',
        pv_k: datos.pv_k || '43',
        ac_k: datos.ac_k || '46',
        alcance_proyecto: datos.alcance_proyecto || '',
        dias_ingenieria: datos.dias_ingenieria || 15,
        dias_ejecucion: datos.dias_ejecucion || 25,
        normativa_aplicable: datos.normativa_aplicable || 'CNE - Código Nacional de Electricidad',
        subtitulo_normativa: datos.subtitulo_normativa || 'Gestión según PMBOK® Guide 7th Edition',
        stakeholders: datos.stakeholders || [
            { nombre: 'Cliente', rol: 'Cliente / Patrocinador Principal', poder: 'Alto', interes: 'Alto' },
            { nombre: 'Jefe de Proyecto', rol: 'Project Manager / Responsable de Ejecución', poder: 'Alto', interes: 'Alto' },
            { nombre: 'Equipo Técnico', rol: 'Ingenieros y Técnicos Instaladores', poder: 'Medio', interes: 'Alto' }
        ],
        riesgos: datos.riesgos || [
            { id: 'R01', descripcion: 'Retrasos en entrega de equipos', probabilidad: 'Media', impacto: 'Alto', severidad: 'Alta', mitigacion: 'Compra anticipada de equipos críticos' },
            { id: 'R02', descripcion: 'Variación de precios de materiales', probabilidad: 'Media', impacto: 'Medio', severidad: 'Media', mitigacion: 'Cláusulas de precio fijo en contratos' },
            { id: 'R03', descripcion: 'Cambios en alcance del proyecto', probabilidad: 'Alta', impacto: 'Alto', severidad: 'Alta', mitigacion: 'Control de cambios riguroso con aprobaciones' },
            { id: 'R04', descripcion: 'Interferencias con otros contratistas', probabilidad: 'Alta', impacto: 'Medio', severidad: 'Media', mitigacion: 'Coordinación semanal con todos los actores' },
            { id: 'R05', descripcion: 'Fallas en equipos especializados', probabilidad: 'Baja', impacto: 'Alto', severidad: 'Media', mitigacion: 'Garantías extendidas y equipos de respaldo' }
        ],
        // ✅ NUEVO: Datos dinámicos para secciones antes estáticas
        entregables: datos.entregables || ['📋 Project Charter', '📊 Plan de gestión', '👥 Registro stakeholders', '📝 WBS y diccionario', '📅 Cronograma Gantt', '📐 Planos instalación', '📄 Especif. técnicas', '✅ Plan de calidad', '⚠️ Registro de riesgos', '🔬 Protocolos FAT/SAT', '🏗️ Planos as-built', '📚 Lecciones aprendidas', '🎯 Acta de cierre'],
        cronograma_fases: datos.cronograma_fases || [
            { label: '1. Inicio y Planificación', width: '15%', dias: '10 días' },
            { label: '2. Gestión Stakeholders', width: '8%', dias: '3 días' },
            { label: '3. Ingeniería y Diseño', width: '25%', dias: '15 días' },
            { label: '4. Ejecución', width: '40%', dias: '25 días' },
            { label: '5. Pruebas y Puesta en Marcha', width: '10%', dias: '8 días' },
            { label: '6. Cierre', width: '7%', dias: '5 días' }
        ],
        raci_actividades: datos.raci_actividades || [
            { actividad: 'Planificación del Proyecto', roles: ['A', 'R', 'I', 'C', 'C'] },
            { actividad: 'Diseño e Ingeniería', roles: ['A', 'R', 'C', 'C', 'I'] },
            { actividad: 'Ejecución de Obra', roles: ['A', 'A', 'R', 'C', 'I'] },
            { actividad: 'Control de Calidad', roles: ['A', 'C', 'C', 'R', 'I'] },
            { actividad: 'Aprobación de Entregables', roles: ['R', 'C', 'I', 'C', 'A'] }
        ],
        // ✅ NUEVO: Recursos y Materiales
        recursos_humanos: datos.recursos_humanos || ['Project Manager', 'Supervisor de Obra', 'Técnicos Electricistas', 'Prevencionista de Riesgos'],
        materiales: datos.materiales || ['Cables LSOH', 'Tableros Eléctricos Adosables', 'Interruptores Termomagnéticos', 'Dimales LED', 'Sistema de Puesta a Tierra'],
        // ✅ NUEVO: Información del Proyecto
        ubicacion: datos.ubicacion || '',
        area_m2: datos.area_m2 || ''
    });

    // Estado para la moneda
    const [moneda, setMoneda] = useState('S/'); // S/, $, €

    const COLORES = {
        'azul-tesla': { primario: '#0052A3', secundario: '#1E40AF', acento: '#3B82F6', claro: '#EFF6FF', claroBorde: '#DBEAFE' },
        'rojo-energia': { primario: '#8B0000', secundario: '#991B1B', acento: '#DC2626', claro: '#FEF2F2', claroBorde: '#FECACA' },
        'verde-ecologico': { primario: '#27AE60', secundario: '#16A34A', acento: '#22C55E', claro: '#F0FDF4', claroBorde: '#BBF7D0' },
        'personalizado': { primario: '#8B5CF6', secundario: '#7C3AED', acento: '#A78BFA', claro: '#F5F3FF', claroBorde: '#DDD6FE' }  // Morado personalizado
    };
    const colores = COLORES[esquemaColores] || COLORES['azul-tesla'];

    // ✅ CRÍTICO: Sincronizar datos del chatbot cuando lleguen
    useEffect(() => {
        if (datos && Object.keys(datos).length > 0) {
            console.log('🔍 SINCRONIZANDO DATOS DEL CHATBOT:', datos);
            console.log('🔍 COMPLEJIDAD RECIBIDA:', datos.complejidad);
            console.log('🔍 FASES RECIBIDAS:', datos.cronograma_fases?.length);

            setDatosEditables(prev => ({
                ...prev,
                // Sobrescribir SOLO los campos que vienen del chatbot
                ...(datos.nombre_proyecto && { nombre_proyecto: datos.nombre_proyecto }),
                ...(datos.codigo_proyecto && { codigo_proyecto: datos.codigo_proyecto }),
                ...(datos.cliente && { cliente: datos.cliente }),
                ...(datos.duracion_total && { duracion_total: datos.duracion_total }),
                ...(datos.fecha_inicio && { fecha_inicio: datos.fecha_inicio }),
                ...(datos.fecha_fin && { fecha_fin: datos.fecha_fin }),
                ...(datos.presupuesto && { presupuesto: datos.presupuesto }),
                ...(datos.spi && { spi: datos.spi }),
                ...(datos.cpi && { cpi: datos.cpi }),
                ...(datos.ev_k && { ev_k: datos.ev_k }),
                ...(datos.pv_k && { pv_k: datos.pv_k }),
                ...(datos.ac_k && { ac_k: datos.ac_k }),
                ...(datos.alcance_proyecto && { alcance_proyecto: datos.alcance_proyecto }),

                ...(datos.dias_ingenieria && { dias_ingenieria: datos.dias_ingenieria }),
                ...(datos.dias_ejecucion && { dias_ejecucion: datos.dias_ejecucion }),
                ...(datos.normativa_aplicable && { normativa_aplicable: datos.normativa_aplicable }),
                ...(datos.subtitulo_normativa && { subtitulo_normativa: datos.subtitulo_normativa }),
                ...(datos.stakeholders && { stakeholders: datos.stakeholders }),
                ...(datos.riesgos && { riesgos: datos.riesgos }),
                ...(datos.entregables && { entregables: datos.entregables }),
                // ✅ CRÍTICO: Cronograma dinámico
                ...(datos.cronograma_fases && { cronograma_fases: datos.cronograma_fases }),
                ...(datos.raci_actividades && { raci_actividades: datos.raci_actividades }),
                ...(datos.recursos_humanos && { recursos_humanos: datos.recursos_humanos }),
                ...(datos.materiales && { materiales: datos.materiales }),
                // ✅ NUEVO: Información del Proyecto
                ...(datos.ubicacion && { ubicacion: datos.ubicacion }),
                ...(datos.area_m2 && { area_m2: datos.area_m2 }),
                // ✅ NUEVO: Datos completos del cliente
                ...(datos.cliente && {
                    cliente: typeof datos.cliente === 'string' ? { nombre: datos.cliente } : datos.cliente
                })
            }));
        }
    }, [datos]);


    // ✅ Incluir moneda en los datos que se envían al padre
    useEffect(() => {
        onDatosChange({
            ...datosEditables,
            moneda: moneda === 'S/' ? 'PEN' : moneda === '$' ? 'USD' : 'EUR'
        });
    }, [datosEditables, moneda]);  // ✅ Agregar moneda como dependencia

    const getBadgeStyle = (nivel) => {
        const styles = {
            'Alta': { background: '#FEE2E2', color: '#991B1B' }, 'Alto': { background: '#FEE2E2', color: '#991B1B' },
            'Media': { background: '#FEF3C7', color: '#92400E' }, 'Medio': { background: '#FEF3C7', color: '#92400E' },
            'Baja': { background: '#D1FAE5', color: '#065F46' }, 'Bajo': { background: '#D1FAE5', color: '#065F46' }
        };
        return styles[nivel] || styles['Media'];
    };

    const getRACIStyle = (tipo) => {
        const styles = {
            'R': { background: '#DBEAFE', color: '#1E40AF' },
            'A': { background: '#FEE2E2', color: '#991B1B' },
            'C': { background: '#FEF3C7', color: '#92400E' },
            'I': { background: '#D1FAE5', color: '#065F46' }
        };
        return styles[tipo] || {};
    };

    return (
        <div style={{ fontFamily: fuenteDocumento, maxWidth: '210mm', margin: '0 auto', padding: '20mm', background: 'white', color: '#1f2937', lineHeight: '1.6' }}>
            {/* HEADER */}
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '30px', paddingBottom: '20px', borderBottom: `4px solid ${colores.primario}` }}>
                <div>
                    {logoBase64 ? <img src={logoBase64} alt="Logo" style={{ width: '180px', height: '80px', objectFit: 'contain', borderRadius: '8px' }} /> :
                        <div style={{ width: '180px', height: '80px', background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold', fontSize: '24px' }}>TESLA</div>}
                    {!logoBase64 && <p style={{ fontSize: '10px', color: '#6B7280' }}>Electricidad y Automatización</p>}
                </div>
                <div style={{ textAlign: 'right', fontSize: '11px', color: '#4b5563' }}>
                    <div style={{ fontSize: '20px', fontWeight: 'bold', color: colores.primario, marginBottom: '8px' }}>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
                    <div>RUC: 20601138787</div><div>Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div><div>Teléfono: 906 315 961 | Email: ingenieria.teslaelectricidad@gmail.com</div>
                </div>
            </div>

            {/* SELECTOR DE MONEDA */}
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '20px', gap: '10px', alignItems: 'center' }}>
                <span style={{ fontSize: '12px', fontWeight: '600', color: colores.secundario }}>Moneda:</span>
                <button onClick={() => setMoneda('S/')} style={{ padding: '6px 12px', background: moneda === 'S/' ? colores.primario : '#E5E7EB', color: moneda === 'S/' ? 'white' : '#6B7280', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '11px', fontWeight: '600' }}>S/ Soles</button>
                <button onClick={() => setMoneda('$')} style={{ padding: '6px 12px', background: moneda === '$' ? colores.primario : '#E5E7EB', color: moneda === '$' ? 'white' : '#6B7280', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '11px', fontWeight: '600' }}>$ Dólares</button>
                <button onClick={() => setMoneda('€')} style={{ padding: '6px 12px', background: moneda === '€' ? colores.primario : '#E5E7EB', color: moneda === '€' ? 'white' : '#6B7280', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '11px', fontWeight: '600' }}>€ Euros</button>
            </div>

            {/* TÍTULO */}
            <div style={{ textAlign: 'center', margin: '30px 0', padding: '25px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderLeft: `6px solid ${colores.primario}` }}>
                <h1 style={{ fontSize: '30px', color: colores.primario, marginBottom: '5px' }}>PROJECT CHARTER</h1>
                <div style={{ fontSize: '14px', color: colores.secundario, fontStyle: 'italic', margin: '8px 0' }}>Gestión de Proyectos según Metodología PMI</div>
                <div style={{ fontSize: '18px', color: colores.secundario, marginTop: '10px' }}>
                    <input type="text" value={datosEditables.nombre_proyecto} onChange={(e) => setDatosEditables({ ...datosEditables, nombre_proyecto: e.target.value })} style={{ width: '80%', border: 'none', borderBottom: `2px solid ${colores.acento}`, background: 'transparent', color: colores.secundario, fontSize: '18px', textAlign: 'center' }} />
                </div>
                <div style={{ fontSize: '14px', color: colores.secundario, fontWeight: '600', marginTop: '5px' }}>
                    <input type="text" value={datosEditables.codigo_proyecto} onChange={(e) => setDatosEditables({ ...datosEditables, codigo_proyecto: e.target.value })} style={{ width: '200px', border: 'none', borderBottom: `2px solid ${colores.acento}`, background: 'transparent', color: colores.secundario, fontSize: '14px', textAlign: 'center' }} />
                </div>
            </div>

            {/* INFO GRID */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '15px', margin: '25px 0' }}>
                {[
                    { label: 'Cliente', value: typeof datosEditables.cliente === 'object' ? datosEditables.cliente?.nombre : datosEditables.cliente, field: 'cliente' },
                    { label: 'Duración Total', value: `${datosEditables.duracion_total} días`, field: 'duracion_total' },
                    { label: 'Inicio', value: datosEditables.fecha_inicio, field: 'fecha_inicio' },
                    { label: 'Fin Estimado', value: datosEditables.fecha_fin, field: 'fecha_fin' }
                ].map((card, i) => (
                    <div key={i} style={{ padding: '15px', background: '#F9FAFB', borderLeft: '4px solid #3B82F6', borderRadius: '4px' }}>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', textTransform: 'uppercase' }}>{card.label}</div>
                        <div style={{ fontSize: '16px', color: colores.primario, fontWeight: 'bold', marginTop: '5px' }}>
                            <input type="text" value={card.value} onChange={(e) => setDatosEditables({ ...datosEditables, [card.field]: e.target.value })} style={{ width: '100%', border: 'none', background: 'transparent', color: colores.primario, fontWeight: 'bold', fontSize: '14px' }} />
                        </div>
                    </div>
                ))}
            </div>

            {/* PRESUPUESTO */}
            <div style={{ textAlign: 'center', padding: '20px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderRadius: '6px', margin: '20px 0' }}>
                <div style={{ fontSize: '12px', color: '#6B7280', marginBottom: '5px' }}>PRESUPUESTO TOTAL DEL PROYECTO</div>
                <div style={{ fontSize: '36px', color: colores.primario, fontWeight: 'bold' }}>
                    {moneda} <input type="text" value={datosEditables.presupuesto} onChange={(e) => setDatosEditables({ ...datosEditables, presupuesto: e.target.value })} style={{ width: '200px', border: 'none', background: 'transparent', color: colores.primario, fontWeight: 'bold', fontSize: '36px', textAlign: 'center' }} />
                </div>
            </div>

            {/* INFORMACIÓN DEL PROYECTO */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>📋 Información del Proyecto
                </h2>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', padding: '15px', background: '#F9FAFB', borderRadius: '6px' }}>
                    {/* Nombre del Proyecto */}
                    <div style={{ gridColumn: '1 / -1' }}>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>NOMBRE DEL PROYECTO</div>
                        <input type="text" value={datosEditables.nombre_proyecto || ''} onChange={(e) => setDatosEditables({ ...datosEditables, nombre_proyecto: e.target.value })} style={{ width: '100%', padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="Nombre del proyecto..." />
                    </div>


                    {/* Ubicación */}
                    <div>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>UBICACIÓN</div>
                        <input type="text" value={datosEditables.ubicacion || ''} onChange={(e) => setDatosEditables({ ...datosEditables, ubicacion: e.target.value })} style={{ width: '100%', padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="Ubicación del proyecto..." />
                    </div>

                    {/* Área del Proyecto */}
                    <div>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>ÁREA DEL PROYECTO</div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                            <input type="number" value={datosEditables.area_m2 || ''} onChange={(e) => setDatosEditables({ ...datosEditables, area_m2: e.target.value })} style={{ flex: 1, padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="0" />
                            <span style={{ fontSize: '12px', color: '#6B7280', fontWeight: '600' }}>m²</span>
                        </div>
                    </div>

                    {/* Presupuesto */}
                    <div>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>PRESUPUESTO</div>
                        <input type="text" value={datosEditables.presupuesto || ''} onChange={(e) => setDatosEditables({ ...datosEditables, presupuesto: e.target.value })} style={{ width: '100%', padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="0" />
                    </div>

                    {/* Duración */}
                    <div>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>DURACIÓN</div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                            <input type="text" value={datosEditables.duracion_total || ''} onChange={(e) => setDatosEditables({ ...datosEditables, duracion_total: e.target.value })} style={{ flex: 1, padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="0" />
                            <span style={{ fontSize: '12px', color: '#6B7280', fontWeight: '600' }}>días</span>
                        </div>
                    </div>

                    {/* Fecha Inicio */}
                    <div>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>FECHA INICIO</div>
                        <input type="text" value={datosEditables.fecha_inicio || ''} onChange={(e) => setDatosEditables({ ...datosEditables, fecha_inicio: e.target.value })} style={{ width: '100%', padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="DD/MM/AAAA" />
                    </div>

                    {/* Fecha Fin */}
                    <div>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>FECHA FIN</div>
                        <input type="text" value={datosEditables.fecha_fin || ''} onChange={(e) => setDatosEditables({ ...datosEditables, fecha_fin: e.target.value })} style={{ width: '100%', padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="DD/MM/AAAA" />
                    </div>
                </div>
            </div>

            {/* DATOS DEL CLIENTE */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>👤 Datos del Cliente
                </h2>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', padding: '15px', background: '#F9FAFB', borderRadius: '6px' }}>
                    <div style={{ gridColumn: '1 / -1' }}>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>NOMBRE DEL CLIENTE</div>
                        <input type="text" value={typeof datosEditables.cliente === 'object' ? datosEditables.cliente?.nombre : datosEditables.cliente} onChange={(e) => setDatosEditables({ ...datosEditables, cliente: { ...datosEditables.cliente, nombre: e.target.value } })} style={{ width: '100%', padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="Nombre del cliente..." />
                    </div>
                    <div>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>RUC / NIT</div>
                        <input type="text" value={datosEditables.cliente?.ruc || ''} onChange={(e) => setDatosEditables({ ...datosEditables, cliente: { ...datosEditables.cliente, ruc: e.target.value } })} style={{ width: '100%', padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="RUC del cliente..." />
                    </div>
                    <div>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>TELÉFONO</div>
                        <input type="text" value={datosEditables.cliente?.telefono || ''} onChange={(e) => setDatosEditables({ ...datosEditables, cliente: { ...datosEditables.cliente, telefono: e.target.value } })} style={{ width: '100%', padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="Teléfono..." />
                    </div>
                    <div>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>DIRECCIÓN</div>
                        <input type="text" value={datosEditables.cliente?.direccion || ''} onChange={(e) => setDatosEditables({ ...datosEditables, cliente: { ...datosEditables.cliente, direccion: e.target.value } })} style={{ width: '100%', padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="Dirección..." />
                    </div>
                    <div>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', marginBottom: '5px' }}>EMAIL</div>
                        <input type="email" value={datosEditables.cliente?.email || ''} onChange={(e) => setDatosEditables({ ...datosEditables, cliente: { ...datosEditables.cliente, email: e.target.value } })} style={{ width: '100%', padding: '8px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', fontSize: '12px' }} placeholder="Email..." />
                    </div>
                </div>
            </div>

            {/* KPIs PMI */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Indicadores de Desempeño (KPIs)
                </h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '15px', margin: '20px 0' }}>
                    {[
                        { label: 'SPI', value: datosEditables.spi, desc: 'Schedule Performance', field: 'spi' },
                        { label: 'CPI', value: datosEditables.cpi, desc: 'Cost Performance', field: 'cpi' },
                        { label: 'EV', value: `${moneda}${datosEditables.ev_k}K`, desc: 'Earned Value', field: 'ev_k' },
                        { label: 'PV', value: `${moneda}${datosEditables.pv_k}K`, desc: 'Planned Value', field: 'pv_k' },
                        { label: 'AC', value: `${moneda}${datosEditables.ac_k}K`, desc: 'Actual Cost', field: 'ac_k' }
                    ].map((kpi, i) => (
                        <div key={i} style={{ padding: '20px', background: 'white', border: `2px solid ${colores.claroBorde}`, borderRadius: '8px', textAlign: 'center' }}>
                            <div style={{ fontSize: '12px', color: '#6B7280', fontWeight: '600', marginBottom: '10px' }}>{kpi.label}</div>
                            <div style={{ fontSize: i < 2 ? '28px' : '20px', color: colores.primario, fontWeight: 'bold' }}>
                                <input type="text" value={kpi.value} onChange={(e) => setDatosEditables({ ...datosEditables, [kpi.field]: e.target.value.replace(/[^0-9.]/g, '') })} style={{ width: '80%', border: 'none', background: 'transparent', color: colores.primario, fontWeight: 'bold', fontSize: i < 2 ? '28px' : '20px', textAlign: 'center' }} />
                            </div>
                            <div style={{ fontSize: '9px', color: '#9CA3AF', marginTop: '5px' }}>{kpi.desc}</div>
                        </div>
                    ))}
                </div>
            </div>

            {/* ALCANCE */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Alcance del Proyecto (WBS Level 1)
                </h2>
                <div style={{ padding: '15px', background: '#F9FAFB', borderLeft: `4px solid ${colores.acento}`, fontSize: '12px', lineHeight: '1.8' }}>
                    <textarea value={datosEditables.alcance_proyecto} onChange={(e) => setDatosEditables({ ...datosEditables, alcance_proyecto: e.target.value })} style={{ width: '100%', minHeight: '100px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px', fontSize: '12px' }} placeholder="Descripción del alcance del proyecto..." />
                </div>
            </div>

            {/* CRONOGRAMA GANTT */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Cronograma del Proyecto (Diagrama Gantt)
                </h2>
                <div style={{ margin: '20px 0' }}>
                    {datosEditables.cronograma_fases.map((fase, i) => (
                        <div key={i} style={{ display: 'flex', alignItems: 'center', margin: '10px 0', fontSize: '11px' }}>
                            <div style={{ width: '200px', fontWeight: '600', color: '#374151' }}>
                                <input
                                    type="text"
                                    value={fase.label}
                                    onChange={(e) => {
                                        const nuevasFases = [...datosEditables.cronograma_fases];
                                        nuevasFases[i].label = e.target.value;
                                        setDatosEditables({ ...datosEditables, cronograma_fases: nuevasFases });
                                    }}
                                    style={{ width: '100%', border: 'none', background: 'transparent', fontWeight: 'bold' }}
                                />
                            </div>
                            <div style={{ flex: 1, height: '30px', background: '#F3F4F6', borderRadius: '4px', position: 'relative', overflow: 'hidden' }}>
                                <div style={{ width: fase.width, height: '100%', background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.acento} 100%)`, borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontSize: '10px', fontWeight: '600' }}>
                                    <input
                                        type="text"
                                        value={fase.dias}
                                        onChange={(e) => {
                                            const nuevasFases = [...datosEditables.cronograma_fases];
                                            nuevasFases[i].dias = e.target.value;
                                            setDatosEditables({ ...datosEditables, cronograma_fases: nuevasFases });
                                        }}
                                        style={{ width: '100%', border: 'none', background: 'transparent', color: 'white', textAlign: 'center', fontWeight: 'bold' }}
                                    />
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* STAKEHOLDERS */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Registro de Stakeholders
                </h2>
                {datosEditables.stakeholders.map((sh, i) => (
                    <div key={i} style={{ display: 'flex', padding: '15px', background: '#F9FAFB', borderLeft: `4px solid ${colores.acento}`, margin: '10px 0', borderRadius: '4px' }}>
                        <div style={{ flex: 1 }}>
                            <div style={{ fontSize: '14px', color: colores.primario, fontWeight: 'bold', marginBottom: '5px' }}>{sh.nombre}</div>
                            <div style={{ fontSize: '11px', color: '#6B7280' }}>{sh.rol}</div>
                        </div>
                        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                            <div>
                                <div style={{ fontSize: '10px', color: '#6B7280' }}>Poder:</div>
                                <span style={{ padding: '4px 12px', borderRadius: '12px', fontSize: '10px', fontWeight: '600', display: 'inline-block', ...getBadgeStyle(sh.poder) }}>{sh.poder}</span>
                            </div>
                            <div>
                                <div style={{ fontSize: '10px', color: '#6B7280' }}>Interés:</div>
                                <span style={{ padding: '4px 12px', borderRadius: '12px', fontSize: '10px', fontWeight: '600', display: 'inline-block', ...getBadgeStyle(sh.interes) }}>{sh.interes}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* MATRIZ RACI - Solo si complejidad >= 6 */}
            {complejidad >= 6 && (
                <div style={{ margin: '30px 0' }}>
                    <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Matriz RACI (Responsabilidades)
                    </h2>
                    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '10px' }}>
                        <thead style={{ background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, color: 'white' }}>
                            <tr>
                                <th style={{ padding: '12px', textAlign: 'left' }}>Actividad</th>
                                <th style={{ padding: '12px' }}>PM</th>
                                <th style={{ padding: '12px' }}>Ing. Residente</th>
                                <th style={{ padding: '12px' }}>Técnicos</th>
                                <th style={{ padding: '12px' }}>Inspector QA</th>
                                <th style={{ padding: '12px' }}>Cliente</th>
                            </tr>
                        </thead>
                        <tbody>
                            {datosEditables.raci_actividades.map((fila, i) => (
                                <tr key={i} style={{ background: i % 2 === 0 ? 'white' : '#F9FAFB' }}>
                                    <td style={{ padding: '10px 12px', borderBottom: '1px solid #E5E7EB' }}>
                                        <input
                                            type="text"
                                            value={fila.actividad}
                                            onChange={(e) => {
                                                const nuevasActs = [...datosEditables.raci_actividades];
                                                nuevasActs[i].actividad = e.target.value;
                                                setDatosEditables({ ...datosEditables, raci_actividades: nuevasActs });
                                            }}
                                            style={{ width: '100%', border: 'none', background: 'transparent' }}
                                        />
                                    </td>
                                    {fila.roles.map((rol, j) => (
                                        <td key={j} style={{ padding: '10px 12px', textAlign: 'center', borderBottom: '1px solid #E5E7EB' }}>
                                            <input
                                                type="text"
                                                value={rol}
                                                onChange={(e) => {
                                                    const nuevasActs = [...datosEditables.raci_actividades];
                                                    nuevasActs[i].roles[j] = e.target.value.toUpperCase().slice(0, 1);
                                                    setDatosEditables({ ...datosEditables, raci_actividades: nuevasActs });
                                                }}
                                                style={{ width: '30px', textAlign: 'center', padding: '4px 8px', borderRadius: '4px', fontWeight: 'bold', border: '1px solid #ddd', ...getRACIStyle(rol) }}
                                            />
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <div style={{ marginTop: '15px', padding: '10px', background: '#F9FAFB', borderRadius: '4px', fontSize: '10px' }}>
                        <strong>Leyenda:</strong>
                        {['R', 'A', 'C', 'I'].map((letra, i) => (
                            <span key={i} style={{ marginLeft: i > 0 ? '10px' : '5px' }}>
                                <span style={{ padding: '4px 8px', borderRadius: '4px', fontWeight: 'bold', ...getRACIStyle(letra) }}>{letra}</span>
                                {letra === 'R' && ' Responsable'}
                                {letra === 'A' && ' Aprobador'}
                                {letra === 'C' && ' Consultado'}
                                {letra === 'I' && ' Informado'}
                                {i < 3 && ' |'}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {/* RECURSOS Y MATERIALES - Sección Nueva */}
            <div style={{ margin: '30px 0', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                {/* Recursos Humanos */}
                <div>
                    <h2 style={{ fontSize: '16px', color: colores.primario, marginBottom: '10px', paddingBottom: '5px', borderBottom: `2px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ width: '4px', height: '20px', background: colores.acento }}></span>Equipo del Proyecto
                    </h2>
                    <div style={{ background: '#F9FAFB', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px' }}>
                        {datosEditables.recursos_humanos.map((recurso, i) => (
                            <div key={i} style={{ display: 'flex', alignItems: 'center', padding: '6px', borderBottom: i < datosEditables.recursos_humanos.length - 1 ? '1px solid #E5E7EB' : 'none' }}>
                                <span style={{ color: colores.acento, marginRight: '8px' }}>•</span>
                                <input
                                    type="text"
                                    value={recurso}
                                    onChange={(e) => {
                                        const nuevosRecursos = [...datosEditables.recursos_humanos];
                                        nuevosRecursos[i] = e.target.value;
                                        setDatosEditables({ ...datosEditables, recursos_humanos: nuevosRecursos });
                                    }}
                                    style={{ width: '100%', border: 'none', background: 'transparent', fontSize: '11px', color: '#374151' }}
                                />
                            </div>
                        ))}
                    </div>
                </div>

                {/* Materiales */}
                <div>
                    <h2 style={{ fontSize: '16px', color: colores.primario, marginBottom: '10px', paddingBottom: '5px', borderBottom: `2px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ width: '4px', height: '20px', background: colores.acento }}></span>Materiales Críticos
                    </h2>
                    <div style={{ background: '#F9FAFB', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px' }}>
                        {datosEditables.materiales.map((material, i) => (
                            <div key={i} style={{ display: 'flex', alignItems: 'center', padding: '6px', borderBottom: i < datosEditables.materiales.length - 1 ? '1px solid #E5E7EB' : 'none' }}>
                                <span style={{ color: colores.acento, marginRight: '8px' }}>•</span>
                                <input
                                    type="text"
                                    value={material}
                                    onChange={(e) => {
                                        const nuevosMateriales = [...datosEditables.materiales];
                                        nuevosMateriales[i] = e.target.value;
                                        setDatosEditables({ ...datosEditables, materiales: nuevosMateriales });
                                    }}
                                    style={{ width: '100%', border: 'none', background: 'transparent', fontSize: '11px', color: '#374151' }}
                                />
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* REGISTRO DE RIESGOS */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Registro de Riesgos (Top 5)
                </h2>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead style={{ background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, color: 'white' }}>
                        <tr>
                            <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', width: '5%' }}>ID</th>
                            <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', width: '30%' }}>Riesgo</th>
                            <th style={{ padding: '12px', textAlign: 'center', fontSize: '12px', width: '10%' }}>Probabilidad</th>
                            <th style={{ padding: '12px', textAlign: 'center', fontSize: '12px', width: '10%' }}>Impacto</th>
                            <th style={{ padding: '12px', textAlign: 'center', fontSize: '12px', width: '10%' }}>Severidad</th>
                            <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', width: '35%' }}>Plan de Mitigación</th>
                        </tr>
                    </thead>
                    <tbody>
                        {datosEditables.riesgos.map((riesgo, i) => (
                            <tr key={i} style={{ background: i % 2 === 0 ? 'white' : '#F9FAFB' }}>
                                <td style={{ padding: '10px 12px', fontSize: '11px', borderBottom: '1px solid #E5E7EB' }}>{riesgo.id}</td>
                                <td style={{ padding: '10px 12px', fontSize: '11px', borderBottom: '1px solid #E5E7EB' }}>{riesgo.descripcion}</td>
                                <td style={{ padding: '10px 12px', textAlign: 'center', fontSize: '11px', borderBottom: '1px solid #E5E7EB' }}>
                                    <span style={{ padding: '4px 10px', borderRadius: '12px', fontSize: '10px', fontWeight: '600', display: 'inline-block', ...getBadgeStyle(riesgo.probabilidad) }}>{riesgo.probabilidad}</span>
                                </td>
                                <td style={{ padding: '10px 12px', textAlign: 'center', fontSize: '11px', borderBottom: '1px solid #E5E7EB' }}>
                                    <span style={{ padding: '4px 10px', borderRadius: '12px', fontSize: '10px', fontWeight: '600', display: 'inline-block', ...getBadgeStyle(riesgo.impacto) }}>{riesgo.impacto}</span>
                                </td>
                                <td style={{ padding: '10px 12px', textAlign: 'center', fontSize: '11px', fontWeight: 'bold', color: riesgo.severidad === 'Alta' ? '#DC2626' : '#D97706', borderBottom: '1px solid #E5E7EB' }}>{riesgo.severidad}</td>
                                <td style={{ padding: '10px 12px', fontSize: '11px', borderBottom: '1px solid #E5E7EB' }}>{riesgo.mitigacion}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* ENTREGABLES */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Entregables Principales del Proyecto
                </h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px', margin: '20px 0' }}>
                    {datosEditables.entregables.map((entregable, i) => (
                        <div key={i} style={{ padding: '10px', background: '#F9FAFB', borderLeft: `3px solid ${colores.primario}`, fontSize: '11px' }}>
                            <input
                                type="text"
                                value={entregable}
                                onChange={(e) => {
                                    const nuevosEntregables = [...datosEditables.entregables];
                                    nuevosEntregables[i] = e.target.value;
                                    setDatosEditables({ ...datosEditables, entregables: nuevosEntregables });
                                }}
                                style={{ width: '100%', border: 'none', background: 'transparent', fontSize: '11px' }}
                            />
                        </div>
                    ))}
                </div>
            </div>

            {/* NORMATIVA */}
            <div style={{ padding: '15px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, margin: '25px 0' }}>
                <div style={{ fontSize: '12px', color: '#6B7280', marginBottom: '5px' }}>NORMATIVA Y ESTÁNDARES APLICABLES</div>
                <div style={{ fontSize: '14px', color: colores.primario, fontWeight: 'bold' }}>
                    <input type="text" value={datosEditables.normativa_aplicable} onChange={(e) => setDatosEditables({ ...datosEditables, normativa_aplicable: e.target.value })} style={{ width: '100%', border: 'none', background: 'transparent', color: colores.primario, fontWeight: 'bold', fontSize: '14px' }} />
                </div>
                <div style={{ fontSize: '11px', color: '#6B7280', marginTop: '5px' }}>
                    <input
                        type="text"
                        value={datosEditables.subtitulo_normativa || "Gestión según PMBOK® Guide 7th Edition"}
                        onChange={(e) => setDatosEditables({ ...datosEditables, subtitulo_normativa: e.target.value })}
                        style={{ width: '100%', border: 'none', background: 'transparent', color: '#6B7280' }}
                    />
                </div>
            </div>

            {/* FOOTER */}
            <div style={{ marginTop: '40px', paddingTop: '20px', borderTop: `3px solid ${colores.primario}`, textAlign: 'center', fontSize: '10px', color: '#6B7280' }}>
                <div style={{ fontWeight: 'bold', color: colores.primario, fontSize: '12px', marginBottom: '8px' }}>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
                <div>RUC: 20601138787 | Tel: 906 315 961 | Email: ingenieria.teslaelectricidad@gmail.com</div>
            </div>
        </div>
    );
};

export default EDITABLE_PROYECTO_COMPLEJO;
