import { useState } from 'react';
import type { Category, Product } from '../../types/api';

interface ProductFormProps {
  product?: Product;
  categories: Category[];
  onSubmit: (data: { name: string; sku: string; price: number; category_id: number; min_stock: number; is_active: boolean }) => Promise<boolean>;
  onClose: () => void;
}

export function ProductForm({ product, categories, onSubmit, onClose }: ProductFormProps) {
  const [name, setName] = useState(product?.name || '');
  const [sku, setSku] = useState(product?.sku || '');
  const [price, setPrice] = useState(product ? String(product.price) : '');
  const [categoryId, setCategoryId] = useState(String(product?.category_id || categories[0]?.id || ''));
  const [minStock, setMinStock] = useState(String(product?.min_stock ?? 0));

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const saved = await onSubmit({
      name,
      sku,
      price: Number(price),
      category_id: Number(categoryId),
      min_stock: Number(minStock),
      is_active: product?.is_active ?? true,
    });
    if (saved) onClose();
  }

  return (
    <form onSubmit={handleSubmit}>
      <label className="field">Nome<input className="input" autoFocus required value={name} onChange={(event) => setName(event.target.value)} /></label>
      <div className="form-grid">
        <label className="field">SKU<input className="input" required value={sku} onChange={(event) => setSku(event.target.value)} /></label>
        <label className="field">Preço (R$)<input className="input" required type="number" min="0" step="0.01" value={price} onChange={(event) => setPrice(event.target.value)} /></label>
      </div>
      <div className="form-grid">
        <label className="field">Categoria<select className="input" required value={categoryId} onChange={(event) => setCategoryId(event.target.value)}>{categories.map((category) => <option key={category.id} value={category.id}>{category.name}</option>)}</select></label>
        <label className="field">Estoque mínimo<input className="input" required type="number" min="0" step="1" value={minStock} onChange={(event) => setMinStock(event.target.value)} /></label>
      </div>
      <div className="form-actions"><button className="button" type="button" onClick={onClose}>Cancelar</button><button className="button primary" type="submit">Salvar</button></div>
    </form>
  );
}
