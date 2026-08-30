import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { formatDate, getSentimentColor } from '../../utils/newsUtils';
import { ExternalLink, User } from 'lucide-react';
import { Button } from '../../ui/button';

export const NewsArticleDetailPanel: React.FC<PanelProps> = () => {
  const { state } = usePanelContext();

  const article = state.data;

  if (!article) return null;

  return (
    <div className="w-full h-full flex flex-col bg-background relative overflow-y-auto">
      {/* Header */}
      <div className="p-4 border-b space-y-3">
        <div className="flex justify-between items-start gap-4">
          <h2 className="text-xl font-bold leading-tight">{article.title}</h2>
          <Button variant="outline" size="icon" onClick={() => window.open(article.url, '_blank')} title="Open Source">
            <ExternalLink className="h-4 w-4" />
          </Button>
        </div>

        <div className="flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
          <span className="font-semibold text-primary">{article.source}</span>
          <span>{formatDate(article.published_at)}</span>
          {article.author && (
            <span className="flex items-center gap-1">
              <User className="h-3 w-3" />
              {article.author}
            </span>
          )}
          {article.sentiment !== undefined && (
            <span className={`font-medium px-2 py-0.5 rounded-sm ${getSentimentColor(article.sentiment)}`}>
              {article.sentiment > 0.3 ? 'Bullish' : article.sentiment < -0.3 ? 'Bearish' : 'Neutral'}
            </span>
          )}
        </div>
      </div>

      {/* Body */}
      <div className="p-4">
        {article.image_url && (
          <img src={article.image_url} alt="Article" className="w-full h-48 object-cover rounded-md mb-4" />
        )}
        <div className="prose dark:prose-invert prose-sm max-w-none">
          <p className="font-medium text-lg mb-4">{article.summary}</p>
          <div className="whitespace-pre-wrap leading-relaxed opacity-90">{article.content}</div>
        </div>

        {/* Tags / Related */}
        {article.tags && article.tags.length > 0 && (
          <div className="mt-8 pt-4 border-t flex flex-wrap gap-2">
            {article.tags.map((tag: string, i: number) => (
              <span key={i} className="bg-muted px-2 py-1 rounded-md text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export const newsArticleDetailPanelDefinition: PanelDefinition = {
  id: 'news-article-detail',
  type: 'NewsArticleDetail',
  title: 'Article View',
  category: 'news',
  description: 'Displays full news article content.',
  defaultSize: 'large',
  icon: 'FileText',
  configurationSchema: {
    type: 'object',
    properties: {
      articleId: { type: 'string', title: 'Article ID' },
      endpoint: { type: 'string', default: 'news-article' }
    },
    required: ['articleId']
  },
  dataRequirements: [{ type: 'news' }],
  component: NewsArticleDetailPanel
};
