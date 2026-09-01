import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { PortfolioSelector } from '../../portfolio/PortfolioSelector';
import { formatCurrency, formatPercentage } from '../../../utils/portfolioUtils';
import Decimal from 'decimal.js';

export const PortfolioSummaryPanel: React.FC<PanelProps> = () => {
  const { state, configuration, onConfigurationChange } = usePanelContext();

  const summary = state.data;

  if (!summary) return <div className="p-4 text-center text-sm text-muted-foreground">No portfolio summary available.</div>;

  const marketValue = new Decimal(summary.total_market_value || 0);
  const costBasis = new Decimal(summary.total_cost_basis || 0);
  const unrealized = new Decimal(summary.total_unrealized_pnl || 0);
  const realized = new Decimal(summary.total_realized_pnl || 0);

  const returnPct = costBasis.isZero() ? new Decimal(0) : marketValue.minus(costBasis).dividedBy(costBasis);
  const isUp = returnPct.gte(0);

  return (
    <div className="w-full h-full flex flex-col bg-background relative">
      <div className="h-8 border-b flex items-center px-2 text-xs text-muted-foreground gap-2 z-10 sticky top-0 bg-background/90 backdrop-blur-sm">
        <span className="font-semibold text-foreground">Summary</span>
        <span>|</span>
        <PortfolioSelector
          portfolioId={configuration.portfolioId}
          onChange={(id) => onConfigurationChange({ ...configuration, portfolioId: id })}
        />
      </div>

      <div className="p-6 flex-1 overflow-y-auto">
        <div className="mb-8 text-center">
          <p className="text-sm text-muted-foreground uppercase tracking-wider font-semibold mb-1">Total Market Value</p>
          <h2 className="text-4xl font-bold">{formatCurrency(marketValue)}</h2>
          <div className={`text-sm font-medium mt-2 flex justify-center items-center gap-2 ${isUp ? 'text-green-500' : 'text-red-500'}`}>
            <span>{isUp ? '+' : ''}{formatCurrency(marketValue.minus(costBasis))}</span>
            <span className="bg-muted px-2 py-0.5 rounded-full">
              {isUp ? '+' : ''}{formatPercentage(returnPct)} All Time
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 rounded-lg border bg-muted/20 text-center">
            <p className="text-xs text-muted-foreground uppercase font-semibold mb-1">Cost Basis</p>
            <p className="text-lg font-bold">{formatCurrency(costBasis)}</p>
          </div>
          <div className="p-4 rounded-lg border bg-muted/20 text-center">
            <p className="text-xs text-muted-foreground uppercase font-semibold mb-1">Unrealized P&L</p>
            <p className={`text-lg font-bold ${unrealized.gte(0) ? 'text-green-500' : 'text-red-500'}`}>
              {unrealized.gte(0) ? '+' : ''}{formatCurrency(unrealized)}
            </p>
          </div>
          <div className="p-4 rounded-lg border bg-muted/20 text-center col-span-2">
            <p className="text-xs text-muted-foreground uppercase font-semibold mb-1">Realized P&L</p>
            <p className={`text-lg font-bold ${realized.gte(0) ? 'text-green-500' : 'text-red-500'}`}>
              {realized.gte(0) ? '+' : ''}{formatCurrency(realized)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export const portfolioSummaryPanelDefinition: PanelDefinition = {
  id: 'portfolio-summary',
  type: 'PortfolioSummary',
  title: 'Portfolio Summary',
  category: 'portfolio',
  description: 'Displays aggregate valuation and performance metrics.',
  defaultSize: 'medium',
  icon: 'PieChart',
  configurationSchema: {
    type: 'object',
    properties: {
      portfolioId: { type: 'string', title: 'Portfolio ID' },
      endpoint: { type: 'string', default: 'portfolio-summary' }
    }
  },
  dataRequirements: [{ type: 'portfolio' } as any],
  component: PortfolioSummaryPanel
};
