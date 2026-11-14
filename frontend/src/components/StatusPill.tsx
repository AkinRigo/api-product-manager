import type { Product } from '../types/api';
import { isLowStock } from '../utils/format';

export function StatusPill({ product }: { product: Product }) {
  const label = !product.is_active ? 'Inativo' : isLowStock(product) ? 'Estoque baixo' : 'Ativo';
  const tone = !product.is_active ? '' : isLowStock(product) ? ' bad' : ' ok';
  return <span className={`pill${tone}`}>{label}</span>;
}

export function MovementPill({ label, tone }: { label: string; tone: 'ok' | 'bad' | 'warn' }) {
  return <span className={`pill ${tone}`}>{label}</span>;
}
