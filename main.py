from infrastructure.logging.logger import Logger
from domain.repositories.resource_repository import ResourceRepository
from application.factories.resource_factory import (
    ResourceFactoryRegistry, 
    AppServiceFactory, 
    StorageAccountFactory, 
    CacheDBFactory
)
from application.observers.resource_observer import LoggingObserver
from application.services.resource_management_service import ResourceManagementService
from infrastructure.cli.cloud_connect_cli import CloudConnectCLI


def main():
    """Bootstrap and run the CloudConnect application"""
    
    # Infrastructure
    logger = Logger()
    
    # Domain
    repository = ResourceRepository()
    
    # Application
    factory_registry = ResourceFactoryRegistry()
    factory_registry.register('AppService', AppServiceFactory())
    factory_registry.register('StorageAccount', StorageAccountFactory())
    factory_registry.register('CacheDB', CacheDBFactory())
    
    logging_observer = LoggingObserver(logger)
    service = ResourceManagementService(repository, factory_registry, logging_observer)
    
    # CLI
    cli = CloudConnectCLI(service, logger)
    cli.run()


if __name__ == "__main__":
    main()