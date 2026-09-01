import { useQuery } from '@tanstack/react-query';
import { DataRequirement, PanelConfiguration, PanelState } from '../types/panel';
import { apiClient } from '../services/apiClient';
import { useWebSocket } from './useWebSocket';
import { useEffect, useState } from 'react';

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
    case 'quote':
      if (config.endpoint === 'stock-overview' && config.symbol) return `/api/v1/instruments/${config.symbol}`;
      if (config.endpoint === 'stock-quote' && config.symbol) return `/api/v1/quotes/${config.symbol}`;
      return '';
    case 'ohlcv':
      if (config.symbol) return `/api/v1/ohlcv/${config.symbol}?interval=${config.interval || '1d'}`;
      return '';
    case 'news':
      if (config.endpoint === 'news-market') return `/api/v1/news/?limit=${config.limit || 20}`;
      if (config.endpoint === 'news-company' && config.symbol) return `/api/v1/news/instrument/${config.symbol}?limit=${config.limit || 20}`;
      if (config.endpoint === 'news-search' && config.query) return `/api/v1/news/search?q=${config.query}&limit=20`;
      if (config.endpoint === 'news-article' && config.articleId) return `/api/v1/news/${config.articleId}`;
      return '';
    case 'fundamentals':
      if (config.endpoint === 'fundamentals-profile' && config.symbol) return `/api/v1/fundamentals/${config.symbol}/profile`;
      if (config.endpoint === 'fundamentals-statements' && config.symbol) return `/api/v1/fundamentals/${config.symbol}/statements/${config.statementType || 'income'}?period_type=${config.periodType || 'annual'}&limit=4`;
      if (config.endpoint === 'fundamentals-ratios' && config.symbol) return `/api/v1/fundamentals/${config.symbol}/ratios?period_type=${config.periodType || 'annual'}&limit=4`;
      if (config.endpoint === 'fundamentals-historical' && config.symbol && config.metric) return `/api/v1/fundamentals/${config.symbol}/historical?metric=${config.metric}&period_type=${config.periodType || 'annual'}&limit=20`;
      return '';
    case 'portfolio':
      if (config.endpoint === 'portfolio-positions' && config.portfolioId) return `/api/v1/portfolios/${config.portfolioId}/positions`;
      if (config.endpoint === 'portfolio-transactions' && config.portfolioId) return `/api/v1/portfolios/${config.portfolioId}/transactions`;
      if (config.endpoint === 'portfolio-summary' && config.portfolioId) return `/api/v1/portfolios/${config.portfolioId}/summary`;
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

  const primaryReq = requirements[0];
  const endpointUrl = primaryReq ? buildApiUrl(primaryReq, configuration) : null;

  const { data, isLoading, error } = useQuery({
    queryKey: ['panelData', endpointUrl, configuration, refreshTrigger],
    queryFn: async () => {
      if (!endpointUrl) return null;
      if (configuration.simulateError) throw new Error('Simulated error');
      if (configuration.simulateEmpty) return [];

      const response = await apiClient.get(endpointUrl);
      return response.data.data || response.data;
    },
    enabled: !!endpointUrl,
    staleTime: 30000,
    refetchInterval: 60000,
  });

  const { lastMessage } = useWebSocket();
  const [liveData, setLiveData] = useState<any>(null);

  useEffect(() => {
    if (lastMessage) {
      try {
        const msg = JSON.parse(lastMessage.data);
        if (msg.topic === configuration.wsTopic) {
           setLiveData(msg.payload);
        }
      } catch (e) {
        // ignore parse errors
      }
    }
  }, [lastMessage, configuration.wsTopic]);

  if (!endpointUrl) {
    return {
      status: configuration.simulateError ? 'error' : (configuration.simulateEmpty ? 'empty' : 'success'),
      data: { message: configuration.message || 'Hello from pure panel' },
      error: configuration.simulateError ? 'Simulated Error' : undefined,
      lastUpdated: new Date()
    };
  }

  const mergedData = liveData || data;

  let status: PanelState['status'] = 'success';
  if (isLoading) status = 'loading';
  else if (error) status = 'error';
  else if (!mergedData || (Array.isArray(mergedData) && mergedData.length === 0) || (typeof mergedData === 'object' && Object.keys(mergedData).length === 0)) status = 'empty';

  return {
    status,
    data: mergedData,
    error: error instanceof Error ? error.message : undefined,
    lastUpdated: new Date()
  };
}
