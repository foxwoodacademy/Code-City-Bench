
import React, { useState, useRef, useEffect } from 'react';
import { Send, X, Minus, Zap, Volume2, VolumeX, Mic, Layers, MicOff, Skull, Hash, Brain, Terminal, ShieldAlert, Activity, ShieldCheck, Crosshair } from 'lucide-react';
import { getJaneBotResponse, getJaneBotVoice } from '../services/gemini';
import { ChatMessage, ThinkingHatColor } from '../types';
import { useSecurityMesh } from '../hooks/useSecurityMesh';

const JaneBotChat: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [isVoiceEnabled, setIsVoiceEnabled] = useState(true);
  const [activeHat, setActiveHat] = useState<ThinkingHatColor>((localStorage.getItem('active_hat') as ThinkingHatColor) || 'Blue');
  const [isRedTeam, setIsRedTeam] = useState(localStorage.getItem('red_team_lockdown') === 'true');
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'assistant', content: "Grandmaster link established. The board is set. State your opening gambit.", timestamp: Date.now() }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const { anchorKnowledge, addCampaign, logPentest } = useSecurityMesh();
  
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    const handleShift = (e: any) => setActiveHat(e.detail.hat);
    const handleRedTeam = (e: any) => setIsRedTeam(e.detail.locked);
    window.addEventListener('cognitive_shift', handleShift);
    window.addEventListener('red_team_toggle', handleRedTeam);
    return () => {
      window.removeEventListener('cognitive_shift', handleShift);
      window.removeEventListener('red_team_toggle', handleRedTeam);
    };
  }, []);

  const getHatColor = (hat: ThinkingHatColor) => {
    if (isRedTeam) return 'red-500';
    switch(hat) {
      case 'White': return 'cyan-100';
      case 'Red': return 'red-500';
      case 'Black': return 'cyan-500';
      case 'Yellow': return 'yellow-400';
      case 'Green': return 'emerald-400';
      case 'Blue': return 'cyan-400';
      default: return 'cyan-400';
    }
  };

  const color = getHatColor(activeHat);

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg: ChatMessage = { role: 'user', content: input, timestamp: Date.now() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    const response = await getJaneBotResponse([...messages, userMsg], activeHat, isRedTeam);
    
    let systemStatus = "";
    if (response.toolCalls) {
      for (const fc of response.toolCalls) {
        if (fc.name === 'log_knowledge_transfer') {
          anchorKnowledge(fc.args.concept, fc.args.vector, fc.args.depth);
          systemStatus += `[ANCHOR: ${fc.args.concept}] `;
        }
        if (fc.name === 'plot_tactical_campaign') {
          addCampaign(fc.args.campaign_name, fc.args.objective, fc.args.steps);
          systemStatus += `[STRATEGY: ${fc.args.campaign_name}] `;
        }
        if (fc.name === 'report_pentest_simulation') {
          logPentest(fc.args.step_label, fc.args.result, fc.args.details, fc.args.vulnerability);
          systemStatus += `[PENTEST: ${fc.args.result}] `;
        }
      }
    }

    const finalResponseText = response.text || (systemStatus ? `Calculations complete. ${systemStatus}` : "Tactical move acknowledged.");

    if (isVoiceEnabled && finalResponseText) {
      const base64Audio = await getJaneBotVoice(finalResponseText, activeHat);
      if (base64Audio) playAudio(base64Audio);
    }

    setMessages(prev => [...prev, { role: 'assistant', content: finalResponseText, timestamp: Date.now() }]);
    setIsLoading(false);
  };

  const playAudio = async (base64: string) => {
    try {
      const context = new (window.AudioContext || (window as any).webkitAudioContext)({sampleRate: 24000});
      const buffer = await decodeAudioData(decodeBase64(base64), context, 24000, 1);
      const source = context.createBufferSource();
      source.buffer = buffer;
      source.connect(context.destination);
      source.start();
    } catch {}
  };

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)} 
        className={`fixed bottom-32 right-6 md:bottom-10 md:right-10 w-16 h-16 md:w-24 md:h-24 etched-glass rounded-full flex items-center justify-center shadow-2xl z-[110] group border transition-all duration-700 border-${color}/40 shadow-${color}/20 active:scale-90`}
      >
        {isRedTeam ? <ShieldAlert size={28} className="text-red-500 animate-pulse" /> : <Crosshair size={28} className={`text-${color} transition-all duration-700`} />}
      </button>
    );
  }

  return (
    <div className={`fixed bottom-0 right-0 md:bottom-10 md:right-10 z-[600] transition-all duration-700 ${isMinimized ? 'h-16 w-full md:w-72' : 'h-full md:h-[780px] w-full md:w-[540px]'} etched-glass flex flex-col overflow-hidden md:rounded-[3rem] border border-${color}/30 shadow-2xl`}>
      <div className={`p-6 md:p-8 flex items-center justify-between cursor-pointer border-b border-white/5 bg-slate-900/95 backdrop-blur-3xl`} onClick={() => isMinimized && setIsMinimized(false)}>
        <div className="flex items-center gap-4">
          <Activity size={20} className={`text-${color} animate-pulse`} />
          <div className="flex flex-col">
             <h3 className="font-black text-[10px] md:text-xs uppercase tracking-[0.4em] text-white">Grandmaster</h3>
             <span className={`text-[8px] font-black uppercase tracking-widest text-${color}`}>{isRedTeam ? 'TACTICAL ENGINE' : `${activeHat} SHARD ACTIVE`}</span>
          </div>
        </div>
        <div className="flex gap-2">
          <button onClick={(e) => { e.stopPropagation(); setIsMinimized(!isMinimized); }} className="p-2 hover:bg-white/5 rounded-xl text-slate-500"><Minus size={18} /></button>
          <button onClick={(e) => { e.stopPropagation(); setIsOpen(false); }} className="p-2 hover:bg-white/5 rounded-xl text-slate-500"><X size={18} /></button>
        </div>
      </div>

      {!isMinimized && (
        <>
          <div className="bg-black/60 px-6 py-2 md:px-10 md:py-3 border-b border-white/5 flex items-center justify-between">
             <div className="flex items-center gap-4">
               <ShieldCheck size={12} className="text-cyan-500" />
               <span className="text-[8px] font-black uppercase tracking-[0.4em] text-cyan-500/60">Tactical Link: Locked</span>
             </div>
             <div className="flex items-center gap-2">
                <div className={`w-1.5 h-1.5 rounded-full bg-${color} animate-pulse`} />
                <span className="text-[8px] font-black uppercase tracking-3em text-slate-600">Cognitive Stream</span>
             </div>
          </div>

          <div className="flex-1 p-6 md:p-10 overflow-y-auto space-y-8 md:space-y-12 scrollbar-hide bg-slate-950/20">
             {messages.map((msg, i) => (
               <div key={i} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} animate-in fade-in slide-in-from-bottom-2 duration-400`}>
                  <div className={`max-w-[95%] md:max-w-[90%] p-5 md:p-7 rounded-[2rem] md:rounded-[2.5rem] text-xs md:text-sm leading-relaxed ${msg.role === 'user' ? 'bg-white/5 text-cyan-50 border border-white/10' : `bg-${color}/10 text-slate-200 border border-${color}/20 shadow-lg`}`}>
                    {msg.content}
                  </div>
                  <span className="text-[8px] text-slate-600 mt-2 font-black uppercase tracking-[0.3em] mx-4">
                    {msg.role === 'user' ? 'Operator' : 'Grandmaster'}
                  </span>
               </div>
             ))}
             {isLoading && (
               <div className="flex flex-col items-start animate-pulse">
                  <div className={`w-24 h-12 bg-${color}/5 border border-${color}/10 rounded-full`} />
               </div>
             )}
             <div ref={chatEndRef} />
          </div>

          <form onSubmit={handleSend} className="p-6 md:p-10 bg-slate-900/90 border-t border-white/5 backdrop-blur-2xl">
            <div className="relative flex items-center gap-4 md:gap-5">
              <input 
                type="text" 
                value={input} 
                onChange={(e) => setInput(e.target.value)} 
                placeholder={isRedTeam ? "Combat Instructions Only..." : "State your move..."}
                disabled={isLoading}
                className="flex-1 bg-white/5 border border-white/5 rounded-2xl md:rounded-3xl px-6 py-4 md:px-8 md:py-6 text-xs md:text-sm focus:outline-none focus:border-cyan-500/30 transition-all font-medium"
              />
              <button type="submit" disabled={!input.trim()} className={`p-4 md:p-6 rounded-2xl md:rounded-3xl transition-all shadow-xl active:scale-95 disabled:opacity-20 bg-${color} text-slate-950 font-black`}>
                <Send size={18} />
              </button>
            </div>
          </form>
        </>
      )}
    </div>
  );
};

function decodeBase64(base64: string) {
  const binaryString = atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) bytes[i] = binaryString.charCodeAt(i);
  return bytes;
}

async function decodeAudioData(data: Uint8Array, ctx: AudioContext, sampleRate: number, numChannels: number): Promise<AudioBuffer> {
  const dataInt16 = new Int16Array(data.buffer);
  const frameCount = dataInt16.length / numChannels;
  const buffer = ctx.createBuffer(numChannels, frameCount, sampleRate);
  for (let channel = 0; channel < numChannels; channel++) {
    const channelData = buffer.getChannelData(channel);
    for (let i = 0; i < frameCount; i++) channelData[i] = dataInt16[i * numChannels + channel] / 32768.0;
  }
  return buffer;
}

export default JaneBotChat;
