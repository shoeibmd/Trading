import React, { useState } from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { formatCurrency, getTrendIndicator } from '../../../utils/fundamentalsUtils';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

export const FinancialStatementsPanel: React.FC<PanelProps> = () => {
  const { state, configuration, onConfigurationChange } = usePanelContext();
  const [statementType, setStatementType] = useState(configuration.statementType || 'income');
  const [periodType, setPeriodType] = useState(configuration.periodType || 'annual');

  const statements = Array.isArray(state.data) ? state.data : [];

  // Update configuration when local state changes so usePanelData refetches
  const handleTypeChange = (type: string) => {
    setStatementType(type);
    onConfigurationChange({ ...configuration, statementType: type });
  };

  const handlePeriodChange = (period: string) => {
    setPeriodType(period);
    onConfigurationChange({ ...configuration, periodType: period });
  };

  if (!statements || statements.length === 0) return (
    <div className="w-full h-full flex items-center justify-center text-muted-foreground text-sm">
      No statement data available.
    </div>
  );

  // Get all unique keys from all statements to build rows
  const allKeys = new Set<string>();
  statements.forEach((stmt: any) => {
    if (stmt.items) Object.keys(stmt.items).forEach(k => allKeys.add(k));
  });

  // Sort keys arbitrarily or use a predefined sort list if available
  const sortedKeys = Array.from(allKeys).sort();

  return (
    <div className="w-full h-full flex flex-col bg-background">
      <div className="flex justify-between items-center p-2 border-b">
        <div className="flex gap-2">
          <select
            className="text-sm bg-muted rounded-md px-2 py-1 border-none outline-none"
            value={statementType}
            onChange={(e) => handleTypeChange(e.target.value)}
          >
            <option value="income">Income Statement</option>
            <option value="balance">Balance Sheet</option>
            <option value="cashflow">Cash Flow</option>
          </select>
          <select
            className="text-sm bg-muted rounded-md px-2 py-1 border-none outline-none"
            value={periodType}
            onChange={(e) => handlePeriodChange(e.target.value)}
          >
            <option value="annual">Annual</option>
            <option value="quarterly">Quarterly</option>
          </select>
        </div>
      </div>

      <div className="flex-1 overflow-auto">
        <table className="w-full text-sm text-left whitespace-nowrap">
          <thead className="text-xs text-muted-foreground bg-muted/30 sticky top-0">
            <tr>
              <th className="px-4 py-2 font-medium sticky left-0 bg-muted/90 backdrop-blur-md">Item</th>
              {statements.map((stmt: any, i: number) => (
                <th key={i} className="px-4 py-2 font-medium text-right min-w-[120px]">
                  {stmt.fiscal_year} {stmt.fiscal_quarter ? `Q${stmt.fiscal_quarter}` : ''}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border/50">
            {sortedKeys.map(key => (
              <tr key={key} className="hover:bg-muted/10 transition-colors">
                <td className="px-4 py-2 font-medium text-foreground sticky left-0 bg-background/90 backdrop-blur-md capitalize">
                  {key.replace(/([A-Z])/g, ' $1').trim()}
                </td>
                {statements.map((stmt: any, i: number) => {
                  const val = stmt.items?.[key];
                  const prevVal = i < statements.length - 1 ? statements[i+1].items?.[key] : undefined;
                  const trend = prevVal ? getTrendIndicator(val, prevVal) : 'neutral';

                  return (
                    <td key={i} className="px-4 py-2 text-right">
                      <div className="flex items-center justify-end gap-2">
                        {trend === 'up' && <TrendingUp className="h-3 w-3 text-green-500 opacity-70" />}
                        {trend === 'down' && <TrendingDown className="h-3 w-3 text-red-500 opacity-70" />}
                        {trend === 'neutral' && <Minus className="h-3 w-3 text-muted-foreground opacity-50" />}
                        <span>{val ? formatCurrency(val, stmt.currency || 'USD') : '-'}</span>
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export const financialStatementsPanelDefinition: PanelDefinition = {
  id: 'financial-statements',
  type: 'FinancialStatements',
  title: 'Financial Statements',
  category: 'fundamentals',
  description: 'Income Statement, Balance Sheet, and Cash Flow.',
  defaultSize: 'large',
  icon: 'TableProperties',
  configurationSchema: {
    type: 'object',
    properties: {
      symbol: { type: 'string', default: 'RELIANCE', title: 'Symbol' },
      statementType: { type: 'string', default: 'income', enum: ['income', 'balance', 'cashflow'] },
      periodType: { type: 'string', default: 'annual', enum: ['annual', 'quarterly'] },
      endpoint: { type: 'string', default: 'fundamentals-statements', title: 'Endpoint' }
    },
    required: ['symbol']
  },
  dataRequirements: [{ type: 'fundamentals' } as any],
  component: FinancialStatementsPanel
};
