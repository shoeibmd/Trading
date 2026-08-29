import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';

export const TopLosersPanel: React.FC<PanelProps> = () => {
  const { state } = usePanelContext();

  const losers = Array.isArray(state.data) ? state.data : [];

  return (
    <div className="w-full h-full overflow-y-auto">
      <table className="w-full text-sm text-left">
        <thead className="text-xs text-muted-foreground bg-muted/50 sticky top-0">
          <tr>
            <th className="px-4 py-2 font-medium">Symbol</th>
            <th className="px-4 py-2 font-medium text-right">Price</th>
            <th className="px-4 py-2 font-medium text-right">% Chg</th>
            <th className="px-4 py-2 font-medium text-right hidden sm:table-cell">Vol</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border/50">
          {losers.map((stock: any, i: number) => (
            <tr key={i} className="hover:bg-muted/30 transition-colors">
              <td className="px-4 py-2 font-semibold text-primary">{stock.symbol}</td>
              <td className="px-4 py-2 text-right">{stock.price.toFixed(2)}</td>
              <td className="px-4 py-2 text-right text-red-500 font-medium">{stock.percent_change.toFixed(2)}%</td>
              <td className="px-4 py-2 text-right text-muted-foreground hidden sm:table-cell">{stock.volume}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export const topLosersPanelDefinition: PanelDefinition = {
  id: 'top-losers',
  type: 'TopLosers',
  title: 'Top Losers',
  category: 'market',
  description: 'Displays worst performing stocks for the session.',
  defaultSize: 'medium',
  icon: 'ArrowDownRight',
  configurationSchema: {
    type: 'object',
    properties: {
      limit: { type: 'number', default: 10, title: 'Number of rows' },
      exchange: { type: 'string', default: 'NSE', title: 'Exchange' },
      endpoint: { type: 'string', default: 'losers' },
      wsTopic: { type: 'string', default: 'market:losers:NSE' }
    }
  },
  dataRequirements: [{ type: 'instrument' }],
  component: TopLosersPanel
};
