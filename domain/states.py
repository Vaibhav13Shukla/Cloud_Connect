from abc import ABC, abstractmethod


class ResourceState(ABC):
    """Abstract base class for resource states"""
    
    @abstractmethod
    def start(self, resource: 'Resource') -> None:
        pass
    
    @abstractmethod
    def stop(self, resource: 'Resource') -> None:
        pass
    
    @abstractmethod
    def delete(self, resource: 'Resource') -> None:
        pass
    
    @abstractmethod
    def get_state_name(self) -> str:
        pass


class CreatedState(ResourceState):
    def start(self, resource: 'Resource') -> None:
        resource.set_state(StartedState())
        resource.notify_started()
    
    def stop(self, resource: 'Resource') -> None:
        raise InvalidStateTransitionError("Cannot stop a resource that hasn't been started")
    
    def delete(self, resource: 'Resource') -> None:
        resource.set_state(DeletedState())
        resource.notify_deleted()
    
    def get_state_name(self) -> str:
        return "Created"


class StartedState(ResourceState):
    def start(self, resource: 'Resource') -> None:
        raise InvalidStateTransitionError("Resource is already started")
    
    def stop(self, resource: 'Resource') -> None:
        resource.set_state(StoppedState())
        resource.notify_stopped()
    
    def delete(self, resource: 'Resource') -> None:
        raise InvalidStateTransitionError("Cannot delete: Resource must be stopped first")
    
    def get_state_name(self) -> str:
        return "Started"


class StoppedState(ResourceState):
    def start(self, resource: 'Resource') -> None:
        resource.set_state(StartedState())
        resource.notify_started()
    
    def stop(self, resource: 'Resource') -> None:
        raise InvalidStateTransitionError("Resource is already stopped")
    
    def delete(self, resource: 'Resource') -> None:
        resource.set_state(DeletedState())
        resource.notify_deleted()
    
    def get_state_name(self) -> str:
        return "Stopped"


class DeletedState(ResourceState):
    def start(self, resource: 'Resource') -> None:
        raise InvalidStateTransitionError("Cannot start a deleted resource")
    
    def stop(self, resource: 'Resource') -> None:
        raise InvalidStateTransitionError("Cannot stop a deleted resource")
    
    def delete(self, resource: 'Resource') -> None:
        raise InvalidStateTransitionError("Resource is already deleted")
    
    def get_state_name(self) -> str:
        return "Deleted"
