import { useEffect } from 'react';

interface ToastProps {
  message: string;
  kind: 'ok' | 'bad';
  onClose: () => void;
}

export function Toast({ message, kind, onClose }: ToastProps) {
  useEffect(() => {
    const timer = window.setTimeout(onClose, 3800);
    return () => window.clearTimeout(timer);
  }, [message, onClose]);

  return <div className={`toast${kind === 'bad' ? ' bad' : ''}`}>{message}</div>;
}
