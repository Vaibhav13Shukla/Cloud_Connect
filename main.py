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