export function formatCurrency(value: string | number, currency: string = 'USD'): string {
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return 'N/A';

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
    notation: 'compact',
    maximumFractionDigits: 2
  }).format(num);
}

export function formatPercentage(value: string | number): string {
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return 'N/A';

  return `${(num * 100).toFixed(2)}%`;
}

export function formatNumber(value: string | number): string {
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return 'N/A';

  return new Intl.NumberFormat('en-US', {
    notation: 'compact',
    maximumFractionDigits: 2
  }).format(num);
}

export function getTrendIndicator(current: string | number, previous: string | number): 'up' | 'down' | 'neutral' {
  const c = typeof current === 'string' ? parseFloat(current) : current;
  const p = typeof previous === 'string' ? parseFloat(previous) : previous;

  if (isNaN(c) || isNaN(p)) return 'neutral';
  if (c > p) return 'up';
  if (c < p) return 'down';
  return 'neutral';
}

export function getRatioStatus(ratio: string, value: string | number): 'good' | 'warning' | 'bad' {
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return 'neutral' as any;

  // Simple heuristic logic for mock presentation
  if (ratio === 'pe_ratio') {
    if (num < 15) return 'good';
    if (num > 30) return 'bad';
    return 'warning';
  }

  if (ratio === 'debt_to_equity') {
    if (num < 0.5) return 'good';
    if (num > 1.5) return 'bad';
    return 'warning';
  }

  if (ratio === 'roe') {
     if (num > 0.15) return 'good';
     if (num < 0.05) return 'bad';
     return 'warning';
  }

  return 'neutral' as any;
}
