from datetime import datetime
from domain.entities.resource import Resource
from domain.value_objects import ResourceId, Runtime, Region


class AppService(Resource):
    def __init__(self, resource_id: ResourceId, runtime: Runtime, region: Region, replica_count: int):
        if not 1 <= replica_count <= 10:
            raise ValueError("Replica count must be between 1 and 10")
        
        config = {
            "runtime": runtime.value,
            "region": region.value,
            "replica_count": replica_count
        }
        super().__init__(resource_id, config)
        self._runtime = runtime
        self._region = region
    
    def get_resource_type(self) -> str:
        return "AppService"
    
    def _get_start_message(self) -> str:
        time = datetime.now().strftime("%I:%M %p")
        return f"AppService started at {time} in {self._region.value}"
    
    def _get_stop_message(self) -> str:
        return "AppService stopped successfully"
    
    def _get_delete_message(self) -> str:
        return "AppService marked as deleted"