import { useCallback, useEffect, useMemo, useState } from 'react';
import { api, ApiError } from './services/api';
import type { Category, MovementPayload, Product, ProductPayload, StockMovement } from './types/api';
import { Header, type ViewKey } from './components/Header';
import { Modal } from './components/Modal';
import { Toast } from './components/Toast';
import { CategoryForm } from './components/forms/CategoryForm';
import { MovementForm } from './components/forms/MovementForm';
import { ProductForm } from './components/forms/ProductForm';
import { DashboardView } from './views/DashboardView';
import { ProductsView } from './views/ProductsView';
import { CategoriesView } from './views/CategoriesView';
import { StockView } from './views/StockView';

type ModalState = { kind: 'product'; product?: Product } | { kind: 'category'; category?: Category } | { kind: 'movement'; productId?: number } | { kind: 'confirm'; title: string; message: string; action: () => Promise<boolean> } | null;
type ToastState = { message: string; kind: 'ok' | 'bad' } | null;
const pageText: Record<ViewKey, [string, string]> = { dashboard: ['Visão geral', 'Resumo da operação de estoque'], products: ['Produtos', 'Cadastro, busca e controle de saldo'], categories: ['Categorias', 'Organize o catálogo'], stock: ['Estoque', 'Entradas, saídas e ajustes'] };

function App() {
  const [view, setView] = useState<ViewKey>('dashboard'); const [categories, setCategories] = useState<Category[]>([]); const [products, setProducts] = useState<Product[]>([]); const [movements, setMovements] = useState<StockMovement[]>([]); const [loading, setLoading] = useState(true); const [dark, setDark] = useState(false); const [modal, setModal] = useState<ModalState>(null); const [toast, setToast] = useState<ToastState>(null);
  const showError = useCallback((error: unknown) => { if (error instanceof ApiError) setToast({ kind: 'bad', message: `${error.status ? `${error.status} · ` : ''}${error.message}` }); else setToast({ kind: 'bad', message: error instanceof Error ? error.message : 'Erro inesperado' }); }, []);
  const loadData = useCallback(async () => { const [nextCategories, nextProducts, nextMovements] = await Promise.all([api.categories(), api.products(), api.stock()]); setCategories(nextCategories); setProducts(nextProducts); setMovements([...nextMovements].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())); }, []);
  useEffect(() => { loadData().catch(showError).finally(() => setLoading(false)); }, [loadData, showError]);
  useEffect(() => { document.documentElement.dataset.theme = dark ? 'dark' : 'light'; }, [dark]);
  const mutate = useCallback(async (operation: () => Promise<unknown>, successMessage: string): Promise<boolean> => { try { await operation(); await loadData(); setToast({ kind: 'ok', message: successMessage }); return true; } catch (error) { showError(error); return false; } }, [loadData, showError]);
  const submitProduct = async (data: Required<ProductPayload>) => modal && modal.kind === 'product' && modal.product ? mutate(() => api.updateProduct(modal.product!.id, data), 'Produto atualizado') : mutate(() => api.createProduct(data), 'Produto criado');
  const submitCategory = async (data: { name: string; description?: string | null }) => modal && modal.kind === 'category' && modal.category ? mutate(() => api.updateCategory(modal.category!.id, data), 'Categoria atualizada') : mutate(() => api.createCategory(data), 'Categoria criada');
  const submitMovement = (data: MovementPayload) => mutate(() => api.createMovement(data), 'Movimentação registrada');
  const deleteProduct = (product: Product) => setModal({ kind: 'confirm', title: 'Confirmar exclusão', message: `Excluir o produto “${product.name}”?`, action: () => mutate(() => api.deleteProduct(product.id), 'Produto excluído') });
  const deleteCategory = (category: Category) => setModal({ kind: 'confirm', title: 'Confirmar exclusão', message: `Excluir a categoria “${category.name}”?`, action: () => mutate(() => api.deleteCategory(category.id), 'Categoria excluída') });
  const toggleProduct = (product: Product) => { void mutate(() => api.updateProduct(product.id, { is_active: !product.is_active }), product.is_active ? 'Produto inativado' : 'Produto ativado'); };
  const closeModal = () => setModal(null);
  const body = useMemo(() => { if (loading) return <p className="muted">Carregando…</p>; if (view === 'dashboard') return <DashboardView products={products} categories={categories} movements={movements} onGoToStock={() => setView('stock')} />; if (view === 'products') return <ProductsView products={products} categories={categories} onMove={(productId) => setModal({ kind: 'movement', productId })} onEdit={(product) => setModal({ kind: 'product', product })} onToggle={toggleProduct} onDelete={deleteProduct} />; if (view === 'categories') return <CategoriesView categories={categories} products={products} onEdit={(category) => setModal({ kind: 'category', category })} onDelete={deleteCategory} />; return <StockView products={products} movements={movements} />; }, [categories, loading, movements, products, view]);
  function createModal() { if (view === 'products') setModal({ kind: 'product' }); else if (view === 'categories') setModal({ kind: 'category' }); else setModal({ kind: 'movement' }); }
  return <><Header view={view} dark={dark} onViewChange={setView} onThemeChange={() => setDark((value) => !value)} onCreate={createModal} /><main><div className="heading"><h1>{pageText[view][0]}</h1><p>{pageText[view][1]}</p></div>{body}</main>{modal?.kind === 'product' && <Modal title={modal.product ? 'Editar produto' : 'Novo produto'} onClose={closeModal}><ProductForm product={modal.product} categories={categories} onSubmit={submitProduct} onClose={closeModal} /></Modal>}{modal?.kind === 'category' && <Modal title={modal.category ? 'Editar categoria' : 'Nova categoria'} onClose={closeModal}><CategoryForm category={modal.category} onSubmit={submitCategory} onClose={closeModal} /></Modal>}{modal?.kind === 'movement' && <Modal title="Nova movimentação" onClose={closeModal}><MovementForm products={products} productId={modal.productId} onSubmit={submitMovement} onClose={closeModal} /></Modal>}{modal?.kind === 'confirm' && <Modal title={modal.title} onClose={closeModal}><p>{modal.message}</p><div className="form-actions"><button className="button" onClick={closeModal}>Cancelar</button><button className="button primary" onClick={async () => { const success = await modal.action(); if (success) closeModal(); }}>Confirmar</button></div></Modal>}{toast && <Toast message={toast.message} kind={toast.kind} onClose={() => setToast(null)} />}</>;
}
export default App;
