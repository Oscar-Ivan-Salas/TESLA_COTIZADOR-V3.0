import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader, Sparkles, User, Bot } from 'lucide-react';

const ChatIA = ({ contexto, onCotizacionGenerada }) => {
  const [mensajes, setMensajes] = useState([
    {
      role: 'assistant',
      content: '¡Hola! Soy tu asistente de cotización. Cuéntame sobre el proyecto que necesitas cotizar.'
    }
  ]);
  const [inputMensaje, setInputMensaje] = useState('');
  const [cargando, setCargando] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [mensajes]);

  const enviarMensaje = async () => {
    if (!inputMensaje.trim() || cargando) return;

    const nuevoMensaje = {
      role: 'user',
      content: inputMensaje
    };

    setMensajes(prev => [...prev, nuevoMensaje]);
    setInputMensaje('');
    setCargando(true);

    try {
      const response = await fetch('/api/chat/conversacional', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          mensaje: inputMensaje,
          contexto: mensajes
        })
      });

      const data = await response.json();

      setMensajes(prev => [...prev, {
        role: 'assistant',
        content: data.respuesta
      }]);

      // Si la IA generó una cotización completa
      if (data.cotizacion) {
        onCotizacionGenerada(data.cotizacion);
      }

    } catch (error) {
      console.error('Error al enviar mensaje:', error);
      setMensajes(prev => [...prev, {
        role: 'assistant',
        content: 'Disculpa, hubo un error. ¿Puedes intentarlo de nuevo?'
      }]);
    } finally {
      setCargando(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      enviarMensaje();
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-gradient-to-br from-gray-900 to-black rounded-2xl shadow-2xl border-2 border-yellow-600">
      {/* Header */}
      <div className="bg-gradient-to-r from-red-900 to-black p-4 rounded-t-2xl border-b-2 border-yellow-600">
        <div className="flex items-center gap-3">
          <div className="bg-yellow-600 p-2 rounded-full animate-pulse">
            <Sparkles className="text-black" size={24} />
          </div>
          <div>
            <h3 className="text-yellow-400 font-bold text-xl">Asistente IA Gemini</h3>
            <p className="text-gray-400 text-sm">Generando cotización inteligente...</p>
          </div>
        </div>
      </div>

      {/* Mensajes */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {mensajes.map((msg, index) => (
          <div
            key={index}
            className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role === 'assistant' && (
              <div className="bg-yellow-600 p-2 rounded-full h-fit">
                <Bot size={20} className="text-black" />
              </div>
            )}
            
            <div
              className={`max-w-[70%] p-4 rounded-2xl ${
                msg.role === 'user'
                  ? 'bg-gradient-to-r from-red-900 to-red-800 text-white'
                  : 'bg-gray-800 text-gray-100'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>

            {msg.role === 'user' && (
              <div className="bg-red-900 p-2 rounded-full h-fit">
                <User size={20} className="text-yellow-400" />
              </div>
            )}
          </div>
        ))}

        {cargando && (
          <div className="flex gap-3 justify-start">
            <div className="bg-yellow-600 p-2 rounded-full h-fit animate-pulse">
              <Bot size={20} className="text-black" />
            </div>
            <div className="bg-gray-800 p-4 rounded-2xl">
              <div className="flex gap-2 items-center">
                <Loader className="animate-spin text-yellow-400" size={20} />
                <span className="text-gray-400">Gemini está pensando...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 bg-gray-900 rounded-b-2xl border-t-2 border-yellow-600">
        <div className="flex gap-3">
          <textarea
            value={inputMensaje}
            onChange={(e) => setInputMensaje(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Describe tu proyecto o haz preguntas..."
            className="flex-1 bg-gray-800 text-white rounded-xl p-3 border-2 border-gray-700 focus:border-yellow-600 focus:outline-none resize-none"
            rows="2"
            disabled={cargando}
          />
          <button
            onClick={enviarMensaje}
            disabled={cargando || !inputMensaje.trim()}
            className="bg-gradient-to-r from-yellow-600 to-yellow-500 text-black px-6 rounded-xl font-bold hover:from-yellow-500 hover:to-yellow-400 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={24} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatIA;