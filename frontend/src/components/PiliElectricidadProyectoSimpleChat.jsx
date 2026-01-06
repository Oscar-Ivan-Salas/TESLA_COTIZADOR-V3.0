import React, { useState, useRef, useEffect } from 'react';
import { Send, FileText, Phone, MapPin, Clock } from 'lucide-react';

const PiliElectricidadProyectoSimpleChat = ({ 
  datosCliente, 
  nombreProyecto, 
  clienteProyecto, 
  presupuestoEstimado, 
  monedaProyecto, 
  duracionMeses, 
  onDatosGenerados, 
  onBotonesUpdate, 
  onBack, 
  onFinish 
}) => {
  const [conversacion, setConversacion] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [conversationState, setConversationState] = useState(null);
  const [hasQuote, setHasQuote] = useState(false);
  const messagesEndRef = useRef(null);
  const hasSentInitialMessage = useRef(false);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversacion]);

  useEffect(() => {
    if (!hasSentInitialMessage.current) {
      hasSentInitialMessage.current = true;
      
      const estadoInicial = {
        cliente_nombre: datosCliente?.nombre || clienteProyecto || null,
        cliente_ruc: datosCliente?.ruc || null,
        cliente_direccion: datosCliente?.direccion || null,
        cliente_telefono: datosCliente?.telefono || null,
        cliente_email: datosCliente?.email || null,
        proyecto_nombre: nombreProyecto || null,
        presupuesto: presupuestoEstimado ? parseFloat(presupuestoEstimado) : null,
        moneda: monedaProyecto || 'PEN',
        duracion_meses: duracionMeses ? parseInt(duracionMeses) : null
      };
      
      setConversationState(estadoInicial);
      enviarMensaje('', estadoInicial);
    }
  }, []);

  const addMessage = (sender, text, buttons = null) => {
    setConversacion(prev => [...prev, {
      sender,
      text,
      buttons,
      timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
    }]);
    if (buttons && onBotonesUpdate) onBotonesUpdate(buttons);
  };

  const enviarMensaje = async (mensaje, estadoCustom = null) => {
    if (isTyping) return;
    setIsTyping(true);
    
    try {
      const res = await fetch('http://localhost:8000/api/chat/pili-electricidad-proyecto-simple', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mensaje,
          conversation_state: estadoCustom || conversationState
        })
      });
      
      const data = await res.json();
      
      if (data.success) {
        addMessage('bot', data.respuesta, data.botones);
        setConversationState(data.conversation_state);
        
        if (data.datos_generados) {
          setHasQuote(true);
          if (onDatosGenerados) onDatosGenerados(data.datos_generados);
        }
      }
    } catch (e) {
      addMessage('bot', '❌ Error de conexión. Por favor intenta de nuevo.');
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 rounded-2xl shadow-2xl overflow-hidden border-2 border-cyan-600/30">
      <div className="bg-gradient-to-r from-slate-800 to-blue-900 p-4 border-b-2 border-cyan-500/50 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-full flex items-center justify-center shadow-lg">
              <FileText className="w-7 h-7 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-cyan-400">PILI Proyecto Simple</h3>
              <p className="text-xs text-cyan-200">Electricidad • Experta IA</p>
            </div>
          </div>
          {onBack && (
            <button onClick={onBack} className="px-4 py-2 bg-cyan-700/50 hover:bg-cyan-600/70 text-white rounded-lg font-semibold transition-all backdrop-blur-sm">
              ← Volver
            </button>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-slate-950 to-black">
        {conversacion.map((msg, i) => (
          <div key={i} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
            <div className="max-w-[80%]">
              <div className={`rounded-2xl p-4 shadow-lg ${
                msg.sender === 'user' 
                  ? 'bg-gradient-to-br from-cyan-500 to-blue-600 text-white' 
                  : 'bg-slate-800/70 backdrop-blur-sm text-white border border-cyan-500/30'
              }`}>
                <div dangerouslySetInnerHTML={{ 
                  __html: (msg.text || '')
                    .replace(/\*\*(.*?)\*\*/g, '<strong class="text-cyan-300">$1</strong>')
                    .replace(/\n/g, '<br />') 
                }} />
              </div>
              {msg.buttons && (
                <div className="mt-3 flex flex-wrap gap-2">
                  {msg.buttons.map((btn, j) => (
                    <button
                      key={j}
                      onClick={() => {
                        addMessage('user', btn.value);
                        setTimeout(() => enviarMensaje(btn.value), 100);
                      }}
                      disabled={isTyping}
                      className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold shadow-md transition-all transform hover:scale-105 disabled:opacity-50"
                    >
                      {btn.text}
                    </button>
                  ))}
                </div>
              )}
              <div className={`text-xs mt-1 ${msg.sender === 'user' ? 'text-right text-cyan-200/60' : 'text-left text-gray-400'}`}>
                {msg.timestamp}
              </div>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start animate-fadeIn">
            <div className="bg-slate-800/70 backdrop-blur-sm rounded-2xl p-4 border border-cyan-500/30">
              <div className="flex gap-2">
                {[0, 150, 300].map((delay, i) => (
                  <div
                    key={i}
                    className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"
                    style={{ animationDelay: `${delay}ms` }}
                  />
                ))}
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="bg-slate-900/90 backdrop-blur-sm p-4 border-t-2 border-cyan-500/50">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (inputValue.trim()) {
                  addMessage('user', inputValue.trim());
                  enviarMensaje(inputValue.trim());
                  setInputValue('');
                }
              }
            }}
            placeholder="Escribe tu mensaje..."
            disabled={isTyping}
            className="flex-1 px-4 py-3 bg-slate-800 text-white border-2 border-cyan-600/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 placeholder-gray-400 disabled:opacity-50"
          />
          <button
            onClick={() => {
              if (inputValue.trim()) {
                addMessage('user', inputValue.trim());
                enviarMensaje(inputValue.trim());
                setInputValue('');
              }
            }}
            disabled={!inputValue.trim() || isTyping}
            className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105 disabled:opacity-50 flex items-center gap-2"
          >
            <Send className="w-5 h-5" />
            Enviar
          </button>
        </div>
        
        {hasQuote && onFinish && (
          <button
            onClick={onFinish}
            className="w-full mt-3 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-700 hover:from-green-500 hover:to-emerald-600 text-white rounded-lg font-bold shadow-lg transition-all transform hover:scale-105"
          >
            ✅ Finalizar y Ver Documento
          </button>
        )}
      </div>

      <div className="bg-slate-950 p-3 border-t border-cyan-800/30">
        <div className="flex justify-around text-xs text-gray-300">
          <div className="flex items-center gap-1">
            <Phone className="w-3 h-3" />
            <span>906 315 961</span>
          </div>
          <div className="flex items-center gap-1">
            <MapPin className="w-3 h-3" />
            <span>Huancayo</span>
          </div>
          <div className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            <span>Lun-Sáb 8am-6pm</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PiliElectricidadProyectoSimpleChat;
