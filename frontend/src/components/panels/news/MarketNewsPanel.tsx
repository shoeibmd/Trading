import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { NewsList } from '../../news/NewsList';

export const MarketNewsPanel: React.FC<PanelProps> = () => {
  const { state, configuration } = usePanelContext();

  const articles = Array.isArray(state.data) ? state.data : [];

  return (
    <div className="w-full h-full overflow-y-auto bg-background">
      <NewsList
        articles={articles}
        showSummary={configuration.showSummary !== false}
      />
    </div>
  );
};

export const marketNewsPanelDefinition: PanelDefinition = {
  id: 'market-news',
  type: 'MarketNews',
  title: 'Market News',
  category: 'news',
  description: 'Displays the latest breaking market and macroeconomic news.',
  defaultSize: 'medium',
  icon: 'Globe',
  configurationSchema: {
    type: 'object',
    properties: {
      limit: { type: 'number', default: 20, title: 'Number of articles' },
      showSummary: { type: 'boolean', default: true, title: 'Show Summary' },
      endpoint: { type: 'string', default: 'news-market', title: 'Endpoint' },
      wsTopic: { type: 'string', default: 'news:market', title: 'WebSocket Topic' }
    }
  },
  dataRequirements: [{ type: 'news' }],
  component: MarketNewsPanel
};
