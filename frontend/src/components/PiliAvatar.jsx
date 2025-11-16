import React from 'react';
import { Bot } from 'lucide-react';

/**
 * 👑 PILI Avatar - La cara bonita del proyecto
 *
 * Avatar de PILI (Procesadora Inteligente de Licitaciones Industriales)
 * con su corona distintiva de reina de la inteligencia
 */
const PiliAvatar = ({ size = 24, className = "", showCrown = true }) => {
  const containerSize = size + 8;

  return (
    <div
      className={`relative inline-flex items-center justify-center ${className}`}
      style={{ width: containerSize, height: containerSize }}
    >
      {/* Corona sobre PILI */}
      {showCrown && (
        <div
          className="absolute -top-1 left-1/2 transform -translate-x-1/2 z-10"
          style={{
            fontSize: size * 0.5,
            filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.3))'
          }}
        >
          👑
        </div>
      )}

      {/* Bot Icon de PILI */}
      <div className="relative">
        <Bot
          size={size}
          className="text-black animate-pulse"
          strokeWidth={2.5}
        />

        {/* Brillo especial en los "ojos" de PILI */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: 'radial-gradient(circle at 40% 40%, rgba(255,215,0,0.4) 0%, transparent 60%)',
            animation: 'pili-shine 3s ease-in-out infinite'
          }}
        />
      </div>

      <style jsx>{`
        @keyframes pili-shine {
          0%, 100% { opacity: 0.3; }
          50% { opacity: 0.8; }
        }
      `}</style>
    </div>
  );
};

/**
 * Variantes del Avatar de PILI para diferentes contextos
 */
export const PiliAvatarLarge = ({ showCrown = true }) => (
  <div className="relative inline-block">
    {showCrown && (
      <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 z-10 text-4xl animate-bounce">
        👑
      </div>
    )}
    <div className="bg-gradient-to-br from-yellow-400 via-yellow-500 to-yellow-600 p-4 rounded-full shadow-2xl border-4 border-yellow-300 relative overflow-hidden">
      <Bot size={48} className="text-black relative z-10" strokeWidth={2.5} />

      {/* Efecto de brillo animado */}
      <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white to-transparent opacity-30 animate-pulse" />

      {/* Partículas doradas */}
      <div className="absolute inset-0">
        <div className="absolute top-2 right-2 w-1 h-1 bg-yellow-200 rounded-full animate-ping" />
        <div className="absolute bottom-3 left-3 w-1 h-1 bg-yellow-200 rounded-full animate-ping" style={{ animationDelay: '0.5s' }} />
        <div className="absolute top-1/2 right-1 w-1 h-1 bg-yellow-200 rounded-full animate-ping" style={{ animationDelay: '1s' }} />
      </div>
    </div>
  </div>
);

/**
 * Badge de PILI con nombre
 */
export const PiliBadge = ({ nombre = "PILI", variant = "default" }) => {
  const variants = {
    default: "bg-yellow-600 text-black",
    cotizadora: "bg-yellow-600 text-black",
    analista: "bg-blue-600 text-white",
    coordinadora: "bg-green-600 text-white",
    projectManager: "bg-purple-600 text-white",
    reportera: "bg-indigo-600 text-white",
    analistaSenior: "bg-red-600 text-white"
  };

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full ${variants[variant]} font-bold text-sm shadow-lg border-2 border-opacity-50 border-white`}>
      <PiliAvatar size={16} showCrown={true} />
      <span>{nombre}</span>
      <span className="text-xs opacity-75">IA</span>
    </div>
  );
};

/**
 * Estado de PILI (pensando, escribiendo, etc.)
 */
export const PiliStatus = ({ status = "active" }) => {
  const statusConfig = {
    active: { text: "Lista para ayudar", color: "bg-green-500", icon: "✨" },
    thinking: { text: "Pensando...", color: "bg-yellow-500", icon: "🤔" },
    analyzing: { text: "Analizando...", color: "bg-blue-500", icon: "🔍" },
    generating: { text: "Generando documento...", color: "bg-purple-500", icon: "📄" },
    offline: { text: "Modo offline", color: "bg-gray-500", icon: "💤" }
  };

  const config = statusConfig[status] || statusConfig.active;

  return (
    <div className="flex items-center gap-2">
      <PiliAvatar size={20} showCrown={true} />
      <div className="flex items-center gap-2">
        <div className={`w-2 h-2 ${config.color} rounded-full animate-pulse`} />
        <span className="text-sm text-gray-300 font-medium">
          {config.icon} {config.text}
        </span>
      </div>
    </div>
  );
};

export default PiliAvatar;
