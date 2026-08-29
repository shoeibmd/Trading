import React, { useState } from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { Search, Plus } from 'lucide-react';
import { Input } from '../../ui/input';
import { Button } from '../../ui/button';

export const WatchlistPanel: React.FC<PanelProps> = () => {
  const { state } = usePanelContext();
  const [searchTerm, setSearchTerm] = useState('');

  // For Phase 11, data from the backend is mapped appropriately
  // The actual endpoint returns `{ items: [...] }`
  const watchlistItems = state.data?.items || [];

  return (
    <div className="w-full h-full flex flex-col bg-background">
      <div className="p-2 border-b flex gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Add symbol..."
            className="pl-8 h-8 text-sm"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <Button size="sm" className="h-8 w-8 p-0">
          <Plus className="h-4 w-4" />
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {watchlistItems.length === 0 ? (
          <div className="flex items-center justify-center h-full text-sm text-muted-foreground">
            No instruments in watchlist
          </div>
        ) : (
          <table className="w-full text-sm text-left">
            <thead className="text-[10px] text-muted-foreground bg-muted/30 sticky top-0 uppercase tracking-wider">
              <tr>
                <th className="px-3 py-2 font-medium">Symbol</th>
                <th className="px-3 py-2 font-medium text-right">Price</th>
                <th className="px-3 py-2 font-medium text-right">% Chg</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/50">
              {watchlistItems.map((item: any) => {
                // If real quote data isn't merged yet via WS, default to instrument data or 0
                const price = item.quote?.price || item.instrument?.last_price || 0;
                const pctChg = item.quote?.percent_change || 0;
                const isUp = pctChg >= 0;

                return (
                  <tr key={item.id} className="hover:bg-muted/30 transition-colors cursor-pointer">
                    <td className="px-3 py-2 font-semibold">{item.instrument?.symbol || 'UNKNOWN'}</td>
                    <td className="px-3 py-2 text-right">{price.toFixed(2)}</td>
                    <td className={`px-3 py-2 text-right font-medium ${isUp ? 'text-green-500' : 'text-red-500'}`}>
                      {isUp ? '+' : ''}{pctChg.toFixed(2)}%
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export const watchlistPanelDefinition: PanelDefinition = {
  id: 'watchlist',
  type: 'Watchlist',
  title: 'Watchlist',
  category: 'market',
  description: 'Displays a custom list of instruments with real-time quotes.',
  defaultSize: 'medium',
  icon: 'List',
  configurationSchema: {
    type: 'object',
    properties: {
      watchlistId: { type: 'string', title: 'Watchlist ID' },
      endpoint: { type: 'string', default: 'watchlist' }
    },
    required: ['watchlistId']
  },
  dataRequirements: [{ type: 'instrument' }],
  component: WatchlistPanel
};
