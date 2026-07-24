
import React, { useState, useEffect, useRef } from 'react';
import { Ghost, Heart, Shield, Sun, Leaf, Cog, Info, Zap, Mic, Activity, RefreshCcw } from 'lucide-react';
import { ThinkingHat, ThinkingHatColor } from '../types';

const HATS_DATA: ThinkingHat[] = [
  { type: 'White', label: 'White Hat', focus: 'Data & Facts', description: 'Objective information, stats, and logical gaps.', active: false },
  { type: 'Red', label: 'Red Hat', focus: 'Emotion & Instinct', description: 'Gut feelings, hunches, and emotional nuances.', active: true },
  { type: 'Black', label: 'Black Hat', focus: 'Caution & Risk', description: 'Critical judgment, risk assessment, and flaws.', active: false },
  { type: 'Yellow', label: 'Yellow Hat', focus: 'Benefits & Value', description: 'Optimism, logical benefits, and constructive energy.', active: false },
  { type: 'Green', label: 'Green Hat', focus: 'Creativity & Ideas', description: 'Alternatives, provocations, and new solutions.', active: false },
  { type: 'Blue', label: 'Blue Hat', focus: 'Process & Control', description: 'Orchestration, summaries, and next steps.', active: false },
];

const ThinkingHats: React.FC = () => {
  const [activeHat, setActiveHat] = useState<ThinkingHatColor>(
    (localStorage.getItem('active_hat') as ThinkingHatColor) || 'Blue'
  );
  const [isListening, setIsListening] = useState(false);
  const [bursting, setBursting] = useState(false);
  const recognitionRef = useRef<any>(null);

  const switchHat = (type: ThinkingHatColor) => {
    if (type === activeHat) return;
    setBursting(true);
    
    // Neural Flush effect
    document.body.classList.add('neural-flush');
    setTimeout(() => document.body.classList.remove('neural-flush'), 800);
    
    setTimeout(() => setBursting(false), 800);
    setActiveHat(type);
    localStorage.setItem('active_hat', type);
    window.dispatchEvent(new CustomEvent('cognitive_shift', { detail: { hat: type } }));
  };

  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase();
        
        const commands = [
          { keywords: ['white', 'data', 'fact'], hat: 'White' },
          { keywords: ['red', 'emotion', 'instinct', 'gut'], hat: 'Red' },
          { keywords: ['black', 'risk', 'caution', 'flaw', 'audit'], hat: 'Black' },
          { keywords: ['yellow', 'benefit', 'value', 'logic', 'positive'], hat: 'Yellow' },
          { keywords: ['green', 'creative', 'idea', 'provoke'], hat: 'Green' },
          { keywords: ['blue', 'process', 'control', 'orchestrate'], hat: 'Blue' },
        ];

        for (const c of commands) {
          if (c.keywords.some(k => transcript.includes(k))) {
            switchHat(c.hat as ThinkingHatColor);
            break;
          }
        }
      };

      recognitionRef.current.onerror = () => setIsListening(false);
      recognitionRef.current.onend = () => isListening && recognitionRef.current.start();
    }
  }, [isListening, activeHat]);

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
    } else {
      recognitionRef.current?.start();
      setIsListening(true);
    }
  };

  const getHatStyles = (type: ThinkingHatColor) => {
    switch (type) {
      case 'White': return { color: 'text-slate-100', border: 'border-white/40', bg: 'bg-white/10', glow: 'shadow-[0_0_40px_rgba(255,255,255,0.15)]', icon: <Info size={24} /> };
      case 'Red': return { color: 'text-red-500', border: 'border-red-500/40', bg: 'bg-red-500/10', glow: 'shadow-[0_0_40px_rgba(239,68,68,0.3)]', icon: <Heart size={24} /> };
      case 'Black': return { color: 'text-slate-400', border: 'border-slate-800', bg: 'bg-slate-900/60', glow: 'shadow-[0_0_40px_rgba(0,0,0,0.8)]', icon: <Shield size={24} /> };
      case 'Yellow': return { color: 'text-yellow-400', border: 'border-yellow-500/40', bg: 'bg-yellow-500/10', glow: 'shadow-[0_0_40px_rgba(234,179,8,0.2)]', icon: <Sun size={24} /> };
      case 'Green': return { color: 'text-emerald-400', border: 'border-emerald-500/40', bg: 'bg-emerald-500/10', glow: 'shadow-[0_0_40px_rgba(16,185,129,0.2)]', icon: <Leaf size={24} /> };
      case 'Blue': return { color: 'text-blue-500', border: 'border-blue-500/40', bg: 'bg-blue-500/10', glow: 'shadow-[0_0_40px_rgba(59,130,246,0.2)]', icon: <Cog size={24} /> };
    }
  };

  const activeStyles = getHatStyles(activeHat);

  return (
    <div className="max-w-6xl mx-auto space-y-16 pb-24 animate-in fade-in duration-1000">
      {/* Burst Overlay */}
      {bursting && (
        <div className="fixed inset-0 z-[1000] pointer-events-none flex items-center justify-center">
           <div className={`w-1 h-1 rounded-full animate-[ping_0.8s_ease-out_forwards] ${activeStyles.bg.replace('/10', '')}`} />
           <div className="absolute inset-0 bg-white/5 backdrop-blur-sm animate-out fade-out duration-700" />
        </div>
      )}

      <div className="text-center space-y-6 relative">
        <div className={`absolute -top-20 left-1/2 -translate-x-1/2 opacity-10 blur-3xl w-64 h-64 rounded-full animate-pulse ${activeStyles.bg}`} />
        
        <div className="flex flex-col items-center gap-6">
          <div className="flex gap-4">
            <button 
              onClick={toggleListening}
              className={`group flex items-center gap-4 px-8 py-3 rounded-full border transition-all duration-500 ${isListening ? 'bg-red-500/20 border-red-500 shadow-[0_0_20px_rgba(239,68,68,0.3)]' : 'etched-glass text-slate-500 hover:text-white'}`}
            >
              <div className={`relative ${isListening ? 'animate-pulse' : ''}`}>
                <Mic size={18} className={isListening ? 'text-red-400' : ''} />
                {isListening && <div className="absolute -inset-2 border border-red-500/50 rounded-full animate-ping" />}
              </div>
              <span className="text-[10px] font-black uppercase tracking-[0.5em]">
                {isListening ? 'Listener: Live' : 'Voice Link'}
              </span>
            </button>
          </div>
          
          <div className="space-y-2">
            <h2 className={`text-7xl font-black tracking-tighter uppercase italic transition-all duration-700 ${activeStyles.color}`}>Cognitive Shards</h2>
            <p className="text-[10px] font-black uppercase tracking-[1em] text-slate-500 translate-x-1">Neural Logic Interface</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {HATS_DATA.map((hat) => {
          const styles = getHatStyles(hat.type);
          const isActive = activeHat === hat.type;
          
          return (
            <button 
              key={hat.type}
              onClick={() => switchHat(hat.type)}
              className={`etched-glass p-10 rounded-[3.5rem] border-2 transition-all duration-700 text-left group relative overflow-hidden ${
                isActive ? `${styles.bg} ${styles.border} ${styles.glow} scale-[1.05] -translate-y-2` : 'border-white/5 opacity-40 hover:opacity-100 hover:scale-[1.02]'
              }`}
            >
              <div className={`w-16 h-16 rounded-[2rem] ${styles.bg} ${styles.color} flex items-center justify-center mb-8 transition-all duration-700 group-hover:rotate-12 shadow-inner`}>
                {styles.icon}
              </div>
              
              <h3 className={`text-2xl font-black tracking-tight ${styles.color}`}>{hat.label}</h3>
              <p className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500 mt-2">{hat.focus}</p>
              <p className="text-sm text-slate-400 mt-6 leading-relaxed font-medium">{hat.description}</p>
              
              <div className={`absolute bottom-0 left-0 h-1.5 w-full transition-all duration-1000 ${isActive ? 'bg-gradient-to-r from-transparent via-current to-transparent' : 'bg-transparent'} ${styles.color}`} />
              
              {isActive && (
                <div className="absolute top-6 right-8">
                   <RefreshCcw size={16} className={`animate-spin-slow opacity-20 ${styles.color}`} />
                </div>
              )}
            </button>
          );
        })}
      </div>

      <div className={`etched-glass p-12 rounded-[4.5rem] border-2 transition-all duration-1000 flex flex-col lg:flex-row items-center gap-12 ${activeStyles.border} bg-slate-900/40`}>
        <div className="shrink-0 relative">
          <div className={`w-48 h-48 rounded-full border-2 border-dashed animate-[spin_20s_linear_infinite] opacity-20 ${activeStyles.color.replace('text-', 'border-')}`} />
          <div className="absolute inset-0 flex items-center justify-center">
            <div className={`w-28 h-28 rounded-[2.5rem] glass flex items-center justify-center shadow-2xl scale-110 ${activeStyles.color} bg-black/40`}>
              {activeStyles.icon}
            </div>
          </div>
          <Activity className={`absolute -bottom-4 -right-4 ${activeStyles.color} animate-pulse`} size={32} />
        </div>
        
        <div className="flex-1 space-y-6 text-center lg:text-left">
          <div className="flex flex-col lg:flex-row items-center gap-4">
             <span className={`text-5xl font-black tracking-tighter uppercase italic ${activeStyles.color}`}>Link: {activeHat}</span>
             <div className={`px-4 py-1.5 rounded-full text-[9px] font-black uppercase tracking-[0.4em] border transition-all duration-700 ${activeStyles.border} ${activeStyles.color}`}>
               Logic Shard Verified
             </div>
          </div>
          <p className="text-slate-200 text-xl leading-relaxed font-medium max-w-2xl">
            Sovereign override confirmed. The Grandmaster is now processing via the <span className={activeStyles.color}>{activeHat} logic shard</span>. Strategic filters tuned to {HATS_DATA.find(h => h.type === activeHat)?.focus}.
          </p>
          <div className="flex gap-4 justify-center lg:justify-start pt-4">
             <div className="h-1 w-20 rounded-full bg-white/5"><div className={`h-full w-full rounded-full ${activeStyles.color.replace('text-', 'bg-')}`} /></div>
             <div className="h-1 w-20 rounded-full bg-white/5"><div className={`h-full w-1/2 rounded-full opacity-50 ${activeStyles.color.replace('text-', 'bg-')}`} /></div>
          </div>
        </div>
      </div>
      
      <style>{`
        .neural-flush {
          animation: chromatic 0.8s ease-in-out;
        }
        @keyframes chromatic {
          0% { filter: contrast(1.2) brightness(1.2); }
          50% { filter: contrast(1.5) brightness(1.5) hue-rotate(10deg); }
          100% { filter: none; }
        }
      `}</style>
    </div>
  );
};

export default ThinkingHats;
