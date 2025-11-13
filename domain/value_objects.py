from enum import Enum


class ResourceId:
    """Value object for resource identification"""
    def __init__(self, name: str):
        if not name or not name.strip():
            raise ValueError("Resource name cannot be empty")
        if len(name) > 50:
            raise ValueError("Resource name cannot exceed 50 characters")
        self._name = name.strip()
    
    @property
    def value(self) -> str:
        return self._name
    
    def __eq__(self, other):
        return isinstance(other, ResourceId) and self._name == other._name
    
    def __hash__(self):
        return hash(self._name)
    
    def __str__(self):
        return self._name


class Region(Enum):
    EAST_US = "EastUS"
    WEST_EUROPE = "WestEurope"
    CENTRAL_INDIA = "CentralIndia"


class Runtime(Enum):
    PYTHON = "python"
    NODEJS = "nodejs"
    DOTNET = "dotnet"


class EvictionPolicy(Enum):
    LRU = "LRU"
    FIFO = "FIFO"
    LFU = "LFU"
