import type { Category, Product, StockMovement } from '../types/api';
import { Avatar } from '../components/Avatar';
import { AvatarStack } from '../components/AvatarStack';
import { MovementPill } from '../components/StatusPill';
import { formatBRL, formatDate, isLowStock, movementLabels, palette } from '../utils/format';

interface DashboardViewProps { products: Product[]; categories: Category[]; movements: StockMovement[]; onGoToStock: () => void; }

export function DashboardView({ products, categories, movements, onGoToStock }: DashboardViewProps) {
  const active = products.filter((product) => product.is_active);
  const lowStock = products.filter(isLowStock);
  const totalUnits = products.reduce((sum, product) => sum + product.stock_quantity, 0);
  const stockValue = products.reduce((sum, product) => sum + Number(product.price) * product.stock_quantity, 0);
  const categoryTotals = categories.map((category, index) => ({ category, index, quantity: products.filter((product) => product.category_id === category.id).reduce((sum, product) => sum + product.stock_quantity, 0) }));
  const productMap = Object.fromEntries(products.map((product) => [product.id, product]));

  return <div>
    <div className="kpi-grid">
      <Kpi background="var(--c0)" label="Produtos ativos" value={active.length} subtitle={`de ${products.length} cadastrados`} products={active} />
      <Kpi background="var(--c2)" label="Categorias" value={categories.length} subtitle="no catálogo" />
      <Kpi background="var(--c3)" label="Valor em estoque" value={formatBRL(stockValue)} subtitle={`${totalUnits} unidades no total`} />
      <Kpi background="var(--c1)" label="Estoque baixo" value={lowStock.length} subtitle="precisam de reposição" products={lowStock} />
    </div>
    <div className="two-column">
      <section className="panel"><h3>Distribuição por categoria</h3><div className="segmented-bar">{categoryTotals.map(({ category, index, quantity }) => <i key={category.id} style={{ flex: quantity || 0.01, background: palette[index % 5] }} />)}</div>{categoryTotals.map(({ category, index, quantity }) => <div className="row" key={category.id}><span className="dot" style={{ background: palette[index % 5] }} /><span>{category.name}</span><small>{quantity} un.</small><b>{totalUnits ? Math.round((quantity / totalUnits) * 100) : 0}%</b></div>)}{!categoryTotals.length && <p className="muted">Nenhuma categoria cadastrada.</p>}</section>
      <section className="panel"><h3>Reposição necessária</h3>{lowStock.length ? lowStock.map((product) => <div className="row" key={product.id}><Avatar id={product.id} name={product.name} /><span>{product.name}<small>{product.sku}</small></span><span className="pill bad">{product.stock_quantity} / mín. {product.min_stock}</span></div>) : <p className="muted">Tudo em dia.</p>}</section>
    </div>
    <section className="panel activity-panel"><h3>Atividade recente</h3>{movements.slice(0, 5).map((movement) => { const product = productMap[movement.product_id]; const fallback = product || { id: 0, name: '?', sku: '' }; const info = movementLabels[movement.type]; return <div className="row" key={movement.id}><Avatar id={fallback.id} name={fallback.name} /><span>{product?.name || 'Produto removido'}<small>{formatDate(movement.created_at)} · {movement.stock_before} → {movement.stock_after}</small></span><MovementPill label={info.label} tone={info.tone} /></div>; })}{!movements.length && <p className="muted">Nenhuma movimentação registrada.</p>}<button className="link-button" onClick={onGoToStock}>Ver histórico completo →</button></section>
  </div>;
}

function Kpi({ background, label, value, subtitle, products }: { background: string; label: string; value: string | number; subtitle: string; products?: Product[] }) { return <article className="kpi" style={{ background }}><span>{label}</span><b>{value}</b><em>{subtitle}</em>{products && <AvatarStack products={products} />}</article>; }
