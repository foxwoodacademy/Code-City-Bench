
import React, { useState } from 'react';
import { Fingerprint, Key, Smartphone, Mail, MoreVertical, ShieldCheck, Zap, Sparkles, Check, Hammer } from 'lucide-react';
import { useAiStamper } from '../hooks/useAiStamper';

const IdentityHub: React.FC = () => {
  const [autoPopulate, setAutoPopulate] = useState(true);
  const [stampFeedback, setStampFeedback] = useState<string | null>(null);
  
  // Listen for JaneBot 'Wheel Elevation' events
  useAiStamper('autoPopulate', (val) => {
    setAutoPopulate(val === 'true' || val === true);
    setStampFeedback('Propagating Identity...');
    setTimeout(() => setStampFeedback(null), 3000);
  });

  const platforms = [
    { name: 'Apple ID Sync', status: 'Connected', icon: <Smartphone size={20} />, lastUsed: '3h ago' },
    { name: 'Google Workspace', status: 'Connected', icon: <Mail size={20} />, lastUsed: '5m ago' },
    { name: 'Hardware Key (Yubikey)', status: 'Active', icon: <Key size={20} />, lastUsed: '2d ago' },
    { name: 'Native Biometrics', status: 'Standby', icon: <Fingerprint size={20} />, lastUsed: 'Today' },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-10 pb-12 animate-in fade-in duration-700">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-black tracking-tighter uppercase">Identity Vaults</h2>
          <p className="text-slate-500 font-medium text-lg mt-1">Cross-platform shard management for <span className="text-emerald-400">Syntax-AI</span>.</p>
        </div>
        {stampFeedback && (
          <div className="px-4 py-2 bg-emerald-500/20 border border-emerald-500/30 rounded-2xl flex items-center gap-2 animate-bounce">
            <Hammer size={16} className="text-emerald-400" />
            <span className="text-[10px] font-black uppercase text-emerald-400 tracking-widest">{stampFeedback}</span>
          </div>
        )}
      </div>

      <div className="glass p-10 rounded-[3rem] border border-emerald-500/20 relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-10 opacity-5 group-hover:opacity-10 transition-opacity rotate-12">
          <Zap size={150} className="text-emerald-500 fill-emerald-500" />
        </div>
        
        <div className="flex flex-col md:flex-row gap-10 relative z-10">
          <div className="shrink-0">
            <div className="w-20 h-20 bg-emerald-500 rounded-[2.5rem] flex items-center justify-center shadow-[0_20px_50px_rgba(16,185,129,0.3)]">
              <Sparkles className="text-slate-950" size={40} />
            </div>
          </div>
          <div className="flex-1 space-y-6">
            <div>
              <h3 className="text-2xl font-bold tracking-tight">Universal Auto-Populate</h3>
              <p className="text-slate-400 mt-2 leading-relaxed">JaneBot can automatically push your verified identity to new shards. Hand the wheel to let Syntax-AI manage your onboarding.</p>
            </div>
            
            <div className="flex flex-wrap gap-3">
              <div className="flex items-center gap-2 px-4 py-2 bg-white/5 rounded-2xl text-[11px] font-bold text-slate-300 uppercase tracking-widest border border-white/5">
                <Check size={14} className="text-emerald-400" /> AI Elevation Ready
              </div>
              <div className="flex items-center gap-2 px-4 py-2 bg-white/5 rounded-2xl text-[11px] font-bold text-slate-300 uppercase tracking-widest border border-white/5">
                <Check size={14} className="text-emerald-400" /> Shard Rotation
              </div>
            </div>
            
            <div className="flex items-center justify-between pt-6 border-t border-white/5">
              <div className="flex flex-col">
                <span className="font-bold text-lg">Global Identity Propagation</span>
                <span className="text-xs text-slate-500 uppercase tracking-widest mt-0.5">Managed by aFiREfly Scout</span>
              </div>
              <button 
                onClick={() => setAutoPopulate(!autoPopulate)}
                className={`w-16 h-8 rounded-full transition-all relative p-1 ${autoPopulate ? 'bg-emerald-500 shadow-[0_0_20px_rgba(16,185,129,0.5)]' : 'bg-slate-800'}`}
              >
                <div className={`w-6 h-6 bg-white rounded-full shadow-lg transition-all duration-300 ${autoPopulate ? 'translate-x-8' : 'translate-x-0'}`}></div>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-4">
        {platforms.map((p, i) => (
          <div key={i} className="glass p-6 rounded-[2.5rem] flex items-center justify-between group hover:bg-emerald-500/5 transition-all duration-500 border-white/5 hover:border-emerald-500/20">
            <div className="flex items-center gap-6">
              <div className="w-16 h-16 rounded-[1.8rem] bg-slate-900 flex items-center justify-center text-slate-500 group-hover:text-emerald-400 group-hover:bg-emerald-500/10 transition-all duration-500 shadow-inner">
                {p.icon}
              </div>
              <div>
                <h4 className="font-bold text-xl tracking-tight">{p.name}</h4>
                <div className="flex items-center gap-3 mt-1.5">
                  <span className={`w-2 h-2 rounded-full ${p.status === 'Connected' || p.status === 'Active' ? 'bg-emerald-500 shadow-[0_0_8px_#10b981]' : 'bg-slate-700'}`}></span>
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">{p.status} • Syncing {p.lastUsed}</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button className="px-6 py-2.5 bg-white/5 border border-white/10 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-white/10 transition-all">Configure</button>
              <button className="p-3 text-slate-600 hover:text-white transition-colors"><MoreVertical size={22} /></button>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-emerald-500/5 border border-emerald-500/20 p-8 rounded-[3rem] flex items-start gap-6 group">
        <div className="p-4 bg-emerald-500/10 rounded-[1.8rem] text-emerald-400 group-hover:scale-110 transition-transform duration-500">
          <ShieldCheck size={32} />
        </div>
        <div>
          <h4 className="font-bold text-2xl text-emerald-400 tracking-tight">Security Handshake</h4>
          <p className="text-base text-slate-400 mt-2 leading-relaxed max-w-2xl">
            Syntax-AI has detected a legacy token in your Apple ID Sync. We recommend a proactive shard rotation to prevent cross-platform neural drift.
          </p>
          <button className="mt-6 px-8 py-3 bg-emerald-500 text-slate-950 font-black text-xs rounded-2xl uppercase tracking-[0.2em] shadow-xl shadow-emerald-500/20 hover:scale-[1.05] transition-all active:scale-95">
            Upgrade Handshake Now
          </button>
        </div>
      </div>
    </div>
  );
};

export default IdentityHub;
