import Decimal from 'decimal.js';

export function calculateUnrealizedPnL(quantity: string | number, averageCost: string | number, currentPrice: string | number): Decimal {
  const q = new Decimal(quantity);
  const cost = new Decimal(averageCost);
  const price = new Decimal(currentPrice);
  return price.minus(cost).times(q);
}

export function calculateRealizedPnL(quantity: string | number, averageCost: string | number, sellPrice: string | number, fees: string | number): Decimal {
  const q = new Decimal(quantity);
  const cost = new Decimal(averageCost);
  const price = new Decimal(sellPrice);
  const f = new Decimal(fees);
  return price.minus(cost).times(q).minus(f);
}

export function calculateReturn(currentValue: string | number, costBasis: string | number): Decimal {
  const current = new Decimal(currentValue);
  const cost = new Decimal(costBasis);
  if (cost.isZero()) return new Decimal(0);
  return current.minus(cost).dividedBy(cost);
}

export function formatCurrency(value: Decimal | string | number, currency: string = 'USD'): string {
  const num = new Decimal(value).toNumber();
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
    notation: 'compact',
    maximumFractionDigits: 2
  }).format(num);
}

export function formatPercentage(value: Decimal | string | number): string {
  const num = new Decimal(value).toNumber();
  return `${(num * 100).toFixed(2)}%`;
}

export function getAllocationBreakdown(positions: any[]) {
  // Simple heuristic mapping for Phase 15. In production, maps to `instrument.sector`
  const breakdown: Record<string, number> = {};
  let total = new Decimal(0);

  positions.forEach(p => {
    const val = new Decimal(p.quantity).times(new Decimal(p.average_cost)); // Fallback to avg_cost if live price is missing
    const sector = p.instrument?.sector || 'Other';
    breakdown[sector] = (breakdown[sector] || 0) + val.toNumber();
    total = total.plus(val);
  });

  return Object.entries(breakdown).map(([name, value]) => ({
    name,
    value,
    percentage: total.isZero() ? 0 : (value / total.toNumber()) * 100
  })).sort((a, b) => b.value - a.value);
}
