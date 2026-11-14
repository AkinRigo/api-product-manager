export interface Category {
  id: number;
  name: string;
  description?: string | null;
  created_at?: string;
}

export interface Product {
  id: number;
  name: string;
  sku: string;
  price: number | string;
  stock_quantity: number;
  min_stock: number;
  is_active: boolean;
  category_id: number;
  created_at?: string;
  updated_at?: string;
}

export type MovementType = 'ENTRY' | 'EXIT' | 'ADJUSTMENT';

export interface StockMovement {
  id: number;
  product_id: number;
  type: MovementType;
  quantity: number;
  reason: string | null;
  stock_before: number;
  stock_after: number;
  created_at: string;
}

export interface CategoryPayload {
  name: string;
  description?: string | null;
}

export interface ProductPayload {
  name?: string;
  sku?: string;
  price?: number;
  category_id?: number;
  min_stock?: number;
  is_active?: boolean;
}

export interface MovementPayload {
  product_id: number;
  type: MovementType;
  quantity: number;
  reason: string | null;
}
