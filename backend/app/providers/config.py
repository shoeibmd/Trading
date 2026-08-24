import os
import json
from typing import List, Dict, Any
from .models import RESTProviderConfig, WebSocketProviderConfig, ProviderType

def load_provider_configs_from_env() -> List[Any]:
    """
    Load JSON formatted configurations from a predefined environment variable
    E.g. PROVIDER_CONFIGS='[{"code": "MOCK", "name": "Mock", "provider_type": "REST_API", "base_url": "http://mock"}]'
    """
    raw_config = os.getenv("PROVIDER_CONFIGS")
    configs: List[Any] = []

    if raw_config:
        try:
            parsed = json.loads(raw_config)
            if not isinstance(parsed, list):
                raise ValueError("PROVIDER_CONFIGS must be a list of objects.")

            for p in parsed:
                ptype = p.get("provider_type")
                if ptype == ProviderType.REST_API.value:
                    configs.append(RESTProviderConfig(**p))
                elif ptype == ProviderType.WEBSOCKET.value:
                    configs.append(WebSocketProviderConfig(**p))
                else:
                    # Generic or Manual
                    pass
        except Exception as e:
            import logging
            logging.error(f"Failed to load provider configs from ENV: {e}")
            raise e

    return configs
