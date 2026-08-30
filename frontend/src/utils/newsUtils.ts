export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
}

export function truncateText(text: string, maxLength: number): string {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength).trim() + '...';
}

export function getSentimentColor(sentiment: number | null | undefined): string {
  if (sentiment === null || sentiment === undefined) return 'bg-muted text-muted-foreground';
  if (sentiment > 0.3) return 'bg-green-500/20 text-green-600 dark:text-green-400';
  if (sentiment < -0.3) return 'bg-red-500/20 text-red-600 dark:text-red-400';
  return 'bg-yellow-500/20 text-yellow-600 dark:text-yellow-400';
}
