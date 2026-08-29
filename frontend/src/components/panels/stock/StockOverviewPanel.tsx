import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { TrendingUp, TrendingDown, Clock, BarChart3, Info } from 'lucide-react';
import { Button } from '../../ui/button';

export const StockOverviewPanel: React.FC<PanelProps> = () => {
  const { state, configuration } = usePanelContext();

  if (!state.data) return null;

  const quote = state.data.quote || {};
  const instrument = state.data.instrument || {};
  const fundamentals = state.data.fundamentals || {};

  const isUp = (quote.change || 0) >= 0;

  return (
    <div className="w-full h-full p-4 overflow-y-auto bg-background flex flex-col gap-4">
      {/* Header Section */}
      <div className="flex justify-between items-start">
        <div>
          <h2 className="text-xl font-bold">{instrument.symbol || configuration.symbol || 'N/A'}</h2>
          <p className="text-sm text-muted-foreground">{instrument.name || 'Unknown Company'}</p>
          <span className="text-xs bg-muted px-2 py-0.5 rounded-sm mt-1 inline-block">
            {instrument.exchange || configuration.exchange || 'NSE'}
          </span>
        </div>
        <div className="flex flex-col items-end">
          <span className="text-2xl font-bold">{(quote.price || 0).toFixed(2)}</span>
          <div className={`flex items-center gap-1 font-medium ${isUp ? 'text-green-500' : 'text-red-500'}`}>
            {isUp ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
            <span>{(quote.change || 0).toFixed(2)} ({(quote.percent_change || 0).toFixed(2)}%)</span>
          </div>
          <div className="text-[10px] text-muted-foreground flex items-center gap-1 mt-1">
            <Clock className="h-3 w-3" />
            {quote.timestamp ? new Date(quote.timestamp).toLocaleTimeString() : 'Delayed'}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex gap-2">
        <Button variant="secondary" size="sm" className="flex-1">Add to Watchlist</Button>
        <Button variant="default" size="sm" className="flex-1">View Chart</Button>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-3 mt-2">
        <div className="bg-muted/30 p-2 rounded-md border">
          <p className="text-[10px] uppercase text-muted-foreground font-semibold tracking-wider">Volume</p>
          <p className="font-medium text-sm">{(quote.volume || 0).toLocaleString()}</p>
        </div>
        <div className="bg-muted/30 p-2 rounded-md border">
          <p className="text-[10px] uppercase text-muted-foreground font-semibold tracking-wider">Avg Volume</p>
          <p className="font-medium text-sm">{(fundamentals.average_volume || 0).toLocaleString()}</p>
        </div>
        <div className="bg-muted/30 p-2 rounded-md border">
          <p className="text-[10px] uppercase text-muted-foreground font-semibold tracking-wider">Day Range</p>
          <p className="font-medium text-sm">{(quote.low || 0).toFixed(2)} - {(quote.high || 0).toFixed(2)}</p>
        </div>
        <div className="bg-muted/30 p-2 rounded-md border">
          <p className="text-[10px] uppercase text-muted-foreground font-semibold tracking-wider">52W Range</p>
          <p className="font-medium text-sm">{(fundamentals.fifty_two_week_low || 0).toFixed(2)} - {(fundamentals.fifty_two_week_high || 0).toFixed(2)}</p>
        </div>
        <div className="bg-muted/30 p-2 rounded-md border">
          <p className="text-[10px] uppercase text-muted-foreground font-semibold tracking-wider">Market Cap</p>
          <p className="font-medium text-sm">{(fundamentals.market_cap || 0).toLocaleString()}</p>
        </div>
        <div className="bg-muted/30 p-2 rounded-md border">
          <p className="text-[10px] uppercase text-muted-foreground font-semibold tracking-wider">P/E Ratio</p>
          <p className="font-medium text-sm">{(fundamentals.pe_ratio || 0).toFixed(2)}</p>
        </div>
      </div>
    </div>
  );
};

export const stockOverviewPanelDefinition: PanelDefinition = {
  id: 'stock-overview',
  type: 'StockOverview',
  title: 'Stock Overview',
  category: 'stock',
  description: 'Comprehensive overview of a specific stock.',
  defaultSize: 'medium',
  icon: 'Info',
  configurationSchema: {
    type: 'object',
    properties: {
      symbol: { type: 'string', default: 'RELIANCE', title: 'Symbol' },
      exchange: { type: 'string', default: 'NSE', title: 'Exchange' },
      endpoint: { type: 'string', default: 'stock-overview', title: 'Endpoint (Internal)' },
      wsTopic: { type: 'string', default: 'quote:RELIANCE:NSE', title: 'WebSocket Topic' }
    },
    required: ['symbol']
  },
  dataRequirements: [{ type: 'quote' }],
  component: StockOverviewPanel
};
