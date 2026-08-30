import React, { useState, useEffect } from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { Search } from 'lucide-react';
import { Input } from '../../ui/input';
import { NewsList } from '../../news/NewsList';
import { useDebounce } from '../../../hooks/useDebounce';

// Reusing generic debounce if it exists, otherwise implement simple one inline
export function useDebouncedValue<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  return debouncedValue;
}

export const NewsSearchPanel: React.FC<PanelProps> = () => {
  const { state, configuration, onConfigurationChange } = usePanelContext();
  const [localQuery, setLocalQuery] = useState(configuration.query || '');

  const debouncedQuery = useDebouncedValue(localQuery, 500);

  // Sync back to config for usePanelData to catch the change
  useEffect(() => {
    if (debouncedQuery !== configuration.query) {
      onConfigurationChange({ ...configuration, query: debouncedQuery });
    }
  }, [debouncedQuery, configuration, onConfigurationChange]);

  const articles = Array.isArray(state.data) ? state.data : [];

  return (
    <div className="w-full h-full flex flex-col bg-background relative">
      <div className="p-2 border-b sticky top-0 bg-background z-10">
        <div className="relative">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search news..."
            className="pl-8 h-9 text-sm"
            value={localQuery}
            onChange={(e) => setLocalQuery(e.target.value)}
          />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        {state.status === 'loading' && <div className="p-4 text-center text-sm text-muted-foreground">Searching...</div>}
        {state.status === 'success' && <NewsList articles={articles} showSummary={true} />}
      </div>
    </div>
  );
};

export const newsSearchPanelDefinition: PanelDefinition = {
  id: 'news-search',
  type: 'NewsSearch',
  title: 'News Search',
  category: 'news',
  description: 'Full-text search across all news sources.',
  defaultSize: 'medium',
  icon: 'Search',
  configurationSchema: {
    type: 'object',
    properties: {
      query: { type: 'string', default: 'markets' },
      endpoint: { type: 'string', default: 'news-search' }
    }
  },
  dataRequirements: [{ type: 'news' }],
  component: NewsSearchPanel
};
