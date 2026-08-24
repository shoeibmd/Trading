class IngestionError(Exception):
    """Base exception for all ingestion errors."""
    pass

class ValidationError(IngestionError):
    """Raised when data validation fails."""
    pass

class NormalizationError(IngestionError):
    """Raised when data normalization fails."""
    pass

class StorageError(IngestionError):
    """Raised when database storage operations fail."""
    pass

class PipelineError(IngestionError):
    """Raised when a general pipeline orchestration error occurs."""
    pass

class RateLimitExceededError(IngestionError):
    """Raised when the internal application rate limit strategy is exceeded."""
    pass

class StaleDataError(IngestionError):
    """Raised when incoming data is older than the configured staleness threshold."""
    pass
