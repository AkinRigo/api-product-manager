import type {
  Category,
  CategoryPayload,
  MovementPayload,
  Product,
  ProductPayload,
  StockMovement,
} from '../types/api';

const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');

type StockMovementResponse = Omit<StockMovement, 'type'> & {
  type?: StockMovement['type'];
  movement_type?: StockMovement['type'];
};

const fieldLabels: Record<string, string> = {
  product_id: 'um produto',
  movement_type: 'o tipo da movimentação',
  quantity: 'a quantidade',
  reason: 'o motivo',
};

function translateMessage(message: string): string {
  const normalized = message.toLowerCase();
  if (normalized.includes('estoque insuficiente')) return 'Não há saldo suficiente para essa saída.';
  if (normalized.includes('inativo')) return 'Produtos inativos não aceitam entradas ou saídas.';
  if (normalized.includes('motivo') || normalized.includes('raz')) return 'Informe um motivo para o ajuste de estoque.';
  if (normalized.includes('quantidade') && normalized.includes('maior')) return 'A quantidade deve ser maior que zero.';
  if (normalized.includes('quantidade')) return 'Informe uma quantidade inteira válida.';
  if (normalized.includes('produto') && normalized.includes('encontr')) return 'Produto não encontrado.';
  if (normalized.includes('categoria') && normalized.includes('uso')) return 'Não é possível excluir uma categoria que possui produtos.';
  if (normalized.includes('sku')) return 'Já existe um produto com este SKU.';
  if (normalized.includes('categoria') && normalized.includes('exist')) return 'A categoria selecionada não existe.';
  return message.replace(/^value error,\s*/i, '');
}

function validationMessage(detail: unknown): string {
  if (typeof detail !== 'object' || detail === null) return 'Revise os dados informados.';
  const item = detail as { msg?: unknown; loc?: unknown[] };
  const message = typeof item.msg === 'string' ? item.msg : '';
  const field = item.loc?.[item.loc.length - 1];
  if (message.toLowerCase() === 'field required' && typeof field === 'string') {
    return `Informe ${fieldLabels[field] || 'este campo'}.`;
  }
  if (message.toLowerCase().includes('json decode error')) return 'Revise os dados informados.';
  return translateMessage(message || 'Revise os dados informados.');
}

function normalizeMovement(movement: StockMovementResponse): StockMovement {
  const type = movement.type ?? movement.movement_type;
  if (!type) throw new ApiError(500, 'A API retornou uma movimentação sem tipo.');
  return { ...movement, type };
}

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...(init?.headers || {}),
      },
    });
  } catch {
    throw new ApiError(0, 'Não foi possível conectar à API.');
  }

  if (!response.ok) {
    const payload = (await response.json().catch(() => ({}))) as { detail?: unknown };
    const detail = Array.isArray(payload.detail)
      ? payload.detail.map(validationMessage).join('; ')
      : typeof payload.detail === 'string'
        ? translateMessage(payload.detail)
        : 'Revise os dados informados.';
    throw new ApiError(response.status, detail);
  }

  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

export const api = {
  categories: () => request<Category[]>('/categories/'),
  createCategory: (body: CategoryPayload) =>
    request<Category>('/categories/', { method: 'POST', body: JSON.stringify(body) }),
  updateCategory: (id: number, body: CategoryPayload) =>
    request<Category>(`/categories/${id}`, { method: 'PATCH', body: JSON.stringify(body) }),
  deleteCategory: (id: number) => request<void>(`/categories/${id}`, { method: 'DELETE' }),

  products: () => request<Product[]>('/products/'),
  createProduct: (body: Required<ProductPayload>) =>
    request<Product>('/products/', { method: 'POST', body: JSON.stringify(body) }),
  updateProduct: (id: number, body: ProductPayload) =>
    request<Product>(`/products/${id}`, { method: 'PATCH', body: JSON.stringify(body) }),
  deleteProduct: (id: number) => request<void>(`/products/${id}`, { method: 'DELETE' }),

  stock: async () => {
    const movements = await request<StockMovementResponse[]>('/stock/');
    return movements.map(normalizeMovement);
  },
  createMovement: async (body: MovementPayload) => {
    const movement = await request<StockMovementResponse>('/stock/', {
      method: 'POST',
      body: JSON.stringify({
        product_id: body.product_id,
        movement_type: body.type,
        quantity: body.quantity,
        reason: body.reason,
      }),
    });
    return normalizeMovement(movement);
  },
};
