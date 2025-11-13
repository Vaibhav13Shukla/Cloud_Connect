class StorageAccount(Resource):
    def __init__(self, resource_id: ResourceId, encryption_enabled: bool, access_key: str, max_size_gb: int):
        if not 1 <= max_size_gb <= 10000:
            raise ValueError("Max size must be between 1 and 10000 GB")
        if not access_key or len(access_key) < 16:
            raise ValueError("Access key must be at least 16 characters")
        
        config = {
            "encryption_enabled": encryption_enabled,
            "access_key": access_key,
            "max_size_gb": max_size_gb
        }
        super().__init__(resource_id, config)
        self._encryption_enabled = encryption_enabled
    
    def get_resource_type(self) -> str:
        return "StorageAccount"
    
    def _get_start_message(self) -> str:
        time = datetime.now().strftime("%I:%M %p")
        encryption = "with encryption" if self._encryption_enabled else "without encryption"
        return f"StorageAccount started at {time} {encryption}"
    
    def _get_stop_message(self) -> str:
        return "StorageAccount stopped successfully"
    
    def _get_delete_message(self) -> str:
        return "StorageAccount marked as deleted"