
import React from 'react';
import { FileText, Terminal, ShieldAlert, Clock, Download, Share2, Skull } from 'lucide-react';
import { PentestOutcome, SecurityAgent } from '../types';

interface TacticalBriefProps {
  history: PentestOutcome[];
  agents: SecurityAgent[];
  campaignName: string;
  onClose: () => void;
}

const TacticalBrief: React.FC<TacticalBriefProps> = ({ history, agents, campaignName, onClose }) => {
  return (
    <div className="fixed inset-0 z-[300] flex items-center justify-center p-4 md:p-10 backdrop-blur-3xl bg-slate-950/90 animate-in fade-in duration-500">
      <div className="w-full max-w-5xl h-full etched-glass border-cyan-500/20 flex flex-col overflow-hidden rounded-[3rem]">
        <header className="p-8 border-b border-white/5 flex justify-between items-center bg-slate-900/50">
          <div className="flex items-center gap-6">
            <div className="w-14 h-14 bg-cyan-500/10 rounded-2xl flex items-center justify-center text-cyan-400">
              <FileText size={28} />
            </div>
            <div>
              <h2 className="text-3xl font-black uppercase italic tracking-tighter text-white">Tactical Brief: {campaignName}</h2>
              <p className="text-[10px] font-black uppercase tracking-[0.4em] text-slate-500">Operation Red Team Shard • Exercise Log</p>
            </div>
          </div>
          <div className="flex gap-3">
             <button className="p-3 text-slate-400 hover:text-white transition-colors"><Download size={20} /></button>
             <button onClick={onClose} className="p-3 text-slate-400 hover:text-white transition-colors"><ShieldAlert size={20} /></button>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-10 space-y-12 scrollbar-hide">
          <section className="space-y-6">
            <h3 className="text-[10px] font-black uppercase tracking-[0.5em] text-cyan-500 flex items-center gap-2">
              <Terminal size={14} /> Agent Debriefing
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {agents.slice(0, 4).map(agent => (
                <div key={agent.id} className="p-6 bg-white/5 rounded-3xl border border-white/5">
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-[10px] font-black text-white uppercase">{agent.name}</span>
                    <span className="text-[8px] font-black text-cyan-500 uppercase tracking-widest">{agent.status}</span>
                  </div>
                  <p className="text-xs text-slate-400 italic">"Simulated penetration of AI Studio edge nodes complete. No anomalous signatures detected on current shard. Monitoring for return-oriented-programming drifts."</p>
                </div>
              ))}
            </div>
          </section>

          <section className="space-y-6">
            <h3 className="text-[10px] font-black uppercase tracking-[0.5em] text-red-500 flex items-center gap-2">
              <Clock size={14} /> Sequential Execution Log
            </h3>
            <div className="space-y-4">
              {history.map((entry, i) => (
                <div key={entry.id} className="p-8 bg-black/40 rounded-[2.5rem] border border-white/5 flex flex-col md:flex-row gap-8 items-start">
                  <div className="shrink-0 text-right md:w-32">
                    <p className="text-[10px] font-mono text-cyan-500/60">{new Date(entry.timestamp).toLocaleTimeString()}</p>
                    <p className="text-[8px] font-black text-slate-700 uppercase mt-1">Step {history.length - i}</p>
                  </div>
                  <div className="flex-1 space-y-3">
                    <div className="flex items-center gap-4">
                      <h4 className="text-lg font-black text-white uppercase italic">{entry.stepLabel}</h4>
                      <span className={`px-2 py-0.5 rounded text-[8px] font-black uppercase ${entry.result === 'Success' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
                        {entry.result}
                      </span>
                    </div>
                    <p className="text-sm text-slate-300 leading-relaxed font-medium">
                      {entry.details}
                    </p>
                    {entry.vulnerabilityIdentified && (
                      <div className="flex items-center gap-2 pt-2 border-t border-white/5">
                        <Skull size={12} className="text-red-500" />
                        <span className="text-[10px] font-black text-red-500 uppercase tracking-widest">Vector: {entry.vulnerabilityIdentified}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>

        <footer className="p-8 border-t border-white/5 bg-slate-900/80 flex justify-between items-center">
          <p className="text-[9px] font-black text-slate-600 uppercase tracking-[0.3em]">SHA-256 Digest: 8f4e...9a21 • Verified Operator Brief</p>
          <button 
            onClick={onClose}
            className="px-10 py-4 bg-cyan-500 text-slate-950 rounded-2xl font-black uppercase text-[10px] tracking-widest hover:scale-105 transition-all shadow-2xl shadow-cyan-500/20"
          >
            Acknowledge & Close
          </button>
        </footer>
      </div>
    </div>
  );
};

export default TacticalBrief;
