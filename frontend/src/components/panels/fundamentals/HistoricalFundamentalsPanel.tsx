import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { ChartContainer } from '../../charts/ChartContainer';

export const HistoricalFundamentalsPanel: React.FC<PanelProps> = () => {
  const { state, configuration, onConfigurationChange } = usePanelContext();

  const metricData = Array.isArray(state.data) ? state.data : [];

  const chartData = metricData.map((d: any) => ({
    timestamp: d.period_end_date,
    close: parseFloat(d.value),
    open: parseFloat(d.value),
    high: parseFloat(d.value),
    low: parseFloat(d.value),
    volume: 0
  })).reverse(); // Chart container expects oldest to newest

  return (
    <div className="w-full h-full bg-background flex flex-col relative">
      <div className="h-8 border-b flex items-center px-2 text-xs text-muted-foreground gap-2 z-10 absolute top-0 left-0 w-full bg-background/80 backdrop-blur-sm">
        <span className="font-semibold text-foreground">{configuration.symbol || 'N/A'}</span>
        <span>|</span>
        <select
          className="bg-transparent border-none text-xs focus:ring-0 cursor-pointer"
          value={configuration.metric || 'revenue'}
          onChange={(e) => onConfigurationChange({ ...configuration, metric: e.target.value })}
        >
          <option value="revenue">Revenue</option>
          <option value="net_income">Net Income</option>
        </select>
        <span>|</span>
        <select
          className="bg-transparent border-none text-xs focus:ring-0 cursor-pointer"
          value={configuration.periodType || 'annual'}
          onChange={(e) => onConfigurationChange({ ...configuration, periodType: e.target.value })}
        >
          <option value="annual">Annual</option>
          <option value="quarterly">Quarterly</option>
        </select>
      </div>

      <div className="flex-1 pt-8">
        {chartData.length > 0 ? (
          <ChartContainer
            data={chartData}
            type={configuration.chartType as any || 'bar'}
            showVolume={false}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-muted-foreground text-sm flex-col gap-2">
            <span>No historical data available</span>
          </div>
        )}
      </div>
    </div>
  );
};

export const historicalFundamentalsPanelDefinition: PanelDefinition = {
  id: 'historical-fundamentals',
  type: 'HistoricalFundamentals',
  title: 'Historical Trends',
  category: 'fundamentals',
  description: 'Visualizes historical financial metrics over time.',
  defaultSize: 'large',
  icon: 'BarChart',
  configurationSchema: {
    type: 'object',
    properties: {
      symbol: { type: 'string', default: 'RELIANCE', title: 'Symbol' },
      metric: { type: 'string', default: 'revenue', enum: ['revenue', 'net_income'], title: 'Metric' },
      periodType: { type: 'string', default: 'annual', enum: ['annual', 'quarterly'], title: 'Period' },
      chartType: { type: 'string', default: 'bar', enum: ['bar', 'line', 'area'], title: 'Chart Type' },
      endpoint: { type: 'string', default: 'fundamentals-historical', title: 'Endpoint' }
    },
    required: ['symbol']
  },
  dataRequirements: [{ type: 'fundamentals' } as any],
  component: HistoricalFundamentalsPanel
};
