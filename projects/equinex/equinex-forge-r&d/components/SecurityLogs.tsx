
import React, { useState } from 'react';
import { Search, Filter, CheckCircle2, AlertTriangle, Info, Terminal, Fingerprint, MapPin, Zap, Activity, Shield, Skull, BookOpen, ShieldCheck, History, Crosshair } from 'lucide-react';
import { useSecurityMesh } from '../hooks/useSecurityMesh';

const SecurityLogs: React.FC = () => {
  const mesh = useSecurityMesh();
  const [activeTab, setActiveTab] = useState<'system' | 'knowledge' | 'exercise'>('knowledge');

  return (
    <div className="max-w-7xl mx-auto space-y-12 pb-24 animate-in fade-in duration-700">
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-8">
        <div className="flex items-center gap-6">
          <div className="w-20 h-20 bg-emerald-500/10 rounded-[2.5rem] flex items-center justify-center text-emerald-400 border border-emerald-500/20 shadow-2xl shadow-emerald-500/10">
            <History size={40} />
          </div>
          <div>
            <h2 className="text-5xl font-black tracking-tighter text-white uppercase italic">Sovereign Audit Ledger</h2>
            <p className="text-slate-500 font-medium text-lg italic">Immutable record of system state and <span className="text-emerald-400">Knowledge Transfer</span>.</p>
          </div>
        </div>
        
        <div className="flex gap-4">
          <div className="etched-glass px-8 py-4 flex items-center gap-4 border-emerald-500/30">
             <div className="flex flex-col items-end">
                <span className="text-[9px] font-black uppercase tracking-widest text-slate-500">Vetting Pulse</span>
                <span className="text-lg font-black text-emerald-400">ACTIVE - 99.8% Verified</span>
             </div>
             <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse" />
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-10">
        <div className="lg:col-span-1 space-y-8">
           <div className="etched-glass p-8 space-y-6">
              <h4 className="text-[10px] font-black uppercase tracking-[0.5em] text-slate-600">Audit Scopes</h4>
              <nav className="space-y-2">
                 <AuditTab active={activeTab === 'knowledge'} onClick={() => setActiveTab('knowledge')} icon={BookOpen} label="Knowledge Shards" />
                 <AuditTab active={activeTab === 'exercise'} onClick={() => setActiveTab('exercise')} icon={Crosshair} label="Exercise Log" />
                 <AuditTab active={activeTab === 'system'} onClick={() => setActiveTab('system')} icon={Terminal} label="System Events" />
              </nav>
           </div>
           
           <div className="etched-glass p-8">
              <h4 className="text-[10px] font-black uppercase tracking-[0.5em] text-slate-600 mb-6">Ledger Health</h4>
              <div className="space-y-6">
                 <MetricBar label="Verification Rate" val={99} color="text-emerald-400" />
                 <MetricBar label="Log Integrity" val={100} color="text-blue-400" />
                 <MetricBar label="Operator Trust" val={84} color="text-purple-400" />
              </div>
           </div>
        </div>

        <div className="lg:col-span-3">
          <div className="etched-glass rounded-[3.5rem] overflow-hidden border-white/5 bg-slate-900/40">
             <div className="p-10 border-b border-white/5 flex justify-between items-center">
                <h3 className="text-xl font-black uppercase tracking-tight flex items-center gap-3">
                   {activeTab === 'knowledge' ? <BookOpen className="text-emerald-500" /> : 
                    activeTab === 'exercise' ? <Crosshair className="text-red-500" /> : <Terminal className="text-blue-500" />}
                   {activeTab === 'knowledge' ? 'Session Knowledge Transfers' : 
                    activeTab === 'exercise' ? 'Pentest Exercise Logs' : 'Core System Ledger'}
                </h3>
                <div className="flex gap-2">
                   <div className="px-4 py-2 bg-white/5 rounded-xl text-[10px] font-black uppercase tracking-widest text-slate-500">
                      Total Entries: {activeTab === 'knowledge' ? mesh.auditLedger.length : 
                                      activeTab === 'exercise' ? mesh.pentestHistory.length : '1,240'}
                   </div>
                </div>
             </div>

             <div className="p-4">
               {activeTab === 'knowledge' && (
                 <div className="space-y-4">
                    {mesh.auditLedger.length > 0 ? mesh.auditLedger.map((log) => (
                       <KnowledgeRow key={log.id} log={log} />
                    )) : (
                      <div className="p-20 text-center text-slate-600">
                         <Activity size={40} className="mx-auto mb-4 opacity-20" />
                         <p className="text-[10px] font-black uppercase tracking-[0.3em]">No Knowledge Shards Anchored in Current Session</p>
                      </div>
                    )}
                 </div>
               )}

               {activeTab === 'exercise' && (
                 <div className="space-y-4">
                    {mesh.pentestHistory.length > 0 ? mesh.pentestHistory.map((outcome) => (
                       <ExerciseRow key={outcome.id} outcome={outcome} />
                    )) : (
                      <div className="p-20 text-center text-slate-600">
                         <Skull size={40} className="mx-auto mb-4 opacity-20" />
                         <p className="text-[10px] font-black uppercase tracking-[0.3em]">No Pentest Exercises Logged</p>
                      </div>
                    )}
                 </div>
               )}

               {activeTab === 'system' && (
                 <div className="space-y-1">
                    {[...Array(6)].map((_, i) => (
                      <div key={i} className="flex items-center justify-between p-6 hover:bg-white/5 transition-all rounded-2xl group border border-transparent hover:border-white/5">
                        <div className="flex items-center gap-6">
                           <div className="w-10 h-10 bg-blue-500/10 text-blue-400 rounded-xl flex items-center justify-center font-mono text-[10px]">#0{i+1}</div>
                           <div>
                              <p className="font-black text-sm text-white uppercase italic tracking-tight">Core System Pulse {i}</p>
                              <p className="text-[9px] text-slate-600 uppercase font-black tracking-widest">Shard Sync • 04:2{i}:01</p>
                           </div>
                        </div>
                        <div className="flex items-center gap-4">
                           <span className="text-[8px] font-black uppercase tracking-[0.2em] text-slate-700">SHA-256 Verified</span>
                           <ShieldCheck size={14} className="text-emerald-500/40" />
                        </div>
                      </div>
                    ))}
                 </div>
               )}
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const KnowledgeRow: React.FC<{ log: any }> = ({ log }) => (
  <div className="p-8 bg-black/40 rounded-[2.5rem] border border-white/5 hover:border-emerald-500/20 transition-all group">
    <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div className="flex items-center gap-6">
        <div className="w-14 h-14 bg-emerald-500/10 text-emerald-500 rounded-2xl flex items-center justify-center">
          <BookOpen size={24} />
        </div>
        <div>
          <div className="flex items-center gap-3">
             <h5 className="text-lg font-black text-white uppercase italic tracking-tight group-hover:text-emerald-400 transition-colors">{log.concept}</h5>
             <span className="px-3 py-0.5 bg-emerald-500/10 text-emerald-500 rounded text-[8px] font-black uppercase tracking-widest">{log.depth}</span>
          </div>
          <p className="text-xs text-slate-500 font-bold uppercase tracking-widest mt-1">Vector: {log.vector}</p>
        </div>
      </div>
      <div className="flex items-center gap-8">
         <div className="text-right">
            <p className="text-[9px] font-black text-slate-600 uppercase tracking-widest">Session Anchor</p>
            <p className="text-[10px] font-mono text-slate-400 mt-1">{new Date(log.timestamp).toLocaleTimeString()}</p>
         </div>
         <div className="flex items-center gap-2 px-4 py-2 bg-emerald-500/5 border border-emerald-500/10 rounded-xl">
            <CheckCircle2 size={14} className="text-emerald-500" />
            <span className="text-[9px] font-black text-emerald-500 uppercase tracking-widest">Vetted</span>
         </div>
      </div>
    </div>
  </div>
);

const ExerciseRow: React.FC<{ outcome: any }> = ({ outcome }) => (
  <div className="p-8 bg-black/40 rounded-[2.5rem] border border-white/5 hover:border-red-500/20 transition-all group">
    <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div className="flex items-center gap-6">
        <div className={`w-14 h-14 rounded-2xl flex items-center justify-center ${outcome.result === 'Success' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'}`}>
          <Skull size={24} />
        </div>
        <div>
          <div className="flex items-center gap-3">
             <h5 className="text-lg font-black text-white uppercase italic tracking-tight group-hover:text-red-400 transition-colors">{outcome.stepLabel}</h5>
             <span className={`px-3 py-0.5 rounded text-[8px] font-black uppercase tracking-widest ${outcome.result === 'Success' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>{outcome.result}</span>
          </div>
          <p className="text-xs text-slate-400 mt-2 font-medium leading-relaxed max-w-xl">{outcome.details}</p>
          {outcome.vulnerabilityIdentified && (
            <p className="text-[9px] text-slate-500 font-black uppercase tracking-widest mt-2 italic">Vector: {outcome.vulnerabilityIdentified}</p>
          )}
        </div>
      </div>
      <div className="flex items-center gap-8 shrink-0">
         <div className="text-right">
            <p className="text-[9px] font-black text-slate-600 uppercase tracking-widest">Simulation Stamp</p>
            <p className="text-[10px] font-mono text-slate-400 mt-1 italic">{new Date(outcome.timestamp).toLocaleTimeString()} [{outcome.timestamp}]</p>
         </div>
      </div>
    </div>
  </div>
);

const AuditTab = ({ active, onClick, icon: Icon, label }: any) => (
  <button 
    onClick={onClick}
    className={`w-full p-4 rounded-2xl flex items-center gap-4 transition-all ${active ? 'bg-white/10 text-white' : 'text-slate-500 hover:bg-white/5 hover:text-slate-300'}`}
  >
    <Icon size={18} className={active ? (label === 'Exercise Log' ? 'text-red-500' : 'text-emerald-400') : ''} />
    <span className="text-[10px] font-black uppercase tracking-widest">{label}</span>
  </button>
);

const MetricBar = ({ label, val, color }: any) => (
  <div className="space-y-3">
     <div className="flex justify-between text-[10px] font-black uppercase tracking-widest text-slate-500">
        <span>{label}</span>
        <span className="text-white">{val}%</span>
     </div>
     <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
        <div className={`h-full ${color.replace('text', 'bg')} transition-all duration-1000`} style={{ width: `${val}%` }} />
     </div>
  </div>
);

export default SecurityLogs;
