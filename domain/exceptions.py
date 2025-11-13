class DomainException(Exception):
    """Base exception for domain errors"""
    pass


class InvalidStateTransitionError(DomainException):
    pass


class ResourceNotFoundException(DomainException):
    pass


class DuplicateResourceError(DomainException):
    pass