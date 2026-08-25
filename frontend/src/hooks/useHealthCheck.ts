import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient';
import { APIResponse, HealthResponse } from '@/types';

export function useHealthCheck() {
  return useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const { data } = await apiClient.get<APIResponse<HealthResponse>>('/api/v1/health');
      return data.data;
    }
  });
}
