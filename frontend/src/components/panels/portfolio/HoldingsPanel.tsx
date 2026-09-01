import React, { useState } from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { PortfolioSelector } from '../../portfolio/PortfolioSelector';
import { formatCurrency, formatPercentage } from '../../../utils/portfolioUtils';
import Decimal from 'decimal.js';

export const HoldingsPanel: React.FC<PanelProps> = () => {
  const { state, configuration, onConfigurationChange } = usePanelContext();

  const positions = Array.isArray(state.data) ? state.data : [];

  return (
    <div className="w-full h-full bg-background flex flex-col relative">
      <div className="h-8 border-b flex items-center px-2 text-xs text-muted-foreground gap-2 z-10 sticky top-0 bg-background/90 backdrop-blur-sm">
        <span className="font-semibold text-foreground">Holdings</span>
        <span>|</span>
        <PortfolioSelector
          portfolioId={configuration.portfolioId}
          onChange={(id) => onConfigurationChange({ ...configuration, portfolioId: id })}
        />
      </div>

      <div className="flex-1 overflow-y-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-[10px] text-muted-foreground bg-muted/30 sticky top-0 uppercase tracking-wider">
            <tr>
              <th className="px-3 py-2 font-medium">Symbol</th>
              <th className="px-3 py-2 font-medium text-right">Qty</th>
              <th className="px-3 py-2 font-medium text-right">Avg Cost</th>
              <th className="px-3 py-2 font-medium text-right">Mkt Price</th>
              <th className="px-3 py-2 font-medium text-right">Unrealized P&L</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/50">
            {positions.map((pos: any) => {
              // Mock live price or fallback to cost if not available
              const livePrice = new Decimal(pos.instrument?.last_price || pos.average_cost);
              const cost = new Decimal(pos.average_cost);
              const qty = new Decimal(pos.quantity);
              const pnl = livePrice.minus(cost).times(qty);
              const isUp = pnl.gte(0);

              return (
                <tr key={pos.id} className="hover:bg-muted/30 transition-colors">
                  <td className="px-3 py-2 font-semibold text-primary">{pos.instrument?.symbol || 'UNKNOWN'}</td>
                  <td className="px-3 py-2 text-right">{pos.quantity}</td>
                  <td className="px-3 py-2 text-right">{formatCurrency(cost)}</td>
                  <td className="px-3 py-2 text-right">{formatCurrency(livePrice)}</td>
                  <td className={`px-3 py-2 text-right font-medium ${isUp ? 'text-green-500' : 'text-red-500'}`}>
                    {isUp ? '+' : ''}{formatCurrency(pnl)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export const holdingsPanelDefinition: PanelDefinition = {
  id: 'portfolio-holdings',
  type: 'Holdings',
  title: 'Portfolio Holdings',
  category: 'portfolio',
  description: 'Displays current holdings with live valuation and P&L.',
  defaultSize: 'large',
  icon: 'Briefcase',
  configurationSchema: {
    type: 'object',
    properties: {
      portfolioId: { type: 'string', title: 'Portfolio ID' },
      endpoint: { type: 'string', default: 'portfolio-positions' }
    }
  },
  dataRequirements: [{ type: 'portfolio' } as any],
  component: HoldingsPanel
};
