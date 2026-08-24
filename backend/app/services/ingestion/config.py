from pydantic import BaseModel

class IngestionConfig(BaseModel):
    retry_attempts: int = 3
    retry_base_delay_seconds: float = 1.0
    retry_max_delay_seconds: float = 60.0
    request_timeout_seconds: int = 30
    batch_size: int = 100
    concurrency_limit: int = 10
    staleness_threshold_seconds: int = 3600
    enable_validation: bool = True
    enable_normalization: bool = True
    log_level: str = "INFO"
