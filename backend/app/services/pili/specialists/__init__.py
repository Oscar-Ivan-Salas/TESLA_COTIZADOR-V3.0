"""
🎯 Specialists - Especialistas modulares
"""

from .base_specialist import BaseSpecialist
from .universal_specialist import UniversalSpecialist
from .specialist_factory import SpecialistFactory, get_specialist_factory

__all__ = [
    'BaseSpecialist',
    'UniversalSpecialist',
    'SpecialistFactory',
    'get_specialist_factory'
]
