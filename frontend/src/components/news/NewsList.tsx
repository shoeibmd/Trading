import React from 'react';
import { formatDate, truncateText, getSentimentColor } from '../../utils/newsUtils';

interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  source: string;
  published_at: string;
  sentiment?: number;
}

interface NewsListProps {
  articles: NewsArticle[];
  showSummary?: boolean;
  onArticleClick?: (articleId: string) => void;
}

export const NewsList: React.FC<NewsListProps> = ({ articles, showSummary = true, onArticleClick }) => {
  if (!articles || articles.length === 0) {
    return <div className="text-center p-4 text-muted-foreground text-sm">No news articles found.</div>;
  }

  return (
    <div className="flex flex-col divide-y divide-border/50 h-full w-full">
      {articles.map((article) => (
        <div
          key={article.id}
          className="p-3 hover:bg-muted/30 cursor-pointer transition-colors"
          onClick={() => onArticleClick && onArticleClick(article.id)}
        >
          <div className="flex justify-between items-start mb-1 gap-2">
            <h4 className="font-semibold text-sm leading-tight text-foreground line-clamp-2 flex-1">
              {article.title}
            </h4>
            {article.sentiment !== undefined && (
              <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded-sm shrink-0 ${getSentimentColor(article.sentiment)}`}>
                {article.sentiment > 0.3 ? 'Bullish' : article.sentiment < -0.3 ? 'Bearish' : 'Neutral'}
              </span>
            )}
          </div>

          {showSummary && article.summary && (
            <p className="text-xs text-muted-foreground line-clamp-2 mb-2">
              {truncateText(article.summary, 150)}
            </p>
          )}

          <div className="flex justify-between items-center text-[10px] text-muted-foreground font-medium uppercase tracking-wider">
            <span>{article.source}</span>
            <span>{formatDate(article.published_at)}</span>
          </div>
        </div>
      ))}
    </div>
  );
};
