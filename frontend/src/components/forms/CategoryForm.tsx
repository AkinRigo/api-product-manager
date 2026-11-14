import { useState } from 'react';
import type { Category } from '../../types/api';

interface CategoryFormProps {
  category?: Category;
  onSubmit: (data: { name: string; description?: string | null }) => Promise<boolean>;
  onClose: () => void;
}

export function CategoryForm({ category, onSubmit, onClose }: CategoryFormProps) {
  const [name, setName] = useState(category?.name || '');
  const [description, setDescription] = useState(category?.description || '');

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const saved = await onSubmit({ name, description: description || null });
    if (saved) onClose();
  }

  return (
    <form onSubmit={handleSubmit}>
      <label className="field">Nome da categoria<input className="input" autoFocus required value={name} onChange={(event) => setName(event.target.value)} /></label>
      <label className="field">Descrição (opcional)<textarea className="input" rows={3} value={description} onChange={(event) => setDescription(event.target.value)} /></label>
      <div className="form-actions"><button className="button" type="button" onClick={onClose}>Cancelar</button><button className="button primary" type="submit">Salvar</button></div>
    </form>
  );
}
