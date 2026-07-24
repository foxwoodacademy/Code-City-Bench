
import React, { useState } from 'react';
import { Skull, Shield, Activity, Terminal, Play, Lock, ChevronRight, Zap, Target, Cpu, Hash, Layers } from 'lucide-react';

interface TraceStep {
  ptr: string;
  val: string;
  desc: string;
  status: 'Safe' | 'Exploited';
}

const CyberRange: React.FC = () => {
  const [drillActive, setDrillActive] = useState(false);
  const [currentExploit, setCurrentExploit] = useState<string | null>(null);
  const [traceIndex, setTraceIndex] = useState(0);

  const bufferTrace: TraceStep[] = [
    { ptr: '0x7ffd5e4a10', val: '0x0000', desc: 'Buffer Start. 512 bytes allocated.', status: 'Safe' },
    { ptr: '0x7ffd5e4a14', val: '0x4141', desc: 'Writing user input "AA"...', status: 'Safe' },
    { ptr: '0x7ffd5e4c10', val: '0x4141', desc: 'Buffer Limit Reached.', status: 'Safe' },
    { ptr: '0x7ffd5e4c14', val: '0x9090', desc: 'OVERFLOW: Overwriting Return Address!', status: 'Exploited' },
  ];

  const startDrill = (type: string) => {
    setCurrentExploit(type);
    setDrillActive(true);
    setTraceIndex(0);
  };

  const exploits = [
    { id: 'sqli', name: 'SQL Injection', level: 'Intermediate', complexity: 45, icon: Layers },
    { id: 'bov', name: 'Buffer Overflow', level: 'Advanced', complexity: 88, icon: Skull },
    { id: 'jwt', name: 'JWT Hijacking', level: 'Beginner', complexity: 20, icon: Lock },
    { id: 'xss', name: 'Stored XSS', level: 'Beginner', complexity: 15, icon: Zap }
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-12 pb-24 animate-in fade-in duration-700">
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-8">
        <div className="flex items-center gap-6">
          <div className="w-20 h-20 bg-red-500/10 rounded-[2.5rem] flex items-center justify-center text-red-500 border border-red-500/20 shadow-2xl shadow-red-500/10">
            <Target size={40} />
          </div>
          <div>
            <h2 className="text-5xl font-black tracking-tighter text-white uppercase italic">Whitebox Range</h2>
            <p className="text-slate-500 font-medium text-lg">Deconstructing the "How" of Positive Execution.</p>
          </div>
        </div>
        
        <div className="etched-glass px-8 py-4 flex items-center gap-4">
           <div className="w-3 h-3 rounded-full bg-red-500 animate-ping" />
           <span className="text-[10px] font-black uppercase tracking-[0.4em] text-white">Debugger: Attached</span>
        </div>
      </header>

      {!drillActive ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {exploits.map((ex) => (
            <button 
              key={ex.id}
              onClick={() => startDrill(ex.name)}
              className="etched-glass p-8 rounded-[3rem] text-left group hover:border-red-500/40 transition-all hover:scale-[1.02]"
            >
              <div className="w-14 h-14 bg-white/5 rounded-2xl flex items-center justify-center text-slate-500 group-hover:text-red-500 transition-colors mb-6">
                <ex.icon size={28} />
              </div>
              <h3 className="text-xl font-bold text-white uppercase italic tracking-tight">{ex.name}</h3>
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mt-2">Theory: {ex.level}</p>
              <div className="mt-8 flex items-center justify-between text-[10px] font-black uppercase tracking-[0.2em] text-red-500 opacity-0 group-hover:opacity-100 transition-opacity">
                Study Execution <ChevronRight size={14} />
              </div>
            </button>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 animate-in zoom-in-95 duration-500">
          <div className="lg:col-span-8 space-y-8">
            <div className="etched-glass p-10 h-[640px] relative overflow-hidden bg-black/40 border-red-500/20">
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-4">
                  <Cpu className="text-red-500" />
                  <h3 className="text-xl font-black uppercase tracking-tight text-white">Memory Trace: {currentExploit}</h3>
                </div>
                <button onClick={() => setDrillActive(false)} className="text-slate-600 hover:text-white px-4 py-2 etched-glass rounded-xl text-[10px] uppercase font-black">Exit Debugger</button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                <div className="space-y-4">
                  <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-500">Execution Stream</h4>
                  <div className="space-y-2 font-mono text-[10px] text-red-400/80">
                    {bufferTrace.map((step, i) => (
                      <div 
                        key={i} 
                        className={`p-4 rounded-xl border transition-all ${i === traceIndex ? 'bg-red-500/10 border-red-500 text-white' : 'bg-white/5 border-transparent opacity-40'}`}
                      >
                        <div className="flex justify-between mb-1">
                          <span className="text-emerald-500">{step.ptr}</span>
                          <span className={step.status === 'Exploited' ? 'text-red-500' : 'text-slate-600'}>{step.status}</span>
                        </div>
                        <p>{step.desc}</p>
                      </div>
                    ))}
                  </div>
                  <div className="pt-6 flex gap-4">
                     <button 
                      onClick={() => setTraceIndex(prev => Math.min(bufferTrace.length - 1, prev + 1))}
                      className="px-6 py-3 bg-red-500 text-slate-950 font-black text-[10px] uppercase tracking-widest rounded-xl"
                     >
                        Next Instruction
                     </button>
                     <button 
                      onClick={() => setTraceIndex(0)}
                      className="px-6 py-3 bg-white/5 text-slate-400 font-black text-[10px] uppercase tracking-widest rounded-xl"
                     >
                        Reset Trace
                     </button>
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-500">Stack Visualization</h4>
                  <div className="border border-white/10 rounded-2xl overflow-hidden bg-slate-950/50 p-2 h-[400px] flex flex-col-reverse gap-1">
                    {[...Array(12)].map((_, i) => (
                      <div 
                        key={i} 
                        className={`h-8 flex items-center justify-center text-[9px] font-mono border-y border-white/5 transition-all ${i >= (12 - traceIndex * 3) ? 'bg-red-500/20 text-red-400 border-red-500/40' : 'bg-white/5 text-slate-700'}`}
                      >
                         {i === 0 ? '[RET_ADDR]' : (i < 8 ? '[BUFFER_SPACE]' : '[STACK_FRAME]')}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="lg:col-span-4 space-y-6">
             <div className="etched-glass p-8 bg-emerald-500/5 border-emerald-500/20">
                <h4 className="text-lg font-black uppercase tracking-tight text-emerald-400 mb-6 flex items-center gap-3">
                  <Terminal size={20} /> The Fix (Mechanics)
                </h4>
                <div className="space-y-6">
                   <p className="text-xs text-slate-400 leading-relaxed">
                     The vulnerability isn't just "the function." It's the **Trusting of Input Length**. By using fixed-size buffers, we allow the CPU to write past the allocated memory into the return pointer.
                   </p>
                   <div className="p-4 bg-black/40 rounded-xl border border-white/5">
                      <p className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-2">Vulnerable Logic</p>
                      <code className="text-[10px] text-red-400">void handle(char *in) {'{'} char buf[512]; strcpy(buf, in); {'}'}</code>
                   </div>
                   <div className="p-4 bg-black/40 rounded-xl border border-emerald-500/20">
                      <p className="text-[10px] font-black uppercase tracking-widest text-emerald-500 mb-2">Sovereign Fix</p>
                      <code className="text-[10px] text-emerald-400">void handle(char *in) {'{'} char buf[512]; strncpy(buf, in, 511); buf[511] = '\0'; {'}'}</code>
                   </div>
                </div>
             </div>
             
             <div className="etched-glass p-8">
                <h4 className="text-sm font-black uppercase tracking-widest text-slate-500 mb-4 flex items-center gap-2">
                  <Hash size={16} /> Mentor Brief
                </h4>
                <p className="text-sm text-slate-400 leading-relaxed italic">
                  "Don't just use strncpy because I said so. Use it because it forces the kernel to respect the boundaries you defined. Ownership means knowing your limits."
                </p>
             </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CyberRange;
