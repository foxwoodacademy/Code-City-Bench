
import { useEffect } from 'react';

export const useAiStamper = (targetId: string, onExecute: (value: any) => void) => {
  useEffect(() => {
    const handleStamping = (event: any) => {
      const { target, value } = event.detail.args;
      if (target === targetId || target === 'global') {
        onExecute(value);
      }
    };

    window.addEventListener('ai_stamper_execution', handleStamping);
    return () => window.removeEventListener('ai_stamper_execution', handleStamping);
  }, [targetId, onExecute]);
};
