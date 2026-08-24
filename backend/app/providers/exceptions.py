class ProviderError(Exception):
    """Base exception for provider-related errors."""
    pass

class ProviderNotAvailableError(ProviderError):
    """Raised when a provider is offline or unreachable."""
    pass

class ProviderRateLimitError(ProviderError):
    """Raised when provider rate limits are exceeded."""
    pass

class ProviderAuthenticationError(ProviderError):
    """Raised for authentication/authorization issues with the provider."""
    pass

class ProviderDataError(ProviderError):
    """Raised when data received from a provider is invalid or corrupted."""
    pass

class ProviderTimeoutError(ProviderError):
    """Raised when a request to a provider times out."""
    pass

class SymbolNotFoundError(ProviderError):
    """Raised when a requested symbol is not found by the provider."""
    pass

class ExchangeNotFoundError(ProviderError):
    """Raised when a requested exchange is not found by the provider."""
    pass
