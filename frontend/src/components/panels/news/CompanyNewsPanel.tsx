import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { NewsList } from '../../news/NewsList';

export const CompanyNewsPanel: React.FC<PanelProps> = () => {
  const { state, configuration } = usePanelContext();

  const articles = Array.isArray(state.data) ? state.data : [];

  return (
    <div className="w-full h-full flex flex-col bg-background relative">
      <div className="h-8 border-b flex items-center px-3 text-xs text-muted-foreground gap-2 z-10 sticky top-0 bg-background/90 backdrop-blur-sm">
        <span className="font-semibold text-foreground">{configuration.symbol || 'All Instruments'}</span>
        <span>News</span>
      </div>
      <div className="flex-1 overflow-y-auto">
        <NewsList
          articles={articles}
          showSummary={configuration.showSummary !== false}
        />
      </div>
    </div>
  );
};

export const companyNewsPanelDefinition: PanelDefinition = {
  id: 'company-news',
  type: 'CompanyNews',
  title: 'Company News',
  category: 'news',
  description: 'Displays news specific to an instrument.',
  defaultSize: 'medium',
  icon: 'Newspaper',
  configurationSchema: {
    type: 'object',
    properties: {
      symbol: { type: 'string', default: 'RELIANCE', title: 'Symbol/Instrument ID' },
      limit: { type: 'number', default: 20, title: 'Number of articles' },
      showSummary: { type: 'boolean', default: true, title: 'Show Summary' },
      endpoint: { type: 'string', default: 'news-company', title: 'Endpoint' }
    },
    required: ['symbol']
  },
  dataRequirements: [{ type: 'news' }],
  component: CompanyNewsPanel
};
