import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';

export const MarketBreadthPanel: React.FC<PanelProps> = () => {
  const { state } = usePanelContext();

  const advances = state.data?.advances || 0;
  const declines = state.data?.declines || 0;
  const unchanged = state.data?.unchanged || 0;
  const total = advances + declines + unchanged;

  const advPct = total > 0 ? (advances / total) * 100 : 0;
  const decPct = total > 0 ? (declines / total) * 100 : 0;
  const uncPct = total > 0 ? (unchanged / total) * 100 : 0;

  return (
    <div className="w-full h-full p-4 flex flex-col justify-center">
      <div className="flex justify-between items-end mb-2">
        <div className="flex flex-col">
          <span className="text-sm font-semibold text-green-500">Advances: {advances}</span>
        </div>
        <div className="flex flex-col text-right">
          <span className="text-sm font-semibold text-red-500">Declines: {declines}</span>
        </div>
      </div>

      {/* Simple Bar Chart */}
      <div className="w-full h-4 bg-muted rounded-full overflow-hidden flex mb-2">
        <div className="bg-green-500 h-full" style={{ width: `${advPct}%` }}></div>
        <div className="bg-muted-foreground/30 h-full" style={{ width: `${uncPct}%` }}></div>
        <div className="bg-red-500 h-full" style={{ width: `${decPct}%` }}></div>
      </div>

      <div className="flex justify-between text-xs text-muted-foreground mt-4">
        <span>Ratio (A/D): {declines > 0 ? (advances / declines).toFixed(2) : 'N/A'}</span>
        <span>Unchanged: {unchanged}</span>
      </div>
    </div>
  );
};

export const marketBreadthPanelDefinition: PanelDefinition = {
  id: 'market-breadth',
  type: 'MarketBreadth',
  title: 'Market Breadth',
  category: 'market',
  description: 'Displays the ratio of advancing to declining stocks.',
  defaultSize: 'small',
  icon: 'BarChart2',
  configurationSchema: {
    type: 'object',
    properties: {
      exchange: { type: 'string', default: 'NSE', title: 'Exchange' },
      endpoint: { type: 'string', default: 'breadth' },
      wsTopic: { type: 'string', default: 'market:breadth:NSE' }
    }
  },
  dataRequirements: [{ type: 'instrument' }],
  component: MarketBreadthPanel
};
