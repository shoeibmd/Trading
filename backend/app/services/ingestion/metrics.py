import logging

class IngestionMetrics:
    def __init__(self) -> None:
        self.requests_total = 0
        self.success_count = 0
        self.failure_count = 0
        self.validation_failures = 0
        self.items_stored = 0
        self.rate_limit_hits = 0

    def record_request(self) -> None:
        self.requests_total += 1

    def record_success(self) -> None:
        self.success_count += 1

    def record_failure(self) -> None:
        self.failure_count += 1

    def record_validation_failure(self) -> None:
        self.validation_failures += 1

    def record_stored_items(self, count: int) -> None:
        self.items_stored += count

    def record_rate_limit_hit(self) -> None:
        self.rate_limit_hits += 1

    def log_metrics(self) -> None:
        logging.info(
            f"Ingestion Metrics - Requests: {self.requests_total}, "
            f"Success: {self.success_count}, Failures: {self.failure_count}, "
            f"Validation Failures: {self.validation_failures}, "
            f"Items Stored: {self.items_stored}, Rate Limit Hits: {self.rate_limit_hits}"
        )
