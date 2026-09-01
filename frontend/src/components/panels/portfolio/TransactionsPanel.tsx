import React, { useState } from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { PortfolioSelector } from '../../portfolio/PortfolioSelector';
import { AddTransactionModal } from '../../portfolio/AddTransactionModal';
import { formatCurrency } from '../../../utils/portfolioUtils';
import { Button } from '../../ui/button';
import { Plus } from 'lucide-react';

export const TransactionsPanel: React.FC<PanelProps> = () => {
  const { state, configuration, onConfigurationChange } = usePanelContext();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const transactions = Array.isArray(state.data) ? state.data : [];

  return (
    <div className="w-full h-full bg-background flex flex-col relative">
      <div className="h-8 border-b flex items-center justify-between px-2 text-xs text-muted-foreground z-10 sticky top-0 bg-background/90 backdrop-blur-sm">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-foreground">Transactions</span>
          <span>|</span>
          <PortfolioSelector
            portfolioId={configuration.portfolioId}
            onChange={(id) => onConfigurationChange({ ...configuration, portfolioId: id })}
          />
        </div>
        <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => setIsModalOpen(true)}>
          <Plus className="h-4 w-4" />
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-[10px] text-muted-foreground bg-muted/30 sticky top-0 uppercase tracking-wider">
            <tr>
              <th className="px-3 py-2 font-medium">Date</th>
              <th className="px-3 py-2 font-medium">Type</th>
              <th className="px-3 py-2 font-medium">Symbol</th>
              <th className="px-3 py-2 font-medium text-right">Qty</th>
              <th className="px-3 py-2 font-medium text-right">Price</th>
              <th className="px-3 py-2 font-medium text-right">Total</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/50">
            {transactions.map((tx: any) => {
              const qty = parseFloat(tx.quantity);
              const price = parseFloat(tx.price);
              const total = (qty * price) + parseFloat(tx.fees);

              const typeColors: Record<string, string> = {
                BUY: 'text-green-500 bg-green-500/10',
                SELL: 'text-red-500 bg-red-500/10',
                DIVIDEND: 'text-blue-500 bg-blue-500/10'
              };

              return (
                <tr key={tx.id} className="hover:bg-muted/30 transition-colors">
                  <td className="px-3 py-2 text-muted-foreground">
                    {new Date(tx.transaction_date).toLocaleDateString()}
                  </td>
                  <td className="px-3 py-2">
                    <span className={`px-1.5 py-0.5 rounded-sm text-[10px] font-bold ${typeColors[tx.transaction_type] || 'bg-muted'}`}>
                      {tx.transaction_type}
                    </span>
                  </td>
                  <td className="px-3 py-2 font-semibold">{tx.instrument_id.substring(0, 8)}...</td>
                  <td className="px-3 py-2 text-right">{tx.quantity}</td>
                  <td className="px-3 py-2 text-right">{formatCurrency(tx.price)}</td>
                  <td className="px-3 py-2 text-right font-medium">{formatCurrency(total)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {isModalOpen && (
        <AddTransactionModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          portfolioId={configuration.portfolioId}
        />
      )}
    </div>
  );
};

export const transactionsPanelDefinition: PanelDefinition = {
  id: 'portfolio-transactions',
  type: 'Transactions',
  title: 'Transaction History',
  category: 'portfolio',
  description: 'Displays a chronological list of portfolio transactions.',
  defaultSize: 'large',
  icon: 'History',
  configurationSchema: {
    type: 'object',
    properties: {
      portfolioId: { type: 'string', title: 'Portfolio ID' },
      endpoint: { type: 'string', default: 'portfolio-transactions' }
    }
  },
  dataRequirements: [{ type: 'portfolio' } as any],
  component: TransactionsPanel
};
