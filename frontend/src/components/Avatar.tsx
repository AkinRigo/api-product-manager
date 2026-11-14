import { palette } from '../utils/format';

interface AvatarProps {
  id: number;
  name: string;
  large?: boolean;
}

export function Avatar({ id, name, large = false }: AvatarProps) {
  return (
    <span className={`avatar${large ? ' avatar-large' : ''}`} style={{ background: palette[id % 5] }}>
      {name.trim().charAt(0).toUpperCase() || '?'}
    </span>
  );
}
