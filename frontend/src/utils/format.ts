import type { MovementType, Product } from '../types/api';

export const palette = ['var(--c0)', 'var(--c1)', 'var(--c2)', 'var(--c3)', 'var(--c4)'];

export function formatBRL(value: number | string): string {
  return Number(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

export function formatDate(value: string): string {
  return new Date(value).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function isLowStock(product: Product): boolean {
  return product.stock_quantity <= product.min_stock;
}

export function stockPercent(product: Product): number {
  return Math.min(100, (product.stock_quantity / Math.max(1, product.min_stock * 3)) * 100);
}

export const movementLabels: Record<MovementType, { label: string; tone: 'ok' | 'bad' | 'warn' }> = {
  ENTRY: { label: 'Entrada', tone: 'ok' },
  EXIT: { label: 'Saída', tone: 'bad' },
  ADJUSTMENT: { label: 'Ajuste', tone: 'warn' },
};
