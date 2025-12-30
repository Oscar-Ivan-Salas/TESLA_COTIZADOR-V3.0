import React, { useState, useRef, useEffect } from 'react';
import { Send, Zap, Phone, MapPin, Clock } from 'lucide-react';

/**
 * 🎯 PiliITSEChat - Componente profesional para PILI especialista en ITSE
 * 
 * Diseño profesional con:
 * - Fondo degradado rojo-naranja
 * - Burbujas de chat estilizadas
 * - Botones interactivos con hover
 * - Conectado con backend Python (/api/chat/chat-contextualizado)
 */
const PiliITSEChat = ({ onCotizacionGenerada, onDatosGenerados, onBotonesUpdate, onBack, onFinish }) => {
    const [conversacion, setConversacion] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [conversationState, setConversationState] = useState(null); // Estado de conversación del backend
    const [hasQuote, setHasQuote] = useState(false); // Estado para habilitar botón Finalizar
    const messagesEndRef = useRef(null);

    // Colores corporativos Tesla EXACTOS (según tailwind.config.js e index.css)
    const colors = {
        primary: '#8B0000',      // tesla-red-900 (Oficial)
        secondary: '#D4AF37',    // tesla-gold-500 (Oficial)
        dark: '#450a0a',         // tesla-red-950 (Fondo oscuro)
        light_red: '#b91c1c',    // tesla-red-700 (Gradiente)
        gold_highlight: '#facc15' // tesla-gold-400 (Brillo)
    };

    const initialized = useRef(false);

    useEffect(() => {
        if (initialized.current) return;
        initialized.current = true;

        // Mensaje de bienvenida inicial
        addBotMessage(
            `¡Hola! 👋 Soy **Pili**, tu especialista en certificados ITSE de **Tesla Electricidad - Huancayo**.

🎯 Te ayudo a obtener tu certificado ITSE con:
✅ Visita técnica GRATUITA
✅ Precios oficiales TUPA Huancayo
✅ Trámite 100% gestionado
✅ Entrega en 7 días hábiles

**Selecciona tu tipo de establecimiento:**`,
            [
                { text: '🏥 Salud', value: 'SALUD' },
                { text: '🎓 Educación', value: 'EDUCACION' },
                { text: '🏨 Hospedaje', value: 'HOSPEDAJE' },
                { text: '🏪 Comercio', value: 'COMERCIO' },
                { text: '🍽️ Restaurante', value: 'RESTAURANTE' },
                { text: '🏢 Oficina', value: 'OFICINA' },
                { text: '🏭 Industrial', value: 'INDUSTRIAL' },
                { text: '🎭 Encuentro', value: 'ENCUENTRO' }
            ]
        );
    }, []);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [conversacion]);

    const addBotMessage = (text, buttons = null) => {
        const mensaje = {
            sender: 'bot',
            text,
            buttons,
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        };
        setConversacion(prev => [...prev, mensaje]);

        // Notificar botones al componente padre
        if (buttons && onBotonesUpdate) {
            onBotonesUpdate(buttons);
        }
    };

    const addUserMessage = (text) => {
        const mensaje = {
            sender: 'user',
            text,
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        };
        setConversacion(prev => [...prev, mensaje]);
    };

    const handleButtonClick = async (value, label) => {
        // VALIDACIÓN: Prevenir múltiples clicks mientras se procesa
        if (isTyping) {
            console.log('⏸️ Ya hay una petición en curso, ignorando click');
            return;
        }

        console.log('🖱️ CLICK EN BOTÓN:', { value, label, estadoActual: conversationState });

        addUserMessage(label);

        // DELAY: Esperar 100ms para que React actualice el estado
        await new Promise(resolve => setTimeout(resolve, 100));

        await enviarMensajeBackend(value);
    };

    const enviarMensajeBackend = async (mensaje) => {
        setIsTyping(true);

        console.log('📤 Enviando al backend:', { mensaje, conversationState });
        try {
            const response = await fetch('http://localhost:8000/api/chat/pili-itse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mensaje: mensaje,
                    conversation_state: conversationState
                })
            });

            const data = await response.json();

            if (data.success) {
                // Actualizar estado de conversación desde el backend
                if (data.state || data.conversation_state) {
                    setConversationState(data.state || data.conversation_state);
                    console.log('🔄 Estado de conversación actualizado:', data.state || data.conversation_state);
                }

                // Agregar respuesta de PILI
                const botones = data.botones_sugeridos || data.botones || null;
                addBotMessage(data.respuesta, botones);

                // Si hay datos generados, notificar al padre para vista previa
                if (data.datos_generados && onDatosGenerados) {
                    console.log('📊 Datos generados recibidos:', data.datos_generados);
                    onDatosGenerados(data.datos_generados);
                }

                // Si hay cotización generada, notificar al padre y habilitar botón
                if (data.cotizacion_generada) {
                    setHasQuote(true);
                    if (onCotizacionGenerada) {
                        onCotizacionGenerada(data.cotizacion_generada);
                    }
                }
            } else {
                addBotMessage('Lo siento, hubo un error. Por favor intenta de nuevo.');
            }
        } catch (error) {
            console.error('Error:', error);
            addBotMessage('Error de conexión. Verifica que el backend esté activo.');
        } finally {
            setIsTyping(false);
        }
    };

    const handleSendMessage = async () => {
        if (!inputValue.trim() || isTyping) return;

        const mensaje = inputValue.trim();
        addUserMessage(mensaje);
        setInputValue('');
        await enviarMensajeBackend(mensaje);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <div style={{
            minHeight: '600px',
            background: `linear-gradient(135deg, ${colors.dark} 0%, ${colors.primary} 60%, ${colors.light_red} 100%)`,
            borderRadius: '20px',
            fontFamily: 'system-ui, -apple-system, sans-serif',
            display: 'flex',
            flexDirection: 'column',
            boxShadow: '0 10px 40px rgba(139, 0, 0, 0.3)' // Sombra roja sutil
        }}>

            {/* Header */}
            <div style={{
                background: `linear-gradient(90deg, ${colors.primary}, ${colors.light_red})`,
                padding: '20px',
                borderRadius: '20px 20px 0 0',
                borderBottom: `3px solid ${colors.secondary}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    <div style={{
                        width: '60px',
                        height: '60px',
                        borderRadius: '50%',
                        background: `linear-gradient(135deg, ${colors.secondary}, ${colors.gold_highlight})`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        boxShadow: '0 0 15px rgba(212, 175, 55, 0.4)',
                        border: `2px solid ${colors.dark}`
                    }}>
                        <Zap size={32} color={colors.dark} strokeWidth={2.5} fill={colors.dark} />
                    </div>
                    <div>
                        <h1 style={{
                            color: 'white',
                            margin: 0,
                            fontSize: '22px',
                            fontWeight: '800',
                            letterSpacing: '0.5px',
                            textShadow: '0 2px 4px rgba(0,0,0,0.3)'
                        }}>
                            Pili - Especialista ITSE
                        </h1>
                        <p style={{
                            color: colors.secondary,
                            margin: 0,
                            fontSize: '13px',
                            fontWeight: '500',
                            opacity: 1
                        }}>
                            Tesla Electricidad • Huancayo
                        </p>
                    </div>
                </div>
            </div>

            {/* Chat Container */}
            <div style={{
                flex: 1,
                overflowY: 'auto',
                padding: '20px',
                background: '#fff',
                backgroundImage: `radial-gradient(${colors.secondary}20 1px, transparent 1px)`,
                backgroundSize: '20px 20px'
            }}>
                {conversacion.map((msg, index) => (
                    <div key={index} style={{
                        display: 'flex',
                        justifyContent: msg.sender === 'bot' ? 'flex-start' : 'flex-end',
                        marginBottom: '15px'
                    }}>
                        <div style={{
                            maxWidth: '80%',
                            padding: '14px 18px',
                            borderRadius: msg.sender === 'bot' ? '20px 20px 20px 2px' : '20px 20px 2px 20px',
                            background: msg.sender === 'bot'
                                ? `linear-gradient(135deg, ${colors.primary}, ${colors.light_red})`
                                : `linear-gradient(135deg, ${colors.secondary}, ${colors.gold_highlight})`,
                            color: msg.sender === 'bot' ? 'white' : '#000',
                            boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                            whiteSpace: 'pre-line',
                            border: msg.sender === 'bot' ? 'none' : `1px solid ${colors.secondary}`
                        }}>
                            <div dangerouslySetInnerHTML={{
                                __html: (msg.text || '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                            }} />

                            {msg.buttons && (
                                <div style={{ marginTop: '15px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                                    {msg.buttons.map((btn, btnIndex) => (
                                        <button
                                            key={btnIndex}
                                            onClick={() => handleButtonClick(btn.value, btn.text)}
                                            disabled={isTyping}
                                            style={{
                                                background: 'white',
                                                color: colors.primary,
                                                border: `1px solid ${colors.secondary}`,
                                                padding: '8px 16px',
                                                borderRadius: '20px',
                                                cursor: isTyping ? 'not-allowed' : 'pointer',
                                                fontWeight: '600',
                                                fontSize: '13px',
                                                transition: 'all 0.2s',
                                                boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
                                                opacity: isTyping ? 0.5 : 1
                                            }}
                                            onMouseOver={(e) => {
                                                e.target.style.background = colors.secondary;
                                                e.target.style.color = 'black';
                                                e.target.style.transform = 'translateY(-2px)';
                                            }}
                                            onMouseOut={(e) => {
                                                e.target.style.background = 'white';
                                                e.target.style.color = colors.primary;
                                                e.target.style.transform = 'translateY(0)';
                                            }}
                                        >
                                            {btn.text}
                                        </button>
                                    ))}
                                </div>
                            )}

                            <div style={{
                                fontSize: '10px',
                                marginTop: '6px',
                                opacity: 0.8,
                                textAlign: 'right',
                                fontStyle: 'italic'
                            }}>
                                {msg.timestamp}
                            </div>
                        </div>
                    </div>
                ))}

                {isTyping && (
                    <div style={{ display: 'flex', gap: '6px', padding: '15px' }}>
                        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: colors.primary, animation: 'bounce 1.4s infinite' }} />
                        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: colors.light_red, animation: 'bounce 1.4s infinite 0.2s' }} />
                        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: colors.secondary, animation: 'bounce 1.4s infinite 0.4s' }} />
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div style={{
                padding: '15px',
                background: `linear-gradient(to right, ${colors.primary}, ${colors.light_red})`,
                borderRadius: '0 0 20px 20px',
                display: 'flex',
                gap: '10px',
                alignItems: 'center'
            }}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Escribe tu respuesta..."
                    style={{
                        flex: 1,
                        padding: '12px 20px',
                        border: '2px solid rgba(255,255,255,0.2)',
                        borderRadius: '25px',
                        fontSize: '14px',
                        outline: 'none',
                        background: 'rgba(255,255,255,0.1)',
                        color: 'white'
                    }}
                />
                <button
                    onClick={handleSendMessage}
                    disabled={isTyping || !inputValue.trim()}
                    style={{
                        background: colors.secondary,
                        border: 'none',
                        borderRadius: '50%',
                        width: '45px',
                        height: '45px',
                        cursor: isTyping ? 'not-allowed' : 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        transition: 'transform 0.2s',
                        boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
                        opacity: isTyping ? 0.6 : 1
                    }}
                    onMouseOver={(e) => !isTyping && (e.target.style.transform = 'scale(1.1)')}
                    onMouseOut={(e) => e.target.style.transform = 'scale(1)'}
                >
                    <Send size={20} color="black" />
                </button>
            </div>

            {/* Navegación y Acciones */}
            <div style={{
                padding: '10px 15px 15px 15px',
                background: colors.dark,
                display: 'flex',
                justifyContent: 'space-between',
                gap: '10px',
                borderTop: `1px solid ${colors.primary}`
            }}>
                <button
                    onClick={onBack}
                    style={{
                        background: 'rgba(255,255,255,0.1)',
                        color: '#ddd',
                        border: '1px solid rgba(255,255,255,0.2)',
                        padding: '8px 16px',
                        borderRadius: '10px',
                        cursor: 'pointer',
                        fontSize: '12px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        transition: 'all 0.2s'
                    }}
                    onMouseOver={(e) => {
                        e.target.style.background = 'rgba(255,255,255,0.2)';
                        e.target.style.color = 'white';
                    }}
                    onMouseOut={(e) => {
                        e.target.style.background = 'rgba(255,255,255,0.1)';
                        e.target.style.color = '#ddd';
                    }}
                >
                    ← Configuración / Servicios
                </button>

                <button
                    onClick={onFinish}
                    disabled={!hasQuote}
                    style={{
                        background: hasQuote ? colors.secondary : 'rgba(255,255,255,0.1)',
                        color: hasQuote ? 'black' : 'rgba(255,255,255,0.3)',
                        border: 'none',
                        padding: '8px 20px',
                        borderRadius: '10px',
                        cursor: hasQuote ? 'pointer' : 'not-allowed',
                        fontSize: '12px',
                        fontWeight: 'bold',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        transition: 'all 0.2s',
                        boxShadow: hasQuote ? '0 0 15px rgba(212, 175, 55, 0.3)' : 'none'
                    }}
                    onMouseOver={(e) => {
                        if (hasQuote) {
                            e.target.style.transform = 'scale(1.05)';
                            e.target.style.boxShadow = '0 0 20px rgba(212, 175, 55, 0.5)';
                        }
                    }}
                    onMouseOut={(e) => {
                        if (hasQuote) {
                            e.target.style.transform = 'scale(1)';
                            e.target.style.boxShadow = '0 0 15px rgba(212, 175, 55, 0.3)';
                        }
                    }}
                >
                    Finalizar y Generar DOC →
                </button>
            </div>

            {/* Footer Info */}
            <div style={{
                padding: '12px',
                background: colors.dark,
                borderRadius: '0 0 20px 20px',
                marginTop: '-5px', // Solapamiento visual
                display: 'flex',
                justifyContent: 'center',
                gap: '20px',
                flexWrap: 'wrap',
                color: 'rgba(255,255,255,0.7)',
                fontSize: '11px',
                borderTop: `1px solid ${colors.primary}`
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Phone size={12} />
                    <span>906 315 961</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <MapPin size={12} />
                    <span>San Juan, Lima</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Clock size={12} />
                    <span>Lun-Sáb: 8am-6pm</span>
                </div>
            </div>

            <style>{`
        @keyframes bounce {
          0%, 80%, 100% {
            transform: scale(0);
          }
          40% {
            transform: scale(1);
          }
        }
        input::placeholder {
            color: rgba(255,255,255,0.6);
        }
      `}</style>
        </div>
    );
};

export default PiliITSEChat;
