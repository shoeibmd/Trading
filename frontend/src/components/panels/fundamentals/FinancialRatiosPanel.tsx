import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { getRatioStatus } from '../../../utils/fundamentalsUtils';

export const FinancialRatiosPanel: React.FC<PanelProps> = () => {
  const { state } = usePanelContext();

  const ratios = Array.isArray(state.data) && state.data.length > 0 ? state.data[0] : null;

  if (!ratios) return <div className="p-4 text-center text-sm text-muted-foreground">No ratio data available.</div>;

  const displayRatios = [
    { key: 'pe_ratio', label: 'P/E Ratio', format: 'number' },
    { key: 'pb_ratio', label: 'P/B Ratio', format: 'number' },
    { key: 'roe', label: 'ROE', format: 'percent' },
    { key: 'roa', label: 'ROA', format: 'percent' },
    { key: 'debt_to_equity', label: 'Debt/Equity', format: 'number' },
    { key: 'current_ratio', label: 'Current Ratio', format: 'number' },
    { key: 'gross_margin', label: 'Gross Margin', format: 'percent' },
    { key: 'net_margin', label: 'Net Margin', format: 'percent' }
  ];

  return (
    <div className="w-full h-full p-4 overflow-y-auto bg-background">
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {displayRatios.map(r => {
          const val = ratios[r.key];
          if (val === undefined || val === null) return null;

          const num = parseFloat(val);
          const formatted = r.format === 'percent' ? `${(num * 100).toFixed(2)}%` : num.toFixed(2);
          const status = getRatioStatus(r.key, val);

          const statusColors = {
            good: 'text-green-500 bg-green-500/10 border-green-500/20',
            warning: 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20',
            bad: 'text-red-500 bg-red-500/10 border-red-500/20',
            neutral: 'text-foreground bg-muted border-border'
          };

          return (
            <div key={r.key} className={`flex flex-col p-3 rounded-lg border ${statusColors[status]}`}>
              <span className="text-[10px] uppercase font-semibold tracking-wider opacity-80 mb-1">{r.label}</span>
              <span className="text-xl font-bold">{formatted}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export const financialRatiosPanelDefinition: PanelDefinition = {
  id: 'financial-ratios',
  type: 'FinancialRatios',
  title: 'Financial Ratios',
  category: 'fundamentals',
  description: 'Key valuation, profitability, and liquidity ratios.',
  defaultSize: 'medium',
  icon: 'Percent',
  configurationSchema: {
    type: 'object',
    properties: {
      symbol: { type: 'string', default: 'RELIANCE', title: 'Symbol' },
      periodType: { type: 'string', default: 'annual', enum: ['annual', 'quarterly'] },
      endpoint: { type: 'string', default: 'fundamentals-ratios', title: 'Endpoint' }
    },
    required: ['symbol']
  },
  dataRequirements: [{ type: 'fundamentals' } as any],
  component: FinancialRatiosPanel
};
