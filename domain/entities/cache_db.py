from datetime import datetime
from domain.entities.resource import Resource
from domain.value_objects import ResourceId, EvictionPolicy

class CacheDB(Resource):
    def __init__(self, resource_id: ResourceId, ttl_seconds: int, capacity_mb: int, eviction_policy: EvictionPolicy):
        if not 1 <= ttl_seconds <= 86400:
            raise ValueError("TTL must be between 1 and 86400 seconds")
        if not 1 <= capacity_mb <= 10000:
            raise ValueError("Capacity must be between 1 and 10000 MB")
        
        config = {
            "ttl_seconds": ttl_seconds,
            "capacity_mb": capacity_mb,
            "eviction_policy": eviction_policy.value
        }
        super().__init__(resource_id, config)
        self._eviction_policy = eviction_policy
    
    def get_resource_type(self) -> str:
        return "CacheDB"
    
    def _get_start_message(self) -> str:
        time = datetime.now().strftime("%I:%M %p")
        return f"CacheDB started at {time} with {self._eviction_policy.value} eviction policy"
    
    def _get_stop_message(self) -> str:
        return "CacheDB stopped successfully"
    
    def _get_delete_message(self) -> str:
        return "CacheDB marked as deleted"
