import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';

export const MostActivePanel: React.FC<PanelProps> = () => {
  const { state } = usePanelContext();

  const active = Array.isArray(state.data) ? state.data : [];

  return (
    <div className="w-full h-full overflow-y-auto">
      <table className="w-full text-sm text-left">
        <thead className="text-xs text-muted-foreground bg-muted/50 sticky top-0">
          <tr>
            <th className="px-4 py-2 font-medium">Symbol</th>
            <th className="px-4 py-2 font-medium text-right">Price</th>
            <th className="px-4 py-2 font-medium text-right">Volume</th>
            <th className="px-4 py-2 font-medium text-right hidden sm:table-cell">% Chg</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border/50">
          {active.map((stock: any, i: number) => {
             const isUp = stock.percent_change >= 0;
             return (
              <tr key={i} className="hover:bg-muted/30 transition-colors">
                <td className="px-4 py-2 font-semibold text-primary">{stock.symbol}</td>
                <td className="px-4 py-2 text-right">{stock.price.toFixed(2)}</td>
                <td className="px-4 py-2 text-right font-medium">{stock.volume.toLocaleString()}</td>
                <td className={`px-4 py-2 text-right hidden sm:table-cell ${isUp ? 'text-green-500' : 'text-red-500'}`}>
                  {isUp ? '+' : ''}{stock.percent_change.toFixed(2)}%
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export const mostActivePanelDefinition: PanelDefinition = {
  id: 'most-active',
  type: 'MostActive',
  title: 'Most Active Stocks',
  category: 'market',
  description: 'Displays stocks with the highest trading volume.',
  defaultSize: 'medium',
  icon: 'Activity',
  configurationSchema: {
    type: 'object',
    properties: {
      limit: { type: 'number', default: 10, title: 'Number of rows' },
      sortBy: { type: 'string', default: 'volume', title: 'Sort By (volume/value)' },
      exchange: { type: 'string', default: 'NSE', title: 'Exchange' },
      endpoint: { type: 'string', default: 'most-active' },
      wsTopic: { type: 'string', default: 'market:most-active:NSE' }
    }
  },
  dataRequirements: [{ type: 'instrument' }],
  component: MostActivePanel
};
