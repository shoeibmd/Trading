import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { TrendingUp, TrendingDown } from 'lucide-react';

export const MarketOverviewPanel: React.FC<PanelProps> = () => {
  const { state, configuration } = usePanelContext();

  // Data comes from REST + WebSockets merged in usePanelData
  const indices = state.data?.indices || [];

  return (
    <div className="w-full h-full p-4 overflow-y-auto bg-background">
      <div className="space-y-3">
        {indices.map((idx: any, i: number) => {
          const isUp = idx.change >= 0;
          return (
            <div key={i} className="flex items-center justify-between p-3 border rounded-lg hover:border-primary/50 transition-colors">
              <div className="flex flex-col">
                <span className="font-semibold text-sm">{idx.symbol}</span>
                <span className="text-xs text-muted-foreground">{idx.price.toFixed(2)}</span>
              </div>
              <div className="flex flex-col items-end">
                <div className={`flex items-center gap-1 font-medium ${isUp ? 'text-green-500' : 'text-red-500'}`}>
                  {isUp ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                  <span>{Math.abs(idx.percent_change).toFixed(2)}%</span>
                </div>
                <span className={`text-xs ${isUp ? 'text-green-500/80' : 'text-red-500/80'}`}>
                  {isUp ? '+' : ''}{idx.change.toFixed(2)}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export const marketOverviewPanelDefinition: PanelDefinition = {
  id: 'market-overview',
  type: 'MarketOverview',
  title: 'Market Overview',
  category: 'market',
  description: 'Displays major market indices and their daily performance.',
  defaultSize: 'small',
  icon: 'Activity',
  configurationSchema: {
    type: 'object',
    properties: {
      exchange: { type: 'string', default: 'NSE', title: 'Exchange' },
      endpoint: { type: 'string', default: 'overview', title: 'Endpoint (Internal)' },
      wsTopic: { type: 'string', default: 'market:overview', title: 'WebSocket Topic' }
    }
  },
  dataRequirements: [
    { type: 'instrument' } // Trigger REST fetch
  ],
  component: MarketOverviewPanel
};
