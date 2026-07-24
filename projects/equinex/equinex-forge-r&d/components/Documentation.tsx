import React from 'react';
import { Book, Code, Shield, Terminal, Zap, Hash, Layers, Cpu, Globe, Brain } from 'lucide-react';

const DocSection = ({ title, children, icon: Icon }: any) => (
  <section className="space-y-6">
    <div className="flex items-center gap-4 group">
      <div className="p-3 bg-white/5 rounded-xl text-slate-500 group-hover:text-emerald-400 transition-colors">
        <Icon size={20} />
      </div>
      <h2 className="text-2xl font-black uppercase tracking-tight text-white">{title}</h2>
    </div>
    <div className="etched-glass p-8 rounded-[2.5rem] border-white/5 leading-relaxed text-slate-400">
      {children}
    </div>
  </section>
);

const CodeBlock = ({ code }: { code: string }) => (
  <div className="bg-black/40 rounded-2xl p-6 my-4 border border-white/5 font-mono text-xs overflow-x-auto">
    <pre className="text-emerald-400"><code>{code}</code></pre>
  </div>
);

const Documentation: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto space-y-16 pb-24 animate-in fade-in duration-1000">
      <header className="space-y-4">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/5 border border-white/10 text-[10px] font-black uppercase tracking-[0.4em] text-slate-500">
          <Book size={12} /> Technical Repository v2.9
        </div>
        <h1 className="text-6xl font-black tracking-tighter text-white uppercase italic">System Shards</h1>
        <p className="text-slate-500 max-w-2xl font-medium text-lg">
          Developer technical specifications for the Equinex-Modmind Universal Authentication Hub.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-12">
        <div className="lg:col-span-1 space-y-8">
          <nav className="sticky top-24 space-y-4">
            {['Architecture', 'Thinking Hats', 'JaneBot AI', 'Security Hardening', 'AFiREfly Protocol'].map(item => (
              <button key={item} className="w-full text-left px-4 py-2 text-[10px] font-black uppercase tracking-widest text-slate-600 hover:text-emerald-400 transition-colors">
                {item}
              </button>
            ))}
          </nav>
        </div>

        <div className="lg:col-span-3 space-y-20">
          <DocSection title="Core Architecture" icon={Layers}>
            <p>The Modmind Hub utilizes a <strong>Zero-Trust Shard Architecture</strong>. Every component—from Identity Vaults to the Security Mesh—operates as an isolated node linked via post-quantum handshakes.</p>
            <CodeBlock code={`// Example Shard Handshake
const shard = await Mesh.link('identity-vault-01');
shard.verify(operator.bioHash);
shard.synchronize();`} />
          </DocSection>

          {/* Added missing Brain import to fix 'Cannot find name Brain' error */}
          <DocSection title="Thinking Hat Integration" icon={Brain}>
            <p>Our <strong>Cognitive Core</strong> forces AI reasoning through six distinct philosophical lenses. This is not just a UI change; it alters the Gemini temperature, system instructions, and tool access in real-time.</p>
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
              <li className="p-4 bg-white/5 rounded-2xl border border-white/5">
                <span className="text-white font-bold block mb-1">Black Hat</span>
                Brutal auditing and risk assessment. No buffers.
              </li>
              <li className="p-4 bg-white/5 rounded-2xl border border-white/5">
                <span className="text-red-400 font-bold block mb-1">Red Hat</span>
                Instinctual and emotional resonance. Gut feelings.
              </li>
            </ul>
          </DocSection>

          <DocSection title="Security Hardening" icon={Shield}>
            <p>For Red Team tests, the hub implements <strong>Autonomous Lockdown</strong>. If suspicious behavior is detected in the input stream, JaneBot triggers a UI freeze and forces a manual Shard Reset.</p>
            <CodeBlock code={`protocol.redTeam_Lockdown({
  threat: 'Injection Attempt',
  severity: 98,
  action: 'UI_FREEZE'
});`} />
          </DocSection>

          <DocSection title="AFiREfly Stamper" icon={Zap}>
            <p>The AFiREfly Stamper allows JaneBot to directly modify the hub state. This is an elevated model privilege that must be enabled in System Settings.</p>
            <div className="flex gap-4 mt-8">
               <div className="px-6 py-4 bg-emerald-500/10 border border-emerald-500/20 rounded-3xl flex-1">
                 <h4 className="text-[10px] font-black uppercase tracking-widest text-emerald-400 mb-2">Endpoint</h4>
                 <code className="text-xs text-white">#fly-preset-combat</code>
               </div>
               <div className="px-6 py-4 bg-blue-500/10 border border-blue-500/20 rounded-3xl flex-1">
                 <h4 className="text-[10px] font-black uppercase tracking-widest text-blue-400 mb-2">Endpoint</h4>
                 <code className="text-xs text-white">#mode-cynic</code>
               </div>
            </div>
          </DocSection>
        </div>
      </div>
    </div>
  );
};

export default Documentation;