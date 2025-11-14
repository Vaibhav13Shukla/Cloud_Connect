from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List
from domain.value_objects import ResourceId
from domain.states import ResourceState, CreatedState


class Resource(ABC):
    """Base entity for all cloud resources"""
    
    def __init__(self, resource_id: ResourceId, config: Dict):
        self._id = resource_id
        self._config = config
        self._state: ResourceState = CreatedState()
        self._created_at = datetime.now()
        self._observers: List['ResourceObserver'] = []
    
    @property
    def id(self) -> ResourceId:
        return self._id
    
    @property
    def state(self) -> str:
        return self._state.get_state_name()
    
    def set_state(self, state: ResourceState) -> None:
        self._state = state
    
    def start(self) -> None:
        self._state.start(self)
    
    def stop(self) -> None:
        self._state.stop(self)
    
    def delete(self) -> None:
        self._state.delete(self)
    
    def attach_observer(self, observer: 'ResourceObserver') -> None:
        self._observers.append(observer)
    
    def notify_started(self) -> None:
        for observer in self._observers:
            observer.on_resource_started(self, self._get_start_message())
    
    def notify_stopped(self) -> None:
        for observer in self._observers:
            observer.on_resource_stopped(self, self._get_stop_message())
    
    def notify_deleted(self) -> None:
        for observer in self._observers:
            observer.on_resource_deleted(self, self._get_delete_message())
    
    @abstractmethod
    def get_resource_type(self) -> str:
        pass
    
    @abstractmethod
    def _get_start_message(self) -> str:
        pass
    
    @abstractmethod
    def _get_stop_message(self) -> str:
        pass
    
    @abstractmethod
    def _get_delete_message(self) -> str:
        pass