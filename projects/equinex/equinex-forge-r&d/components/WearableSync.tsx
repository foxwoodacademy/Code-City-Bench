
import React, { useState, useEffect } from 'react';
import { Watch, Flame, Zap, Activity, Battery, Wind } from 'lucide-react';
import { WearableShard } from '../types';

const WearableSync: React.FC = () => {
  const [active, setActive] = useState(false);
  const [metrics, setMetrics] = useState<WearableShard[]>([
    { id: 'w1', type: 'Watch', label: 'Equinex Watch v2', battery: 84, metric: 'Pulse', value: 72, lastSync: Date.now() },
    { id: 'v1', type: 'Vape', label: 'Modmind Vapor-8', battery: 42, metric: 'Puffs', value: 124, lastSync: Date.now() }
  ]);

  useEffect(() => {
    const handleGesture = (e: any) => {
      const { shards } = e.detail;
      // Wearables are detected if shards are in the "wrist zone" (roughly bottom left)
      setActive(shards >= 1);
    };
    window.addEventListener('optical_gesture', handleGesture);
    return () => window.removeEventListener('optical_gesture', handleGesture);
  }, []);

  if (!active) return null;

  return (
    <div className="fixed bottom-32 left-8 z-[120] space-y-4 animate-in slide-in-from-left-4 duration-500">
      {metrics.map(m => (
        <div key={m.id} className="etched-glass p-4 rounded-3xl border border-emerald-500/10 flex items-center gap-4 w-64 group hover:scale-105 transition-all">
          <div className="w-12 h-12 bg-emerald-500/10 rounded-2xl flex items-center justify-center text-emerald-400 group-hover:bg-emerald-500 group-hover:text-slate-950 transition-all">
            {m.type === 'Watch' ? <Watch size={20} /> : <Wind size={20} />}
          </div>
          <div className="flex-1">
            <div className="flex justify-between items-center">
              <h5 className="text-[10px] font-black uppercase text-white tracking-widest">{m.label}</h5>
              <div className="flex items-center gap-1 text-[8px] font-bold text-slate-500">
                <Battery size={8} /> {m.battery}%
              </div>
            </div>
            <div className="flex items-center justify-between mt-1">
              <p className="text-[8px] font-black uppercase tracking-[0.3em] text-emerald-500/50">{m.metric}</p>
              <p className="text-sm font-black text-white">{m.value}</p>
            </div>
            <div className="h-0.5 w-full bg-white/5 rounded-full mt-2 overflow-hidden">
               <div className="h-full bg-emerald-500 animate-pulse" style={{ width: `${(Number(m.value) % 100)}%` }} />
            </div>
          </div>
        </div>
      ))}
      <div className="flex items-center gap-2 px-4 py-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
         <Zap size={10} className="text-emerald-400 animate-pulse" />
         <span className="text-[7px] font-black uppercase tracking-[0.5em] text-emerald-400">Wearable Mesh: Locked</span>
      </div>
    </div>
  );
};

export default WearableSync;
