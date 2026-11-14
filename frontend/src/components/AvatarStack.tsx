import type { Product } from '../types/api';
import { Avatar } from './Avatar';

interface AvatarStackProps {
  products: Product[];
}

export function AvatarStack({ products }: AvatarStackProps) {
  const visible = products.slice(0, 5);
  return (
    <div className="avatar-stack" aria-label={`${products.length} produtos`}>
      {visible.map((product) => (
        <Avatar key={product.id} id={product.id} name={product.name} />
      ))}
      {products.length > 5 && <span className="avatar avatar-more">+{products.length - 5}</span>}
    </div>
  );
}
