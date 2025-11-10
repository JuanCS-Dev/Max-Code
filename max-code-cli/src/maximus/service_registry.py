"""MAXIMUS 103 Services Registry"""
from enum import IntEnum
from typing import Dict

class ServiceTier(IntEnum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3

MAXIMUS_SERVICES = {
    "constitutional-ai": {"tier": ServiceTier.CRITICAL, "timeout": 60, "model": "claude"},
    "consciousness-core": {"tier": ServiceTier.CRITICAL, "timeout": 45, "model": "claude"},
    "immune-t-cell": {"tier": ServiceTier.CRITICAL, "timeout": 20, "model": "openai"},
    "immune-b-cell": {"tier": ServiceTier.CRITICAL, "timeout": 20, "model": "openai"},
    "immune-nk-cell": {"tier": ServiceTier.CRITICAL, "timeout": 20, "model": "openai"},
    "immune-macrophage": {"tier": ServiceTier.CRITICAL, "timeout": 20, "model": "openai"},
    "immune-dendritic": {"tier": ServiceTier.CRITICAL, "timeout": 20, "model": "openai"},
    "immune-neutrophil": {"tier": ServiceTier.CRITICAL, "timeout": 20, "model": "openai"},
    "immune-eosinophil": {"tier": ServiceTier.CRITICAL, "timeout": 20, "model": "openai"},
    "immune-basophil": {"tier": ServiceTier.CRITICAL, "timeout": 20, "model": "openai"},
    "reactive-fabric": {"tier": ServiceTier.HIGH, "timeout": 30, "model": "openai"},
    "hitl-backend": {"tier": ServiceTier.HIGH, "timeout": 30, "model": "openai"},
    "memory-store": {"tier": ServiceTier.HIGH, "timeout": 30, "model": "openai"},
}

def get_service_config(service: str) -> Dict:
    return MAXIMUS_SERVICES.get(service, {"tier": ServiceTier.LOW, "timeout": 30, "model": "openai"})
