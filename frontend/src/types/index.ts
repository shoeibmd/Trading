export interface APIResponse<T> {
  data: T;
  meta?: Record<string, any>;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface HealthResponse {
  status: string;
  database: string;
  redis: string;
  providers: string;
  latency_ms: number;
}
