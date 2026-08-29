import { useQuery } from '@tanstack/react-query';
import { DataRequirement, PanelConfiguration, PanelState } from '../types/panel';
import { panelRegistry } from '../services/panelRegistry';
import { apiClient } from '../services/apiClient';
import { useWebSocket } from './useWebSocket';
import { useEffect, useState } from 'react';

// Utility to build the correct API URL based on data requirements
const buildApiUrl = (req: DataRequirement, config: PanelConfiguration): string => {
  switch (req.type) {
    case 'instrument':
      if (config.endpoint === 'overview') return `/api/v1/markets/overview?exchange=${config.exchange || 'NSE'}`;
      if (config.endpoint === 'gainers') return `/api/v1/markets/gainers?limit=${config.limit || 10}&exchange=${config.exchange || 'NSE'}`;
      if (config.endpoint === 'losers') return `/api/v1/markets/losers?limit=${config.limit || 10}&exchange=${config.exchange || 'NSE'}`;
      if (config.endpoint === 'most-active') return `/api/v1/markets/most-active?limit=${config.limit || 10}&sort_by=${config.sortBy || 'volume'}&exchange=${config.exchange || 'NSE'}`;
      if (config.endpoint === 'breadth') return `/api/v1/markets/breadth?exchange=${config.exchange || 'NSE'}`;
      if (config.endpoint === 'watchlist' && config.watchlistId) return `/api/v1/watchlists/${config.watchlistId}`;
      return '';
    default:
      return '';
  }
};

export function usePanelData(
  requirements: DataRequirement[],
  configuration: PanelConfiguration,
  refreshTrigger: number
): PanelState {

  // For Phase 11 panels, we assume the first requirement dictates the main fetch
  const primaryReq = requirements[0];
  const endpointUrl = primaryReq ? buildApiUrl(primaryReq, configuration) : null;

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['panelData', endpointUrl, configuration, refreshTrigger],
    queryFn: async () => {
      if (!endpointUrl) return null;
      // In a real scenario, we might have simulated config flags for testing framework
      if (configuration.simulateError) throw new Error('Simulated error');
      if (configuration.simulateEmpty) return [];

      const response = await apiClient.get(endpointUrl);
      return response.data.data || response.data;
    },
    enabled: !!endpointUrl,
    staleTime: 30000,
    refetchInterval: 60000,
  });

  // Basic WebSocket Integration
  const { lastMessage, isConnected } = useWebSocket();
  const [liveData, setLiveData] = useState<any>(null);

  useEffect(() => {
    // If the websocket emits a message relevant to our panel, we merge it.
    // For simplicity in Phase 11 skeleton, we just listen. A robust implementation
    // would check the topic string (e.g., `market:gainers:NSE`) against our config.
    if (lastMessage) {
      try {
        const msg = JSON.parse(lastMessage.data);
        // Only update if topic matches
        if (msg.topic === configuration.wsTopic) {
           setLiveData(msg.payload);
        }
      } catch (e) {
        // ignore parse errors
      }
    }
  }, [lastMessage, configuration.wsTopic]);

  // If we have no endpoint, we might be a pure utility panel (like TestPanel)
  if (!endpointUrl) {
    return {
      status: configuration.simulateError ? 'error' : (configuration.simulateEmpty ? 'empty' : 'success'),
      data: { message: configuration.message || 'Hello from pure panel' },
      error: configuration.simulateError ? 'Simulated Error' : undefined,
      lastUpdated: new Date()
    };
  }

  // Merge static REST data with live WS data
  const mergedData = liveData || data;

  let status: PanelState['status'] = 'success';
  if (isLoading) status = 'loading';
  else if (error) status = 'error';
  else if (!mergedData || (Array.isArray(mergedData) && mergedData.length === 0)) status = 'empty';

  return {
    status,
    data: mergedData,
    error: error instanceof Error ? error.message : undefined,
    lastUpdated: new Date()
  };
}
