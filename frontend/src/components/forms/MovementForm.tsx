import { useState } from 'react';
import type { MovementType, Product } from '../../types/api';
import { movementLabels } from '../../utils/format';

interface MovementFormProps {
  products: Product[];
  productId?: number;
  onSubmit: (data: { product_id: number; type: MovementType; quantity: number; reason: string | null }) => Promise<boolean>;
  onClose: () => void;
}

export function MovementForm({ products, productId, onSubmit, onClose }: MovementFormProps) {
  const [selectedProduct, setSelectedProduct] = useState(String(productId || products[0]?.id || ''));
  const [type, setType] = useState<MovementType>('ENTRY');
  const [quantity, setQuantity] = useState('');
  const [reason, setReason] = useState('');
  const product = products.find((item) => item.id === Number(selectedProduct));
  const adjustment = type === 'ADJUSTMENT';

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const saved = await onSubmit({ product_id: Number(selectedProduct), type, quantity: Number(quantity), reason: reason || null });
    if (saved) onClose();
  }

  return (
    <form onSubmit={handleSubmit}>
      <label className="field">Produto<select className="input" required value={selectedProduct} onChange={(event) => setSelectedProduct(event.target.value)}>{products.map((item) => <option key={item.id} value={item.id}>{item.name} ({item.sku}){item.is_active ? '' : ' · inativo'}</option>)}</select></label>
      <div className="segmented">{(Object.keys(movementLabels) as MovementType[]).map((key) => <button key={key} type="button" className={`chip${type === key ? ' active' : ''}`} onClick={() => setType(key)}>{movementLabels[key].label}</button>)}</div>
      <label className="field">{adjustment ? 'Novo saldo' : 'Quantidade'}{product ? ` · saldo atual: ${product.stock_quantity}` : ''}<input className="input" required type="number" min="0" step="1" value={quantity} onChange={(event) => setQuantity(event.target.value)} /></label>
      <label className="field">Motivo {adjustment ? '(obrigatório)' : '(opcional)'}<input className="input" required={adjustment} value={reason} onChange={(event) => setReason(event.target.value)} /></label>
      <div className="form-actions"><button className="button" type="button" onClick={onClose}>Cancelar</button><button className="button primary" type="submit">Registrar</button></div>
    </form>
  );
}
