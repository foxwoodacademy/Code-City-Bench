
import React, { useState } from 'react';
import { Shield, Key, Fingerprint, ArrowRight, Mail, Lock, CheckCircle, Zap, Eye, EyeOff, Loader2, Chrome, Github, UserPlus, Sparkles, Hexagon } from 'lucide-react';

type AuthView = 'login' | 'signup' | 'success';

const ForgeRing = ({ active }: { active?: boolean }) => (
  <div className="relative w-40 h-40 flex items-center justify-center optical-ring">
    <div className={`absolute inset-0 rounded-full border border-white/5 animate-[spin_15s_linear_infinite]`} />
    <div className={`absolute inset-4 rounded-full border border-emerald-500/10 ${active ? 'animate-pulse' : ''}`} />
    
    <div className="z-10 bg-slate-900/40 w-20 h-20 rounded-full flex items-center justify-center border border-white/10 backdrop-blur-md">
       <Zap className={`text-emerald-400 transition-all duration-700 ${active ? 'scale-110' : 'scale-100 opacity-60'}`} size={32} />
    </div>
    
    {/* Data Markers */}
    {[0, 90, 180, 270].map((deg) => (
      <div 
        key={deg}
        style={{ transform: `rotate(${deg}deg) translateY(-76px)` }}
        className={`absolute w-1 h-3 bg-emerald-500/30 rounded-full transition-all duration-500 ${active ? 'bg-emerald-400' : ''}`} 
      />
    ))}
  </div>
);

const AuthPortal = ({ onLogin }: { onLogin: () => void }) => {
  const [view, setView] = useState<AuthView>('login');
  const [isLoading, setIsLoading] = useState(false);
  const [showPass, setShowPass] = useState(false);

  const handleAction = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    await new Promise(r => setTimeout(r, 1800));
    onLogin();
  };

  const socialLogin = async (provider: string) => {
    setIsLoading(true);
    console.log(`Connecting via ${provider} protocol...`);
    await new Promise(r => setTimeout(r, 1500));
    onLogin();
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center p-8 relative overflow-hidden">
      <div className={`w-full max-w-lg etched-glass p-12 rounded-[2.5rem] relative ${isLoading ? 'opacity-40 blur-sm' : 'opacity-100'}`}>
        
        <div className="flex flex-col items-center mb-10">
          <ForgeRing active={isLoading} />
          <div className="mt-8 text-center">
            <h1 className="text-3xl font-black uppercase tracking-tighter text-white">Equinex Modmind</h1>
            <p className="text-[10px] text-slate-500 font-bold uppercase tracking-[0.4em] mt-2">Zero-Trust Identity Shard</p>
          </div>
        </div>

        {/* Minimal Tab Switcher */}
        <div className="flex border-b border-white/5 mb-10">
          <button 
            onClick={() => setView('login')}
            className={`flex-1 pb-4 text-[10px] font-black uppercase tracking-[0.3em] transition-all border-b-2 ${view === 'login' ? 'border-emerald-500 text-white' : 'border-transparent text-slate-600 hover:text-slate-400'}`}
          >
            Access
          </button>
          <button 
            onClick={() => setView('signup')}
            className={`flex-1 pb-4 text-[10px] font-black uppercase tracking-[0.3em] transition-all border-b-2 ${view === 'signup' ? 'border-emerald-500 text-white' : 'border-transparent text-slate-600 hover:text-slate-400'}`}
          >
            Forge
          </button>
        </div>

        {view === 'login' ? (
          <form onSubmit={handleAction} className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
            <div className="space-y-1">
              <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest ml-1">Shard ID</label>
              <div className="relative">
                <Mail className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-600" size={16} />
                <input type="email" placeholder="operator@equinex.hub" className="w-full bg-white/5 border border-white/5 rounded-2xl py-4 pl-12 pr-4 text-sm focus:outline-none focus:border-emerald-500/40 transition-all" required />
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest ml-1">Key Code</label>
              <div className="relative">
                <Lock className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-600" size={16} />
                <input type={showPass ? "text" : "password"} placeholder="••••••••••••" className="w-full bg-white/5 border border-white/5 rounded-2xl py-4 pl-12 pr-12 text-sm focus:outline-none focus:border-emerald-500/40 transition-all" required />
                <button type="button" onClick={() => setShowPass(!showPass)} className="absolute right-5 top-1/2 -translate-y-1/2 text-slate-600 hover:text-white">
                  {showPass ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
            <button className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black py-5 rounded-2xl shadow-xl transition-all flex items-center justify-center gap-2 uppercase text-[10px] tracking-[0.3em] active:scale-95">
              Connect Shard <ArrowRight size={14} />
            </button>
          </form>
        ) : (
          <form onSubmit={handleAction} className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
             <div className="space-y-1">
                <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest ml-1">Identity Codename</label>
                <div className="relative">
                  <UserPlus className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-600" size={16} />
                  <input type="text" placeholder="Operator X" className="w-full bg-white/5 border border-white/5 rounded-2xl py-4 pl-12 pr-4 text-sm focus:outline-none focus:border-emerald-500/40" required />
                </div>
             </div>
             <div className="space-y-1">
                <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest ml-1">Email Shard</label>
                <input type="email" placeholder="shard@equinex.hub" className="w-full bg-white/5 border border-white/5 rounded-2xl py-4 px-6 text-sm focus:outline-none focus:border-emerald-500/40" required />
             </div>
             <button className="w-full bg-white text-slate-950 hover:bg-emerald-500 font-black py-5 rounded-2xl shadow-xl transition-all flex items-center justify-center gap-2 uppercase text-[10px] tracking-[0.3em] active:scale-95">
                Forge Account <Sparkles size={14} />
             </button>
          </form>
        )}

        {/* Social Buttons - Now Functional with Visual Shard Sync */}
        <div className="mt-12 space-y-4">
          <div className="flex items-center gap-4 text-slate-800">
             <div className="h-[1px] flex-1 bg-white/5" />
             <span className="text-[9px] font-black uppercase tracking-[0.3em] text-slate-600">Cross-Sync</span>
             <div className="h-[1px] flex-1 bg-white/5" />
          </div>
          <div className="grid grid-cols-3 gap-3">
            <button onClick={() => socialLogin('Google')} className="bg-white/5 hover:bg-white/10 p-4 rounded-xl flex items-center justify-center border border-white/5 transition-all group">
              <Chrome className="text-slate-500 group-hover:text-emerald-400" size={20} />
            </button>
            <button onClick={() => socialLogin('GitHub')} className="bg-white/5 hover:bg-white/10 p-4 rounded-xl flex items-center justify-center border border-white/5 transition-all group">
              <Github className="text-slate-500 group-hover:text-emerald-400" size={20} />
            </button>
            <button onClick={() => socialLogin('Biometric')} className="bg-white/5 hover:bg-white/10 p-4 rounded-xl flex items-center justify-center border border-white/5 transition-all group">
              <Fingerprint className="text-slate-500 group-hover:text-emerald-400" size={20} />
            </button>
          </div>
        </div>
      </div>

      {isLoading && (
        <div className="fixed inset-0 z-[100] flex flex-col items-center justify-center backdrop-blur-3xl bg-slate-950/80">
           <div className="w-20 h-20 border-2 border-emerald-500/30 border-t-emerald-500 rounded-full animate-spin shadow-[0_0_40px_rgba(16,185,129,0.2)]" />
           <p className="mt-8 text-[11px] font-black text-emerald-500 tracking-[0.6em] uppercase animate-pulse">Syncing Shards...</p>
        </div>
      )}
    </div>
  );
};

export default AuthPortal;
