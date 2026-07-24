
import React, { useState, useEffect } from 'react';
import { AlertTriangle, X, Terminal, Skull } from 'lucide-react';

const RealityCheckAlert: React.FC = () => {
  const [data, setData] = useState<{ bs_rating: number, critique: string } | null>(null);

  useEffect(() => {
    const handleCheck = (e: any) => {
      setData(e.detail);
      // Auto dismiss after 8s
      setTimeout(() => setData(null), 8000);
    };
    window.addEventListener('reality_check_trigger', handleCheck);
    return () => window.removeEventListener('reality_check_trigger', handleCheck);
  }, []);

  if (!data) return null;

  return (
    <div className="fixed top-24 left-1/2 -translate-x-1/2 z-[300] w-full max-w-xl animate-in slide-in-from-top-10 duration-500 p-4">
      <div className="bg-slate-900 border border-red-500/40 rounded-3xl p-6 shadow-[0_0_50px_rgba(239,68,68,0.2)] backdrop-blur-2xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-red-500/10 rounded-xl flex items-center justify-center text-red-400">
              <Skull size={20} />
            </div>
            <div>
              <h4 className="text-[10px] font-black uppercase tracking-[0.3em] text-red-500">Cynical Reviewer: Reality Check</h4>
              <p className="text-[9px] text-slate-500 uppercase tracking-widest font-bold">Utility Leak Detected</p>
            </div>
          </div>
          <button onClick={() => setData(null)} className="text-slate-600 hover:text-white transition-colors">
            <X size={16} />
          </button>
        </div>

        <div className="space-y-4">
          <div className="p-4 bg-white/5 rounded-2xl border border-white/5">
            <div className="flex justify-between items-center mb-2">
              <span className="text-[8px] font-black text-slate-500 uppercase tracking-widest">Bullshit Rating</span>
              <span className="text-xs font-black text-red-400">{data.bs_rating}%</span>
            </div>
            <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full bg-red-500" style={{ width: `${data.bs_rating}%` }} />
            </div>
          </div>

          <div className="flex gap-4">
            <Terminal size={16} className="text-red-500 shrink-0 mt-1" />
            <p className="text-sm text-slate-300 italic leading-relaxed">
              "{data.critique}"
            </p>
          </div>
        </div>

        <div className="mt-6 flex justify-end">
           <p className="text-[7px] font-black uppercase tracking-[0.5em] text-slate-700">Protocol: Stop being basic</p>
        </div>
      </div>
    </div>
  );
};

export default RealityCheckAlert;
