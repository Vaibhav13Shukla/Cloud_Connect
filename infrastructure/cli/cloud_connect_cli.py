from application.services.resource_management_service import ResourceManagementService
from infrastructure.logging.logger import Logger
from domain.value_objects import Runtime, Region, EvictionPolicy
from domain.entities.resource import Resource

class CloudConnectCLI:
    def __init__(self, service: ResourceManagementService, logger: Logger):
        self._service = service
        self._logger = logger
    
    def run(self) -> None:
        print("\n" + "="*60)
        print("  CloudConnect - Cloud Resource Manager")
        print("="*60)
        
        while True:
            self._show_menu()
            choice = input("\nEnter choice: ").strip()
            
            try:
                if choice == '1':
                    self._create_resource()
                elif choice == '2':
                    self._start_resource()
                elif choice == '3':
                    self._stop_resource()
                elif choice == '4':
                    self._delete_resource()
                elif choice == '5':
                    self._view_logs()
                elif choice == '6':
                    print("\nExiting CloudConnect. Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            input("\nPress Enter to continue...")
    
    def _show_menu(self) -> None:
        print("\n" + "-"*60)
        print("MAIN MENU")
        print("-"*60)
        print("1. Create Resource")
        print("2. Start Resource")
        print("3. Stop Resource")
        print("4. Delete Resource")
        print("5. View Logs")
        print("6. Exit")
    
    def _create_resource(self) -> None:
        print("\n--- Create Resource ---")
        print("Select resource type:")
        print("1. AppService")
        print("2. StorageAccount")
        print("3. CacheDB")
        
        choice = input("Choice: ").strip()
        
        if choice == '1':
            self._create_app_service()
        elif choice == '2':
            self._create_storage_account()
        elif choice == '3':
            self._create_cache_db()
        else:
            print("❌ Invalid resource type")
    
    def _create_app_service(self) -> None:
        name = input("Enter resource name: ").strip()
        
        print("\nSelect runtime:")
        print("1. python")
        print("2. nodejs")
        print("3. dotnet")
        runtime_choice = input("Choice: ").strip()
        runtime_map = {'1': Runtime.PYTHON, '2': Runtime.NODEJS, '3': Runtime.DOTNET}
        runtime = runtime_map.get(runtime_choice)
        
        if not runtime:
            print("❌ Invalid runtime")
            return
        
        print("\nSelect region:")
        print("1. EastUS")
        print("2. WestEurope")
        print("3. CentralIndia")
        region_choice = input("Choice: ").strip()
        region_map = {'1': Region.EAST_US, '2': Region.WEST_EUROPE, '3': Region.CENTRAL_INDIA}
        region = region_map.get(region_choice)
        
        if not region:
            print("❌ Invalid region")
            return
        
        print("\nSelect replica count:")
        print("1. 1 replica")
        print("2. 2 replicas")
        print("3. 3 replicas")
        replica_choice = input("Choice: ").strip()
        replica_map = {'1': 1, '2': 2, '3': 3}
        replica_count = replica_map.get(replica_choice)
        
        if not replica_count:
            print("❌ Invalid replica count")
            return
        
        self._service.create_resource('AppService', name, runtime=runtime, region=region, replica_count=replica_count)
        print(f"✅ AppService '{name}' created successfully!")
    
    def _create_storage_account(self) -> None:
        name = input("Enter resource name: ").strip()
        
        encryption = input("\nEnable encryption? (yes/no): ").strip().lower() == 'yes'
        access_key = input("Enter access key (min 16 chars): ").strip()
        
        print("\nSelect max size:")
        print("1. 100 GB")
        print("2. 500 GB")
        print("3. 1000 GB")
        size_choice = input("Choice: ").strip()
        size_map = {'1': 100, '2': 500, '3': 1000}
        max_size_gb = size_map.get(size_choice)
        
        if not max_size_gb:
            print("❌ Invalid size")
            return
        
        self._service.create_resource('StorageAccount', name, encryption_enabled=encryption, 
                                      access_key=access_key, max_size_gb=max_size_gb)
        print(f"✅ StorageAccount '{name}' created successfully!")
    
    def _create_cache_db(self) -> None:
        name = input("Enter resource name: ").strip()
        
        print("\nSelect TTL (Time To Live):")
        print("1. 60 seconds")
        print("2. 300 seconds")
        print("3. 3600 seconds")
        ttl_choice = input("Choice: ").strip()
        ttl_map = {'1': 60, '2': 300, '3': 3600}
        ttl_seconds = ttl_map.get(ttl_choice)
        
        if not ttl_seconds:
            print("❌ Invalid TTL")
            return
        
        print("\nSelect capacity:")
        print("1. 128 MB")
        print("2. 512 MB")
        print("3. 1024 MB")
        capacity_choice = input("Choice: ").strip()
        capacity_map = {'1': 128, '2': 512, '3': 1024}
        capacity_mb = capacity_map.get(capacity_choice)
        
        if not capacity_mb:
            print("❌ Invalid capacity")
            return
        
        print("\nSelect eviction policy:")
        print("1. LRU (Least Recently Used)")
        print("2. FIFO (First In First Out)")
        print("3. LFU (Least Frequently Used)")
        policy_choice = input("Choice: ").strip()
        policy_map = {'1': EvictionPolicy.LRU, '2': EvictionPolicy.FIFO, '3': EvictionPolicy.LFU}
        eviction_policy = policy_map.get(policy_choice)
        
        if not eviction_policy:
            print("❌ Invalid eviction policy")
            return
        
        self._service.create_resource('CacheDB', name, ttl_seconds=ttl_seconds, 
                                      capacity_mb=capacity_mb, eviction_policy=eviction_policy)
        print(f"✅ CacheDB '{name}' created successfully!")
    
    def _start_resource(self) -> None:
        print("\n--- Start Resource ---")
        name = input("Enter resource name: ").strip()
        self._service.start_resource(name)
    
    def _stop_resource(self) -> None:
        print("\n--- Stop Resource ---")
        name = input("Enter resource name: ").strip()
        self._service.stop_resource(name)
    
    def _delete_resource(self) -> None:
        print("\n--- Delete Resource ---")
        name = input("Enter resource name: ").strip()
        self._service.delete_resource(name)
    
    def _view_logs(self) -> None:
        print("\n--- Latest Log Entries ---")
        logs = self._logger.get_logs(20)
        if not logs:
            print("No logs available.")
        else:
            for log in logs:
                print(log.strip())