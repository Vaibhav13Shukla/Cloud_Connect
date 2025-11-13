from abc import ABC, abstractmethod


class ResourceObserver(ABC):
    @abstractmethod
    def on_resource_started(self, resource: Resource, message: str) -> None:
        pass
    
    @abstractmethod
    def on_resource_stopped(self, resource: Resource, message: str) -> None:
        pass
    
    @abstractmethod
    def on_resource_deleted(self, resource: Resource, message: str) -> None:
        pass


class LoggingObserver(ResourceObserver):
    def __init__(self, logger: 'Logger'):
        self._logger = logger
    
    def on_resource_started(self, resource: Resource, message: str) -> None:
        self._logger.log(resource.get_resource_type(), message)
    
    def on_resource_stopped(self, resource: Resource, message: str) -> None:
        self._logger.log(resource.get_resource_type(), message)
    
    def on_resource_deleted(self, resource: Resource, message: str) -> None:
        self._logger.log(resource.get_resource_type(), message)