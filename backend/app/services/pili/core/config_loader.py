"""
📁 CONFIG LOADER - Carga configuraciones YAML
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    Carga y gestiona configuraciones YAML.
    
    Carga configuraciones de:
    - Servicios (itse, electricidad, etc.)
    - Documentos (cotizacion-simple, proyecto-complejo-pmi, etc.)
    - Agentes (pili-agents.yaml)
    - Multi-IA (multi-ia.yaml)
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Inicializa el loader.
        
        Args:
            config_dir: Directorio de configuraciones (default: pili/config/)
        """
        if config_dir is None:
            # Obtener directorio de este archivo
            current_file = Path(__file__)
            self.config_dir = current_file.parent.parent / "config"
        else:
            self.config_dir = Path(config_dir)
        
        logger.info(f"📁 ConfigLoader inicializado: {self.config_dir}")
    
    def load_service(self, service_name: str) -> Dict[str, Any]:
        """
        Carga configuración de un servicio.
        
        Args:
            service_name: Nombre del servicio (ej: 'itse', 'electricidad')
        
        Returns:
            Dict con configuración del servicio
        """
        config_file = self.config_dir / f"{service_name}.yaml"
        
        if not config_file.exists():
            logger.error(f"❌ Configuración no encontrada: {config_file}")
            raise FileNotFoundError(f"Configuración {service_name} no encontrada")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"✅ Configuración cargada: {service_name}")
        return config
    
    def load_document(self, document_type: str) -> Dict[str, Any]:
        """
        Carga configuración de un tipo de documento.
        
        Args:
            document_type: Tipo de documento (ej: 'cotizacion-simple')
        
        Returns:
            Dict con configuración del documento
        """
        config_file = self.config_dir / "documents" / f"{document_type}.yaml"
        
        if not config_file.exists():
            logger.error(f"❌ Configuración de documento no encontrada: {config_file}")
            raise FileNotFoundError(f"Documento {document_type} no encontrado")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"✅ Documento cargado: {document_type}")
        return config
    
    def load_agents(self) -> Dict[str, Any]:
        """
        Carga configuración de agentes.
        
        Returns:
            Dict con configuración de todos los agentes
        """
        config_file = self.config_dir / "agents" / "pili-agents.yaml"
        
        if not config_file.exists():
            logger.error(f"❌ Configuración de agentes no encontrada: {config_file}")
            raise FileNotFoundError("Configuración de agentes no encontrada")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"✅ Agentes cargados: {len(config.get('agents', {}))} agentes")
        return config
    
    def load_multi_ia(self) -> Dict[str, Any]:
        """
        Carga configuración de multi-IA.
        
        Returns:
            Dict con configuración de proveedores de IA
        """
        config_file = self.config_dir / "multi-ia.yaml"
        
        if not config_file.exists():
            logger.warning(f"⚠️ Configuración multi-IA no encontrada: {config_file}")
            # Retornar configuración por defecto
            return {
                "multi_ia": {
                    "enabled": False,
                    "fallback_mode": "pili_brain",
                    "providers": {}
                }
            }
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"✅ Multi-IA cargado")
        return config
    
    def list_services(self) -> list:
        """
        Lista todos los servicios disponibles.
        
        Returns:
            Lista de nombres de servicios
        """
        services = []
        for file in self.config_dir.glob("*.yaml"):
            if file.stem not in ['multi-ia']:
                services.append(file.stem)
        
        return sorted(services)
    
    def list_documents(self) -> list:
        """
        Lista todos los tipos de documentos disponibles.
        
        Returns:
            Lista de tipos de documentos
        """
        documents = []
        docs_dir = self.config_dir / "documents"
        
        if docs_dir.exists():
            for file in docs_dir.glob("*.yaml"):
                documents.append(file.stem)
        
        return sorted(documents)


# Instancia global
_config_loader = None

def get_config_loader() -> ConfigLoader:
    """Obtiene instancia global del config loader"""
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader
