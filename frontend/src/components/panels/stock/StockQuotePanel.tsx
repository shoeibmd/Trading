import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';

export const StockQuotePanel: React.FC<PanelProps> = () => {
  const { state, configuration } = usePanelContext();

  if (!state.data) return null;

  const quote = state.data.quote || {};

  return (
    <div className="w-full h-full p-4 overflow-y-auto bg-background flex flex-col">
      <div className="flex justify-between items-end mb-4 border-b pb-2">
        <h3 className="font-bold text-lg">{configuration.symbol || 'N/A'} Quotes</h3>
        <span className="text-xs text-muted-foreground">
          {quote.timestamp ? new Date(quote.timestamp).toLocaleTimeString() : '--:--:--'}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Bid/Ask Depth Mockup */}
        <div className="space-y-1">
          <div className="text-[10px] uppercase text-muted-foreground font-bold tracking-wider mb-2 border-b pb-1">Bid (Buyers)</div>
          <div className="flex justify-between text-sm text-green-500 font-medium">
            <span>{(quote.price ? quote.price * 0.999 : 0).toFixed(2)}</span>
            <span>{Math.floor(Math.random() * 5000) + 100}</span>
          </div>
          <div className="flex justify-between text-sm text-green-500/80">
            <span>{(quote.price ? quote.price * 0.998 : 0).toFixed(2)}</span>
            <span>{Math.floor(Math.random() * 5000) + 100}</span>
          </div>
          <div className="flex justify-between text-sm text-green-500/60">
            <span>{(quote.price ? quote.price * 0.997 : 0).toFixed(2)}</span>
            <span>{Math.floor(Math.random() * 5000) + 100}</span>
          </div>
        </div>

        <div className="space-y-1">
          <div className="text-[10px] uppercase text-muted-foreground font-bold tracking-wider mb-2 border-b pb-1">Ask (Sellers)</div>
          <div className="flex justify-between text-sm text-red-500 font-medium">
            <span>{(quote.price ? quote.price * 1.001 : 0).toFixed(2)}</span>
            <span>{Math.floor(Math.random() * 5000) + 100}</span>
          </div>
          <div className="flex justify-between text-sm text-red-500/80">
            <span>{(quote.price ? quote.price * 1.002 : 0).toFixed(2)}</span>
            <span>{Math.floor(Math.random() * 5000) + 100}</span>
          </div>
          <div className="flex justify-between text-sm text-red-500/60">
            <span>{(quote.price ? quote.price * 1.003 : 0).toFixed(2)}</span>
            <span>{Math.floor(Math.random() * 5000) + 100}</span>
          </div>
        </div>
      </div>

      <div className="mt-auto pt-4 grid grid-cols-4 gap-2 text-center border-t">
        <div>
          <div className="text-[10px] text-muted-foreground">Open</div>
          <div className="text-sm font-medium">{(quote.open || 0).toFixed(2)}</div>
        </div>
        <div>
          <div className="text-[10px] text-muted-foreground">High</div>
          <div className="text-sm font-medium">{(quote.high || 0).toFixed(2)}</div>
        </div>
        <div>
          <div className="text-[10px] text-muted-foreground">Low</div>
          <div className="text-sm font-medium">{(quote.low || 0).toFixed(2)}</div>
        </div>
        <div>
          <div className="text-[10px] text-muted-foreground">Prev Close</div>
          <div className="text-sm font-medium">{(quote.previous_close || 0).toFixed(2)}</div>
        </div>
      </div>
    </div>
  );
};

export const stockQuotePanelDefinition: PanelDefinition = {
  id: 'stock-quote',
  type: 'StockQuote',
  title: 'Detailed Quote',
  category: 'stock',
  description: 'Bid/Ask market depth and detailed intraday quotes.',
  defaultSize: 'medium',
  icon: 'ListOrdered',
  configurationSchema: {
    type: 'object',
    properties: {
      symbol: { type: 'string', default: 'RELIANCE', title: 'Symbol' },
      exchange: { type: 'string', default: 'NSE', title: 'Exchange' },
      endpoint: { type: 'string', default: 'stock-quote', title: 'Endpoint (Internal)' },
      wsTopic: { type: 'string', default: 'quote:RELIANCE:NSE', title: 'WebSocket Topic' }
    },
    required: ['symbol']
  },
  dataRequirements: [{ type: 'quote' }],
  component: StockQuotePanel
};
