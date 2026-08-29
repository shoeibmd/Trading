import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { ChartContainer } from '../../charts/ChartContainer';

export const TechnicalIndicatorsPanel: React.FC<PanelProps> = () => {
  const { state, configuration } = usePanelContext();

  const indicatorData = Array.isArray(state.data) ? state.data : [];

  return (
    <div className="w-full h-full bg-background flex flex-col relative">
      <div className="h-8 border-b flex items-center px-2 text-xs text-muted-foreground gap-2 z-10 absolute top-0 left-0 w-full bg-background/80 backdrop-blur-sm">
        <span className="font-semibold text-foreground">{configuration.symbol || 'N/A'}</span>
        <span>|</span>
        <span>{configuration.indicatorType || 'RSI'}</span>
      </div>

      <div className="flex-1 pt-8">
        {indicatorData.length > 0 ? (
          <ChartContainer
            data={indicatorData}
            type="line"
            showVolume={false}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-muted-foreground text-sm flex-col gap-2">
            <span>No indicator data available</span>
            <span className="text-xs">Select an indicator from settings.</span>
          </div>
        )}
      </div>
    </div>
  );
};

export const technicalIndicatorsPanelDefinition: PanelDefinition = {
  id: 'technical-indicators',
  type: 'TechnicalIndicators',
  title: 'Indicators',
  category: 'technical',
  description: 'Displays technical analysis overlays like RSI, MACD.',
  defaultSize: 'medium',
  icon: 'Activity',
  configurationSchema: {
    type: 'object',
    properties: {
      symbol: { type: 'string', default: 'RELIANCE', title: 'Symbol' },
      exchange: { type: 'string', default: 'NSE', title: 'Exchange' },
      indicatorType: { type: 'string', default: 'rsi', enum: ['rsi', 'macd', 'vwap', 'sma', 'ema'], title: 'Indicator' },
      interval: { type: 'string', default: '1d', title: 'Timeframe' },
      endpoint: { type: 'string', default: 'indicator', title: 'Endpoint (Internal)' }
    },
    required: ['symbol', 'indicatorType']
  },
  dataRequirements: [{ type: 'ohlcv' }],
  component: TechnicalIndicatorsPanel
};
