from abc import ABC, abstractmethod
from typing import Dict


class ResourceFactory(ABC):
    @abstractmethod
    def create_resource(self, resource_id: ResourceId, **kwargs) -> Resource:
        pass


class AppServiceFactory(ResourceFactory):
    def create_resource(self, resource_id: ResourceId, **kwargs) -> Resource:
        return AppService(
            resource_id,
            kwargs['runtime'],
            kwargs['region'],
            kwargs['replica_count']
        )


class StorageAccountFactory(ResourceFactory):
    def create_resource(self, resource_id: ResourceId, **kwargs) -> Resource:
        return StorageAccount(
            resource_id,
            kwargs['encryption_enabled'],
            kwargs['access_key'],
            kwargs['max_size_gb']
        )


class CacheDBFactory(ResourceFactory):
    def create_resource(self, resource_id: ResourceId, **kwargs) -> Resource:
        return CacheDB(
            resource_id,
            kwargs['ttl_seconds'],
            kwargs['capacity_mb'],
            kwargs['eviction_policy']
        )


class ResourceFactoryRegistry:
    def __init__(self):
        self._factories: Dict[str, ResourceFactory] = {}
    
    def register(self, resource_type: str, factory: ResourceFactory) -> None:
        self._factories[resource_type] = factory
    
    def create_resource(self, resource_type: str, resource_id: ResourceId, **kwargs) -> Resource:
        factory = self._factories.get(resource_type)
        if not factory:
            raise ValueError(f"Unknown resource type: {resource_type}")
        return factory.create_resource(resource_id, **kwargs)
