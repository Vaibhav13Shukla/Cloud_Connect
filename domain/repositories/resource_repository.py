from typing import Dict


class ResourceRepository:
    """Repository for managing resource persistence"""
    
    def __init__(self):
        self._resources: Dict[ResourceId, Resource] = {}
    
    def add(self, resource: Resource) -> None:
        if resource.id in self._resources:
            raise DuplicateResourceError(f"Resource '{resource.id}' already exists")
        self._resources[resource.id] = resource
    
    def get(self, resource_id: ResourceId) -> Resource:
        resource = self._resources.get(resource_id)
        if not resource:
            raise ResourceNotFoundException(f"Resource '{resource_id}' not found")
        return resource
    
    def exists(self, resource_id: ResourceId) -> bool:
        return resource_id in self._resources