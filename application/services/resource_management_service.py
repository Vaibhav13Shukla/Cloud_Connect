from domain.repositories.resource_repository import ResourceRepository
from application.factories.resource_factory import ResourceFactoryRegistry
from application.observers.resource_observer import LoggingObserver
from domain.value_objects import ResourceId
from domain.entities.resource import Resource
from domain.exceptions import DuplicateResourceError

class ResourceManagementService:
    def __init__(self, repository: ResourceRepository, factory_registry: ResourceFactoryRegistry, 
                 logging_observer: LoggingObserver):
        self._repository = repository
        self._factory_registry = factory_registry
        self._logging_observer = logging_observer
    
    def create_resource(self, resource_type: str, name: str, **kwargs) -> Resource:
        resource_id = ResourceId(name)
        
        if self._repository.exists(resource_id):
            raise DuplicateResourceError(f"Resource '{name}' already exists")
        
        resource = self._factory_registry.create_resource(resource_type, resource_id, **kwargs)
        resource.attach_observer(self._logging_observer)
        self._repository.add(resource)
        
        return resource
    
    def start_resource(self, name: str) -> None:
        resource = self._repository.get(ResourceId(name))
        resource.start()
    
    def stop_resource(self, name: str) -> None:
        resource = self._repository.get(ResourceId(name))
        resource.stop()
    
    def delete_resource(self, name: str) -> None:
        resource = self._repository.get(ResourceId(name))
        resource.delete()