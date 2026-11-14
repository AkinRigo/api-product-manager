export type ViewKey = 'dashboard' | 'products' | 'categories' | 'stock';

interface HeaderProps {
  view: ViewKey;
  dark: boolean;
  onViewChange: (view: ViewKey) => void;
  onThemeChange: () => void;
  onCreate: () => void;
}

const tabs: Array<[ViewKey, string]> = [
  ['dashboard', 'Visão geral'],
  ['products', 'Produtos'],
  ['categories', 'Categorias'],
  ['stock', 'Estoque'],
];

export function Header({ view, dark, onViewChange, onThemeChange, onCreate }: HeaderProps) {
  const action = view === 'products' ? 'Novo produto' : view === 'categories' ? 'Nova categoria' : 'Nova movimentação';
  return (
    <header className="topbar">
      <div className="logo">
        <i aria-hidden="true" />
        <b>Product Manager</b>
      </div>
      <nav className="tabs" aria-label="Navegação principal">
        {tabs.map(([key, label]) => (
          <button key={key} className={`tab${view === key ? ' active' : ''}`} onClick={() => onViewChange(key)}>
            {label}
          </button>
        ))}
      </nav>
      <span className="header-spacer" />
      <button className="button" onClick={onThemeChange}>{dark ? 'Modo claro' : 'Modo escuro'}</button>
      <button className="button primary" onClick={onCreate}>+ {action}</button>
    </header>
  );
}
