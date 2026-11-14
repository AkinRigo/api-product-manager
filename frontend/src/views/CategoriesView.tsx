import type { Category, Product } from '../types/api';
import { Avatar } from '../components/Avatar';
import { AvatarStack } from '../components/AvatarStack';

interface CategoriesViewProps { categories: Category[]; products: Product[]; onEdit: (category: Category) => void; onDelete: (category: Category) => void; }
export function CategoriesView({ categories, products, onEdit, onDelete }: CategoriesViewProps) { return <div className="cards-grid">{categories.map((category) => { const linked = products.filter((product) => product.category_id === category.id); return <article className="panel category-card" key={category.id}><div className="card-top"><Avatar id={category.id} name={category.name} large /></div><b>{category.name}</b><small>{linked.length} produto{linked.length === 1 ? '' : 's'}</small>{linked.length > 0 && <AvatarStack products={linked} />}<div className="card-actions"><button className="link-button" onClick={() => onEdit(category)}>Editar</button><button className="link-button danger" onClick={() => onDelete(category)}>Excluir</button></div></article>; })}{!categories.length && <p className="empty-state">Nenhuma categoria cadastrada.</p>}</div>; }
