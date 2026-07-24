
import React, { useState, useEffect } from 'react';
import RDWorkspace from './components/RDWorkspace';
import CameraGestureEngine from './components/CameraGestureEngine';
import AuthPortal from './components/AuthPortal';
import JaneBotChat from './components/JaneBotChat';
import Dashboard from './components/Dashboard';
import IdentityHub from './components/IdentityHub';
import ThinkingHats from './components/ThinkingHats';
import CyberRange from './components/CyberRange';
import Settings from './components/Settings';
import SecurityLogs from './components/SecurityLogs';
import TacticalEngine from './components/TacticalEngine';
import { Home, User, Brain, Settings as SettingsIcon, LayoutGrid, Target, History, Crosshair } from 'lucide-react';

type ViewState = 'hub' | 'dashboard' | 'identity' | 'hats' | 'settings' | 'range' | 'ledger' | 'tactics';

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [gestureData, setGestureData] = useState<any>(null);
  const [activeView, setActiveView] = useState<ViewState>('tactics');

  useEffect(() => {
    const handleGesture = (e: any) => setGestureData(e.detail);
    window.addEventListener('optical_gesture', handleGesture);
    return () => window.removeEventListener('optical_gesture', handleGesture);
  }, []);

  if (!isLoggedIn) {
    return <AuthPortal onLogin={() => setIsLoggedIn(true)} />;
  }

  const renderView = () => {
    switch (activeView) {
      case 'dashboard': return <Dashboard />;
      case 'identity': return <IdentityHub />;
      case 'hats': return <ThinkingHats />;
      case 'settings': return <Settings />;
      case 'range': return <CyberRange />;
      case 'ledger': return <SecurityLogs />;
      case 'tactics': return <TacticalEngine />;
      default: return (
        <>
          <CameraGestureEngine />
          <RDWorkspace gestureData={gestureData} />
        </>
      );
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] text-slate-100 selection:bg-cyan-500/30 font-['Space_Grotesk']">
      <div className="fixed inset-0 pointer-events-none opacity-20 z-0">
        <div className="absolute inset-0 bg-[linear-gradient(rgba(34,211,238,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(34,211,238,0.05)_1px,transparent_1px)] bg-[size:100px_100px]" />
      </div>

      <main className={`relative z-10 ${activeView === 'hub' ? '' : 'pt-24 px-4 pb-48 md:pb-32'}`}>
        {renderView()}
      </main>

      {/* Primary Navigation - Elevated z-index and higher opacity background for legibility */}
      <nav className="fixed bottom-8 left-1/2 -translate-x-1/2 z-[500] w-[92%] max-w-3xl">
        <div className="etched-glass rounded-full p-2 flex items-center justify-between gap-1 border border-cyan-500/30 bg-slate-900/90 backdrop-blur-3xl shadow-[0_10px_50px_rgba(0,0,0,0.8)]">
          <NavButton active={activeView === 'hub'} onClick={() => setActiveView('hub')} icon={LayoutGrid} label="Hub" />
          <NavButton active={activeView === 'tactics'} onClick={() => setActiveView('tactics')} icon={Crosshair} label="Tactics" />
          <NavButton active={activeView === 'range'} onClick={() => setActiveView('range')} icon={Target} label="Range" />
          <NavButton active={activeView === 'ledger'} onClick={() => setActiveView('ledger')} icon={History} label="Audit" />
          <NavButton active={activeView === 'dashboard'} onClick={() => setActiveView('dashboard')} icon={Home} label="War Room" />
          <NavButton active={activeView === 'identity'} onClick={() => setActiveView('identity')} icon={User} label="Vaults" />
          <NavButton active={activeView === 'hats'} onClick={() => setActiveView('hats')} icon={Brain} label="Thinking" />
          <NavButton active={activeView === 'settings'} onClick={() => setActiveView('settings')} icon={SettingsIcon} label="Core" />
        </div>
      </nav>

      <JaneBotChat />

      <div className="fixed top-4 left-6 md:bottom-8 md:left-8 md:top-auto flex items-center gap-4 text-[9px] font-black uppercase tracking-[0.4em] text-slate-500 z-[100]">
        <div className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse" />
        <span className="hidden sm:inline">Tactical Link:</span> Verified Operator
      </div>
    </div>
  );
};

const NavButton = ({ active, onClick, icon: Icon, label }: any) => (
  <button 
    onClick={onClick}
    className={`flex-1 flex flex-col items-center py-2.5 rounded-full transition-all duration-500 ${active ? 'bg-white/10 text-white' : 'text-slate-500 hover:text-slate-300'}`}
  >
    <Icon size={18} className={active ? 'scale-110 text-cyan-400' : ''} />
    <span className="text-[7px] font-black uppercase tracking-tighter mt-1">{label}</span>
  </button>
);

export default App;
