import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { ChartContainer } from '../../charts/ChartContainer';

export const StockChartPanel: React.FC<PanelProps> = () => {
  const { state, configuration } = usePanelContext();

  const ohlcvData = Array.isArray(state.data) ? state.data : [];

  return (
    <div className="w-full h-full bg-background flex flex-col relative">
      {/* Basic Toolbar placeholder */}
      <div className="h-8 border-b flex items-center px-2 text-xs text-muted-foreground gap-2 z-10 absolute top-0 left-0 w-full bg-background/80 backdrop-blur-sm">
        <span className="font-semibold text-foreground">{configuration.symbol || 'N/A'}</span>
        <span>|</span>
        <span>{configuration.interval || '1d'}</span>
        <span>|</span>
        <select className="bg-transparent border-none text-xs focus:ring-0 cursor-pointer" value={configuration.chartType || 'candlestick'} disabled>
          <option value="candlestick">Candles</option>
          <option value="line">Line</option>
          <option value="area">Area</option>
        </select>
      </div>

      <div className="flex-1 pt-8">
        {ohlcvData.length > 0 ? (
          <ChartContainer
            data={ohlcvData}
            type={configuration.chartType as any || 'candlestick'}
            showVolume={configuration.showVolume !== false}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-muted-foreground text-sm">
            No chart data available
          </div>
        )}
      </div>
    </div>
  );
};

export const stockChartPanelDefinition: PanelDefinition = {
  id: 'stock-chart',
  type: 'StockChart',
  title: 'Interactive Chart',
  category: 'stock',
  description: 'TradingView Lightweight Chart with OHLCV data.',
  defaultSize: 'large',
  icon: 'LineChart',
  configurationSchema: {
    type: 'object',
    properties: {
      symbol: { type: 'string', default: 'RELIANCE', title: 'Symbol' },
      exchange: { type: 'string', default: 'NSE', title: 'Exchange' },
      interval: { type: 'string', default: '1d', title: 'Timeframe' },
      chartType: { type: 'string', default: 'candlestick', enum: ['candlestick', 'line', 'area', 'bar'], title: 'Chart Type' },
      showVolume: { type: 'boolean', default: true, title: 'Show Volume' },
      endpoint: { type: 'string', default: 'ohlcv', title: 'Endpoint (Internal)' },
      wsTopic: { type: 'string', default: 'ohlcv:RELIANCE:NSE:1d', title: 'WebSocket Topic' }
    },
    required: ['symbol']
  },
  dataRequirements: [{ type: 'ohlcv' }],
  component: StockChartPanel
};
