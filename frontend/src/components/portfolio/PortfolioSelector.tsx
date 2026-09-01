import React, { useState, useEffect } from 'react';
import { useWorkspaceStore } from '../../store/useWorkspaceStore';
// Using the same API methods just routed properly
import { apiClient } from '../../services/apiClient';

export const PortfolioSelector: React.FC<{
  portfolioId: string;
  onChange: (id: string) => void;
}> = ({ portfolioId, onChange }) => {
  const [portfolios, setPortfolios] = useState<any[]>([]);

  useEffect(() => {
    // In a real app this would be in a usePortfolioStore, just doing basic fetch here
    apiClient.get('/api/v1/portfolios/').then(res => {
      setPortfolios(res.data.data || res.data);
    }).catch(console.error);
  }, []);

  return (
    <select
      className="bg-transparent border-none text-xs focus:ring-0 cursor-pointer text-foreground"
      value={portfolioId}
      onChange={(e) => onChange(e.target.value)}
    >
      <option value="" disabled>Select Portfolio</option>
      {portfolios.map(p => (
        <option key={p.id} value={p.id}>{p.name}</option>
      ))}
    </select>
  );
};
