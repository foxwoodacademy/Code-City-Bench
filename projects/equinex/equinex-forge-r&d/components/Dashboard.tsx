
import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Cpu, Activity, Layers, ArrowUpRight, ShieldAlert, Zap, FileText, Search, ShieldCheck } from 'lucide-react';
import { useSecurityMesh } from '../hooks/useSecurityMesh';
import { SecurityAgent } from '../types';

const data = [
  { name: '00:00', risk: 10 },
  { name: '04:00', risk: 25 },
  { name: '08:00', risk: 45 },
  { name: '12:00', risk: 30 },
  { name: '16:00', risk: 65 },
  { name: '20:00', risk: 40 },
  { name: '23:59', risk: 15 },
];

const Dashboard: React.FC = () => {
  const mesh = useSecurityMesh();
  const [isGeneratingAudit, setIsGeneratingAudit] = useState(false);

  const generateAudit = async () => {
    setIsGeneratingAudit(true);
    // Logic for JaneBot to trigger 'generate_audit_report' would go here
    await new Promise(r => setTimeout(r, 2000));
    setIsGeneratingAudit(false);
    alert("Executive Audit Generated. Accessing encrypted PDF link...");
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-20 animate-in fade-in duration-1000">
      <header className="flex flex-col md:flex-row md:items-start justify-between gap-8">
        <div className="flex items-center gap-6">
          <div className="w-16 h-16 bg-emerald-500/10 rounded-[2rem] flex items-center justify-center border border-emerald-500/20 shadow-2xl">
            <ShieldCheck className="text-emerald-400" size={32} />
          </div>
          <div>
            <h2 className="text-5xl font-black tracking-tighter text-white uppercase italic">War Room</h2>
            <p className="text-[10px] font-black uppercase tracking-[0.4em] text-slate-500 mt-1">Live Vulnerability Assessment Mesh</p>
          </div>
        </div>
        
        <div className="flex gap-4">
          <button 
            onClick={generateAudit}
            disabled={isGeneratingAudit}
            className="etched-glass px-8 py-4 flex items-center gap-3 hover:bg-emerald-500/10 group transition-all"
          >
            {isGeneratingAudit ? <Activity className="animate-spin" size={18} /> : <FileText className="text-emerald-500 group-hover:scale-110 transition-transform" size={18} />}
            <span className="text-[10px] font-black uppercase tracking-widest text-white">Generate Audit</span>
          </button>
          
          <div className="etched-glass px-8 py-4 flex items-center gap-6 border-emerald-500/30">
            <div className="text-right">
              <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Global Risk</p>
              <p className={`text-2xl font-black tracking-tighter ${mesh.globalRisk > 50 ? 'text-red-500 animate-pulse' : 'text-emerald-400'}`}>
                {mesh.globalRisk.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left: Intelligence Feed */}
        <div className="lg:col-span-8 space-y-8">
          <div className="etched-glass p-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-5">
              <Search size={120} className="text-emerald-500" />
            </div>
            <div className="flex justify-between items-center mb-8 relative z-10">
              <h3 className="text-lg font-black uppercase tracking-tight flex items-center gap-3">
                <Activity size={18} className="text-emerald-400" /> Neural Drift Telemetry
              </h3>
            </div>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data}>
                  <defs>
                    <linearGradient id="riskGlow" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={mesh.globalRisk > 50 ? "#ef4444" : "#10b981"} stopOpacity={0.2}/>
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="5 5" vertical={false} stroke="rgba(255,255,255,0.03)" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#475569', fontSize: 10}} />
                  <YAxis hide />
                  <Area type="stepAfter" dataKey="risk" stroke={mesh.globalRisk > 50 ? "#ef4444" : "#10b981"} strokeWidth={3} fill="url(#riskGlow)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {mesh.agents.map(agent => (
              <div key={agent.id} className="etched-glass p-6 border-white/5 hover:border-emerald-500/20 transition-all">
                <div className="flex justify-between items-start mb-4">
                  <div className="p-3 bg-white/5 rounded-xl text-emerald-500"><Cpu size={18} /></div>
                  <div className="text-right">
                     <span className="text-[8px] font-black uppercase tracking-widest text-slate-600">{agent.type}</span>
                     <div className="text-xs font-bold text-white mt-1">{agent.status}</div>
                  </div>
                </div>
                <h4 className="font-bold text-lg mb-4">{agent.name}</h4>
                <div className="space-y-2">
                  <div className="flex justify-between text-[9px] font-black uppercase text-slate-500 tracking-widest">
                    <span>Node Load</span>
                    <span className="text-white">{Math.round(agent.load)}%</span>
                  </div>
                  <div className="h-1 bg-white/5 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500" style={{ width: `${agent.load}%` }} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Active Vulnerability List */}
        <div className="lg:col-span-4">
           <div className="etched-glass p-8 h-full bg-slate-900/40 border-emerald-500/10">
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-lg font-black uppercase tracking-tight">Active Exploits</h3>
                <ShieldAlert className="text-red-500 animate-pulse" size={20} />
              </div>
              
              <div className="space-y-4">
                {mesh.activeTriggers.map((trig) => (
                  <div key={trig.id} className="p-6 bg-black/40 rounded-[2rem] border border-white/5 group hover:border-red-500/40 transition-all">
                    <div className="flex justify-between items-center mb-3">
                      <span className={`text-[8px] font-black uppercase tracking-[0.2em] px-3 py-1 rounded-full ${trig.severity === 'Critical' ? 'bg-red-500/20 text-red-500' : 'bg-orange-500/10 text-orange-400'}`}>
                        {trig.severity}
                      </span>
                      <ArrowUpRight size={14} className="text-slate-700 group-hover:text-emerald-500 transition-colors" />
                    </div>
                    <h5 className="font-black text-sm text-white uppercase italic tracking-tight">{trig.name}</h5>
                    <p className="text-[11px] text-slate-500 mt-2 leading-relaxed">{trig.description}</p>
                    <div className="mt-4 flex gap-2">
                       <button className="text-[8px] font-black uppercase tracking-widest text-emerald-500 hover:text-white transition-colors">Patch Node</button>
                       <span className="text-slate-800">•</span>
                       <button className="text-[8px] font-black uppercase tracking-widest text-slate-600 hover:text-red-500">Isolate</button>
                    </div>
                  </div>
                ))}
              </div>
           </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
