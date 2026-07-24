
import React from 'react';
import { Users, Link2, ShieldCheck, Clock, Plus, UserPlus, ArrowUpRight } from 'lucide-react';
import { RemoteLink } from '../types';

const RemoteOversight: React.FC = () => {
  const linkedAccounts: RemoteLink[] = [
    { id: 'rl-1', name: 'Child Node (Sarah)', role: 'Family', accessLevel: 1, status: 'Linked' },
    { id: 'rl-2', name: 'Caregiver Alpha', role: 'Nanny', accessLevel: 2, status: 'Linked' },
    { id: 'rl-3', name: 'Supervisor Shard', role: 'Supervisor', accessLevel: 3, status: 'Pending' },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-10 pb-16 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-center gap-6">
          <div className="w-16 h-16 bg-purple-500/10 rounded-[2rem] flex items-center justify-center text-purple-400 border border-purple-500/20 shadow-2xl shadow-purple-500/10">
            <Users size={32} />
          </div>
          <div>
            <h2 className="text-4xl font-extrabold tracking-tighter text-white">Remote Oversight</h2>
            <p className="text-slate-500 font-medium text-lg">Manage linked identities and <span className="text-purple-400">Nanny Mode</span> shards.</p>
          </div>
        </div>
        <button className="px-6 py-4 bg-purple-500 text-white rounded-2xl font-bold shadow-xl shadow-purple-500/20 flex items-center gap-2 hover:scale-[1.02] transition-all active:scale-95">
          <Plus size={18} /> Link New Node
        </button>
      </div>

      <div className="grid gap-4">
        {linkedAccounts.map((account) => (
          <div key={account.id} className="glass p-6 rounded-[2.5rem] border border-white/5 flex items-center justify-between group hover:border-purple-500/30 transition-all">
            <div className="flex items-center gap-6">
              <div className={`w-14 h-14 rounded-2xl flex items-center justify-center ${account.status === 'Linked' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-orange-500/10 text-orange-400'}`}>
                <UserPlus size={24} />
              </div>
              <div>
                <h4 className="font-bold text-lg">{account.name}</h4>
                <div className="flex items-center gap-3 mt-1">
                  <span className="text-xs font-bold px-2 py-0.5 bg-white/5 rounded text-slate-400 uppercase tracking-widest">{account.role}</span>
                  <div className="w-1 h-1 bg-slate-700 rounded-full" />
                  <span className="text-xs text-slate-500">Access Level: {account.accessLevel}</span>
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="text-right hidden sm:block">
                <p className={`text-[10px] font-black uppercase tracking-widest ${account.status === 'Linked' ? 'text-emerald-500' : 'text-orange-500'}`}>{account.status}</p>
                <p className="text-[10px] text-slate-500 mt-1">Active Mesh Link</p>
              </div>
              <button className="p-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all">
                <ArrowUpRight size={18} className="text-slate-400 group-hover:text-white" />
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-purple-500/5 border border-purple-500/20 p-8 rounded-[3rem] flex items-start gap-6">
        <div className="p-4 bg-purple-500/20 rounded-2xl text-purple-400">
          <ShieldCheck size={28} />
        </div>
        <div>
          <h4 className="font-bold text-xl text-purple-400">Universal Nanny Mode</h4>
          <p className="text-sm text-slate-400 mt-2 leading-relaxed">
            Nanny Mode allows you to restrict certain ModMind interactions on linked accounts. Ideal for training agents or safeguarding family nodes from unauthorized Syntax commands.
          </p>
          <div className="mt-6 flex gap-3">
             <button className="px-6 py-2.5 bg-purple-500/20 text-purple-400 border border-purple-500/20 rounded-xl text-xs font-bold hover:bg-purple-500 hover:text-white transition-all">Configure Constraints</button>
             <button className="px-6 py-2.5 bg-white/5 text-slate-400 rounded-xl text-xs font-bold hover:bg-white/10 transition-all">Learn About Sharding</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RemoteOversight;
