
import React, { useState, useEffect, useRef } from 'react';
import { Target, ChevronRight, AlertTriangle, Crosshair, Zap, Activity, Grid, Layers, Share2, Skull, Play, Terminal, Database, Shield, History, Users, Monitor, FileText } from 'lucide-react';
import { useSecurityMesh } from '../hooks/useSecurityMesh';
import { TacticalCampaign, TacticalStep, PentestOutcome } from '../types';
import TacticalBrief from './TacticalBrief';

const TacticalEngine: React.FC = () => {
  const { activeCampaigns, pentestHistory, agents } = useSecurityMesh();
  const [selectedMove, setSelectedMove] = useState<TacticalStep | null>(null);
  const [showFullBrief, setShowFullBrief] = useState(false);
  const [consoleLogs, setConsoleLogs] = useState<{ msg: string, time: string, type: 'info' | 'warn' | 'success' | 'bot' }[]>([]);
  const logContainerRef = useRef<HTMLDivElement>(null);

  const defaultCampaign: TacticalCampaign = {
    id: 'camp-1',
    name: 'Initial Gambit',
    objective: 'Kernel Persistence',
    complexity: 94,
    steps: [
      { id: '1', label: 'Heap Shaper', description: 'Grooming heap chunks for precise allocation control.', pos: { x: 10, y: 50 }, type: 'Entry', successRate: 88, detectionRisk: 12 },
      { id: '2', label: 'Pointer Smash', description: 'Overwriting the function pointer via OOB access.', pos: { x: 35, y: 30 }, type: 'Pivot', successRate: 62, detectionRisk: 45 },
      { id: '3', label: 'ROP Sled', description: 'Executing Return-Oriented-Programming chain for bypass.', pos: { x: 60, y: 70 }, type: 'Pivot', successRate: 75, detectionRisk: 30 },
      { id: '4', label: 'Persistence Root', description: 'Hooking syscalls for permanent kernel access.', pos: { x: 90, y: 50 }, type: 'Objective', successRate: 40, detectionRisk: 90 },
    ]
  };

  const campaigns = activeCampaigns.length > 0 ? activeCampaigns : [defaultCampaign];

  const pushLog = (msg: string, type: 'info' | 'warn' | 'success' | 'bot' = 'info') => {
    setConsoleLogs(prev => [{ msg, time: new Date().toLocaleTimeString(), type }, ...prev].slice(0, 30));
  };

  useEffect(() => {
    if (activeCampaigns.length > 0) {
      const newCamp = activeCampaigns[0];
      pushLog(`New Strategic Vector: ${newCamp.name}`, 'bot');
    }
  }, [activeCampaigns]);

  useEffect(() => {
    if (pentestHistory.length > 0) {
      const latest = pentestHistory[0];
      pushLog(`${latest.stepLabel} execution result: ${latest.result.toUpperCase()}`, latest.result === 'Success' ? 'success' : 'warn');
    }
  }, [pentestHistory]);

  return (
    <div className="max-w-7xl mx-auto space-y-12 pb-24 animate-in fade-in duration-1000">
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-8">
        <div className="flex items-center gap-6">
          <div className="w-20 h-20 bg-cyan-500/10 rounded-[2.5rem] flex items-center justify-center text-cyan-400 border border-cyan-500/20 shadow-2xl shadow-cyan-500/10">
            <Crosshair size={40} />
          </div>
          <div>
            <h2 className="text-5xl font-black tracking-tighter text-white uppercase italic">Tactical Board</h2>
            <p className="text-slate-500 font-medium text-lg">Visualizing <span className="text-cyan-400 uppercase font-black">Campaign Chains</span> of the Grandmaster.</p>
          </div>
        </div>
        
        <div className="flex gap-4">
          <button 
            onClick={() => setShowFullBrief(true)}
            className="etched-glass px-8 py-4 flex items-center gap-3 hover:bg-cyan-500/10 group transition-all border-cyan-500/30"
          >
            <FileText className="text-cyan-500 group-hover:scale-110 transition-transform" size={18} />
            <span className="text-[10px] font-black uppercase tracking-widest text-white">View Full Brief</span>
          </button>
          
          <div className="etched-glass px-8 py-4 flex items-center gap-4 border-cyan-500/30">
             <div className="flex flex-col items-end">
                <span className="text-[9px] font-black uppercase tracking-widest text-slate-500">Neural Depth</span>
                <span className="text-lg font-black text-cyan-400">CHESS MASTER</span>
             </div>
             <div className="w-3 h-3 rounded-full bg-cyan-500 animate-pulse shadow-[0_0_10px_#22d3ee]" />
          </div>
        </div>
      </header>

      {showFullBrief && (
        <TacticalBrief 
          history={pentestHistory} 
          agents={agents} 
          campaignName={campaigns[0].name} 
          onClose={() => setShowFullBrief(false)} 
        />
      )}

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
        <div className="lg:col-span-8 space-y-8">
          <div className="etched-glass p-4 rounded-[4rem] border-white/5 bg-slate-900/40 h-[600px] relative overflow-hidden group shadow-2xl">
            <div className="absolute inset-0 opacity-10 pointer-events-none" 
                 style={{ backgroundImage: 'radial-gradient(circle, #22d3ee 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
            
            <svg className="absolute inset-0 w-full h-full pointer-events-none">
              <path 
                d={`M ${campaigns[0].steps.map(s => `${s.pos.x}% ${s.pos.y}%`).join(' L ')}`} 
                fill="none" 
                stroke="url(#lineGrad)" 
                strokeWidth="2"
                strokeDasharray="8 8"
                className="animate-[dash_20s_linear_infinite]"
              />
              <defs>
                <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#22d3ee" stopOpacity="0.2" />
                  <stop offset="100%" stopColor="#22d3ee" stopOpacity="0.8" />
                </linearGradient>
              </defs>
            </svg>

            {campaigns[0].steps.map((step) => (
              <button
                key={step.id}
                onClick={() => { setSelectedMove(step); pushLog(`Analyzing Move Shard: ${step.label}`, 'info'); }}
                style={{ left: `${step.pos.x}%`, top: `${step.pos.y}%` }}
                className={`absolute -translate-x-1/2 -translate-y-1/2 w-32 h-32 rounded-full flex items-center justify-center transition-all duration-700 group/shard ${selectedMove?.id === step.id ? 'scale-110' : 'hover:scale-105'}`}
              >
                <div className={`absolute inset-0 rounded-full border border-cyan-500/20 ${selectedMove?.id === step.id ? 'animate-spin-slow opacity-100' : 'opacity-0 group-hover/shard:opacity-50'}`} />
                <div className={`w-16 h-16 rounded-2xl flex items-center justify-center transition-all ${selectedMove?.id === step.id ? 'bg-cyan-500 text-slate-950 shadow-2xl shadow-cyan-500/40' : 'bg-slate-800 text-cyan-400 border border-cyan-500/20'}`}>
                   {step.type === 'Entry' ? <Play size={24} /> : step.type === 'Pivot' ? <Zap size={24} /> : <Skull size={24} />}
                </div>
                <div className="absolute -bottom-8 whitespace-nowrap">
                   <span className="text-[10px] font-black uppercase tracking-widest text-white group-hover/shard:text-cyan-400 transition-colors">{step.label}</span>
                </div>
              </button>
            ))}

            <div className="absolute bottom-8 left-8 right-8 p-6 etched-glass border-white/5 bg-black/60 md:w-96 backdrop-blur-2xl">
               <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2 text-cyan-400">
                    <Monitor size={12} />
                    <span className="text-[10px] font-black uppercase tracking-widest">Exercise Command Stream</span>
                  </div>
                  <div className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse" />
               </div>
               <div ref={logContainerRef} className="space-y-2 max-h-32 overflow-y-auto scrollbar-hide font-mono text-[9px]">
                  {consoleLogs.map((log, i) => (
                    <div key={i} className={`flex gap-3 border-l-2 pl-3 transition-all ${
                      log.type === 'bot' ? 'border-cyan-500 text-cyan-300' : 
                      log.type === 'warn' ? 'border-red-500 text-red-400' : 
                      log.type === 'success' ? 'border-emerald-500 text-emerald-400' : 'border-slate-800 text-slate-500'
                    }`}>
                       <span className="opacity-40 shrink-0">{log.time}</span>
                       <span className="truncate">{log.msg}</span>
                    </div>
                  ))}
                  {consoleLogs.length === 0 && <div className="text-slate-700 italic">Standing by for simulation instructions...</div>}
               </div>
            </div>
          </div>

          <div className="etched-glass p-10 bg-slate-900/40 border-white/5 overflow-hidden">
             <div className="flex items-center gap-4 mb-10">
                <Users className="text-cyan-400" />
                <h3 className="text-xl font-black uppercase tracking-tight text-white italic">Active Shard Agents</h3>
             </div>
             <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                {agents.map(agent => (
                   <div key={agent.id} className="p-6 bg-black/40 rounded-3xl border border-white/5 group hover:border-cyan-500/20 transition-all">
                      <div className="flex justify-between items-start mb-4">
                         <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${agent.health > 90 ? 'bg-cyan-500/10 text-cyan-400' : 'bg-red-500/10 text-red-400'}`}>
                            {agent.type === 'Scout' ? <Target size={14} /> : agent.type === 'Guardian' ? <Shield size={14} /> : <Zap size={14} />}
                         </div>
                         <div className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse" />
                      </div>
                      <h4 className="font-black text-xs text-white uppercase tracking-widest">{agent.name}</h4>
                      <p className="text-[8px] text-slate-500 uppercase mt-1 tracking-widest font-bold opacity-60">{agent.persona || agent.type}</p>
                      <div className="mt-4 h-0.5 bg-white/5 rounded-full overflow-hidden">
                         <div className="h-full bg-cyan-500 transition-all duration-1000" style={{ width: `${agent.load}%` }} />
                      </div>
                   </div>
                ))}
             </div>
          </div>
        </div>

        <div className="lg:col-span-4 space-y-8">
          <div className="etched-glass p-8 bg-cyan-500/5 border-cyan-500/20 min-h-[400px]">
             {selectedMove ? (
               <div className="space-y-8 animate-in slide-in-from-right-4 duration-500">
                  <header>
                    <div className="flex justify-between items-start mb-2">
                       <span className="text-[9px] font-black uppercase tracking-[0.5em] text-cyan-500">{selectedMove.type}</span>
                       <Share2 size={16} className="text-slate-700 hover:text-white cursor-pointer" />
                    </div>
                    <h3 className="text-3xl font-black uppercase italic tracking-tighter text-white">{selectedMove.label}</h3>
                  </header>
                  
                  <p className="text-sm text-slate-200 leading-relaxed font-medium">
                    {selectedMove.description}
                  </p>

                  <div className="grid grid-cols-2 gap-4">
                     <div className="p-4 bg-black/40 rounded-2xl border border-white/5">
                        <p className="text-[9px] font-black uppercase text-slate-500 tracking-widest mb-1">PoS</p>
                        <p className="text-xl font-black text-cyan-400">{selectedMove.successRate}%</p>
                     </div>
                     <div className="p-4 bg-black/40 rounded-2xl border border-white/5">
                        <p className="text-[9px] font-black uppercase text-slate-500 tracking-widest mb-1">Risk</p>
                        <p className="text-xl font-black text-red-500">{selectedMove.detectionRisk}%</p>
                     </div>
                  </div>

                  <button 
                    onClick={() => pushLog(`Initiating fallout for: ${selectedMove.label}...`, 'info')}
                    className="w-full py-5 bg-cyan-500 text-slate-950 font-black text-[10px] uppercase tracking-[0.3em] rounded-2xl shadow-2xl shadow-cyan-500/20 active:scale-95 transition-all"
                  >
                    Commit to Simulation
                  </button>
               </div>
             ) : (
               <div className="h-full flex flex-col items-center justify-center text-center space-y-4 py-20">
                  <Skull size={60} className="text-slate-800" />
                  <p className="text-[10px] font-black uppercase tracking-[0.4em] text-slate-600 max-w-[200px]">Select a tactical shard to begin exercise analysis.</p>
               </div>
             )}
          </div>

          <div className="etched-glass p-8 border-white/5 bg-slate-900/60 overflow-hidden">
             <h4 className="text-[10px] font-black uppercase tracking-[0.5em] text-slate-600 mb-6 flex items-center gap-2">
                <History size={14} /> Global Simulation History
             </h4>
             <div className="space-y-4 max-h-[400px] overflow-y-auto scrollbar-hide">
                {pentestHistory.map((outcome) => (
                   <div key={outcome.id} className="p-5 bg-black/40 rounded-2xl border border-white/5 hover:border-cyan-500/20 transition-all group">
                      <div className="flex justify-between items-center mb-2">
                         <h5 className="text-[10px] font-black text-white uppercase group-hover:text-cyan-400 transition-colors">{outcome.stepLabel}</h5>
                         <span className={`text-[8px] font-black px-2 py-0.5 rounded ${outcome.result === 'Success' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'}`}>
                            {outcome.result}
                         </span>
                      </div>
                      <p className="text-[9px] text-slate-500 leading-relaxed italic">{outcome.details}</p>
                      <div className="flex justify-between items-center mt-3">
                        <span className="text-[7px] font-mono text-slate-700 uppercase">{new Date(outcome.timestamp).toLocaleTimeString()}</span>
                        {outcome.vulnerabilityIdentified && (
                          <span className="text-[7px] font-black text-cyan-500/40 uppercase tracking-widest">{outcome.vulnerabilityIdentified}</span>
                        )}
                      </div>
                   </div>
                ))}
                {pentestHistory.length === 0 && (
                   <div className="py-10 text-center opacity-20">
                      <Layers size={32} className="mx-auto mb-2" />
                      <p className="text-[8px] font-black uppercase tracking-widest">No Exercises Run</p>
                   </div>
                )}
             </div>
          </div>
        </div>
      </div>
      
      <style>{`
        @keyframes dash {
          to { stroke-dashoffset: -100; }
        }
        .animate-spin-slow {
          animation: spin 8s linear infinite;
        }
      `}</style>
    </div>
  );
};

export default TacticalEngine;
