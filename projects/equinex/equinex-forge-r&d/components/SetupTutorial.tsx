import React, { useState } from 'react';
import { Zap, ChevronRight, Check, Shield, MousePointer2, Mic, Eye, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';

const Step = ({ active, completed, title, icon: Icon }: any) => (
  <div className={`flex items-center gap-4 transition-all duration-500 ${active ? 'opacity-100' : 'opacity-30'}`}>
    <div className={`w-10 h-10 rounded-xl flex items-center justify-center border ${completed ? 'bg-emerald-500 border-emerald-500 text-slate-950' : (active ? 'border-emerald-500 text-emerald-500 animate-pulse' : 'border-white/10 text-slate-600')}`}>
      {completed ? <Check size={20} /> : <Icon size={20} />}
    </div>
    <span className={`text-[10px] font-black uppercase tracking-widest ${active ? 'text-white' : 'text-slate-700'}`}>{title}</span>
  </div>
);

const SetupTutorial: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    { title: 'Neural Link', icon: Zap, content: 'Initialize your connection to the Modmind Core. Every session starts with a verified neural handshake.' },
    { title: 'Cognitive Sync', icon: Sparkles, content: 'Calibrate the Six Thinking Hats. Choose a hat via voice command: "Jane, activate Black Hat".' },
    { title: 'Optical Gesture', icon: Eye, content: 'Enable Kinetic Link to control the interface via hand gestures. Use the camera for precision stamping.' },
    { title: 'Red Team Prep', icon: Shield, content: 'Harden your security. Turn on Red Team Lockdown in settings to test your system against hostile probes.' },
  ];

  return (
    <div className="max-w-4xl mx-auto py-12 space-y-12 animate-in fade-in zoom-in-95 duration-700">
      <header className="text-center space-y-4">
        <h1 className="text-5xl font-black uppercase tracking-tighter text-white italic">Onboarding Shard</h1>
        <p className="text-slate-500 font-medium">Initialize your Operator interface in 4 tactical phases.</p>
      </header>

      <div className="etched-glass p-12 rounded-[4rem] border-white/5 relative overflow-hidden">
        <div className="flex justify-between mb-16 px-4">
          {steps.map((s, i) => (
            <Step key={i} title={s.title} icon={s.icon} active={currentStep === i} completed={currentStep > i} />
          ))}
        </div>

        <div className="space-y-8 min-h-[200px] flex flex-col justify-center items-center text-center">
          <div className="w-24 h-24 bg-emerald-500/10 rounded-[2rem] flex items-center justify-center text-emerald-400 border border-emerald-500/20 mb-6">
            {React.createElement(steps[currentStep].icon, { size: 40 })}
          </div>
          <h3 className="text-3xl font-black uppercase text-white tracking-tight">{steps[currentStep].title}</h3>
          <p className="text-slate-400 max-w-lg leading-relaxed">{steps[currentStep].content}</p>
        </div>

        <div className="mt-16 flex justify-between items-center">
          <button 
            disabled={currentStep === 0}
            onClick={() => setCurrentStep(s => s - 1)}
            className="text-[10px] font-black uppercase tracking-widest text-slate-700 hover:text-white transition-colors disabled:opacity-0"
          >
            Back
          </button>
          
          {currentStep < steps.length - 1 ? (
            <button 
              onClick={() => setCurrentStep(s => s + 1)}
              className="px-10 py-4 bg-emerald-500 text-slate-950 rounded-2xl font-black uppercase text-[10px] tracking-widest flex items-center gap-2 hover:scale-[1.05] transition-all"
            >
              Sync Next <ChevronRight size={14} />
            </button>
          ) : (
            <Link 
              to="/"
              className="px-10 py-4 bg-white text-slate-950 rounded-2xl font-black uppercase text-[10px] tracking-widest flex items-center gap-2 hover:bg-emerald-500 transition-all"
            >
              Initialize Hub <Zap size={14} />
            </Link>
          )}
        </div>
      </div>
    </div>
  );
};

export default SetupTutorial;