
import React from 'react';
import { Activity, Zap, Search, BrainCircuit, BarChart3, Database } from 'lucide-react';
import { useSecurityMesh } from '../hooks/useSecurityMesh';

const NatHub: React.FC = () => {
  const { natMetrics, detectedIntent } = useSecurityMesh();

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-16 animate-in fade-in slide-in-from-bottom-6 duration-700">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-center gap-6">
          <div className="w-16 h-16 bg-blue-500/10 rounded-[2rem] flex items-center justify-center text-blue-400 border border-blue-500/20 shadow-2xl shadow-blue-500/10">
            <BrainCircuit size={32} />
          </div>
          <div>
            <h2 className="text-4xl font-extrabold tracking-tighter text-white">NatHub Diagnostics</h2>
            <p className="text-slate-500 font-medium text-lg">Nuance detection and intent weighing for <span className="text-blue-400">Syntax-AI</span>.</p>
          </div>
        </div>
        
        <div className="glass px-6 py-4 rounded-3xl border border-white/10 flex items-center gap-4">
          <div className="text-right">
            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Active Intent</p>
            <p className={`text-xl font-bold ${detectedIntent === 'Stable' ? 'text-emerald-400' : 'text-orange-400'}`}>{detectedIntent}</p>
          </div>
          <div className="w-10 h-10 rounded-2xl bg-white/5 flex items-center justify-center">
            <Search size={20} className="text-slate-400" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="glass p-8 rounded-[3rem] border border-white/10 relative overflow-hidden group">
            <div className="absolute -top-24 -right-24 w-64 h-64 bg-blue-500/5 rounded-full blur-[80px]" />
            <div className="flex justify-between items-center mb-8">
              <h3 className="text-2xl font-bold flex items-center gap-3">
                <BarChart3 className="text-blue-400" /> Nuance Analytics
              </h3>
              <Database className="text-slate-600" size={20} />
            </div>
            
            <div className="grid gap-6">
              {natMetrics.map((m) => (
                <div key={m.id} className="space-y-3">
                  <div className="flex justify-between items-end">
                    <div>
                      <h4 className="font-bold text-sm text-slate-300">{m.label}</h4>
                      <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Weight: {m.weight}x • Nuance: {m.nuance}</p>
                    </div>
                    <span className="text-lg font-mono font-bold text-blue-400">{Math.round(m.value)}%</span>
                  </div>
                  <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-blue-600 to-blue-400 transition-all duration-1000"
                      style={{ width: `${m.value}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-10 p-5 bg-white/5 rounded-2xl border border-white/5">
              <p className="text-xs font-medium text-slate-400 leading-relaxed italic">
                "Syntax AI anticipates user intent by calculating the Delta between explicit command and latent behavioral echo."
              </p>
            </div>
          </div>
        </div>

        <div className="lg:col-span-1 space-y-6">
          <div className="glass p-8 rounded-[3rem] border border-white/10 flex flex-col items-center text-center">
            <div className="w-24 h-24 rounded-full bg-blue-500/10 flex items-center justify-center mb-6 relative">
              <Zap className="text-blue-400 animate-pulse" size={40} />
              <div className="absolute inset-0 rounded-full border border-blue-500/20 animate-ping" />
            </div>
            <h3 className="text-xl font-bold">Intent Shifting</h3>
            <p className="text-sm text-slate-500 mt-2">The system is currently pre-caching assets for the detected intent: <span className="text-white font-bold">{detectedIntent}</span>.</p>
            
            <div className="w-full mt-8 space-y-3">
              <button className="w-full py-4 bg-blue-500 text-white rounded-2xl font-bold shadow-xl shadow-blue-500/20 hover:scale-[1.02] transition-all">
                Recalibrate Intent
              </button>
              <button className="w-full py-4 bg-white/5 border border-white/10 text-slate-300 rounded-2xl font-bold hover:bg-white/10 transition-all">
                Clear Nat-DB Cache
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NatHub;
