
import React, { useState, useEffect, useRef } from 'react';
import { Hash, Delete, CornerDownLeft, Space, Zap, Key } from 'lucide-react';

interface NeuralBoardProps {
  onInput: (char: string) => void;
  onDelete: () => void;
  onEnter: () => void;
}

const NeuralBoard: React.FC<NeuralBoardProps> = ({ onInput, onDelete, onEnter }) => {
  const [hoveredKey, setHoveredKey] = useState<string | null>(null);
  const [active, setActive] = useState(false);
  const [cursorPos, setCursorPos] = useState({ x: 50, y: 50 }); // Percentage

  const keys = [
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M'],
  ];

  useEffect(() => {
    const handleGesture = (e: any) => {
      const { midX, midY, shards } = e.detail;
      if (shards >= 1) {
        setActive(true);
        // Map 320x240 to 100x100
        setCursorPos({ x: (midX / 320) * 100, y: (midY / 240) * 100 });
      } else {
        setActive(false);
      }
    };

    const handleStamp = (e: any) => {
      if (hoveredKey) {
        if (hoveredKey === 'DEL') onDelete();
        else if (hoveredKey === 'ENT') onEnter();
        else onInput(hoveredKey);
      }
    };

    window.addEventListener('optical_gesture', handleGesture);
    window.addEventListener('optical_stamp', handleStamp);
    return () => {
      window.removeEventListener('optical_gesture', handleGesture);
      window.removeEventListener('optical_stamp', handleStamp);
    };
  }, [hoveredKey, onDelete, onEnter, onInput]);

  if (!active) return null;

  return (
    <div className="fixed inset-0 z-[150] pointer-events-none flex items-center justify-center">
      {/* Target Reticle */}
      <div 
        style={{ left: `${cursorPos.x}%`, top: `${cursorPos.y}%` }}
        className="absolute w-12 h-12 border-2 border-emerald-500 rounded-full -translate-x-1/2 -translate-y-1/2 transition-all duration-75 flex items-center justify-center"
      >
        <div className="w-1 h-1 bg-emerald-500 rounded-full animate-ping" />
        <div className="absolute inset-0 border border-white/10 rounded-full animate-spin-slow" />
      </div>

      {/* The Floating Board */}
      <div className="etched-glass p-8 rounded-[3rem] border border-emerald-500/20 shadow-[0_0_100px_rgba(16,185,129,0.1)] backdrop-blur-3xl animate-in zoom-in-95 duration-500 max-w-2xl w-full">
        <div className="flex items-center gap-3 mb-6">
          <Key size={16} className="text-emerald-500" />
          <h4 className="text-[10px] font-black uppercase tracking-[0.4em] text-emerald-500/60">Vortex Neural Input</h4>
        </div>

        <div className="space-y-3">
          {keys.map((row, i) => (
            <div key={i} className="flex justify-center gap-2">
              {row.map(k => (
                <KeyElement 
                  key={k} 
                  label={k} 
                  cursorX={cursorPos.x} 
                  cursorY={cursorPos.y} 
                  onHoverChange={setHoveredKey} 
                />
              ))}
            </div>
          ))}
          <div className="flex justify-center gap-2 pt-2">
            <KeyElement label="DEL" icon={<Delete size={14}/>} cursorX={cursorPos.x} cursorY={cursorPos.y} onHoverChange={setHoveredKey} />
            <KeyElement label=" " icon={<Space size={14}/>} cursorX={cursorPos.x} cursorY={cursorPos.y} onHoverChange={setHoveredKey} />
            <KeyElement label="ENT" icon={<CornerDownLeft size={14}/>} cursorX={cursorPos.x} cursorY={cursorPos.y} onHoverChange={setHoveredKey} />
          </div>
        </div>

        <p className="mt-8 text-center text-[8px] font-black uppercase tracking-[0.5em] text-slate-500 animate-pulse">
          Jab forward to Stamp Shard
        </p>
      </div>
    </div>
  );
};

const KeyElement = ({ label, icon, cursorX, cursorY, onHoverChange }: any) => {
  const ref = useRef<HTMLDivElement>(null);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const centerX = (rect.left + rect.width / 2) / window.innerWidth * 100;
    const centerY = (rect.top + rect.height / 2) / window.innerHeight * 100;
    
    const dist = Math.hypot(cursorX - centerX, cursorY - centerY);
    const hovering = dist < 2.5; // Detection radius
    
    if (hovering !== isHovered) {
      setIsHovered(hovering);
      if (hovering) onHoverChange(label);
    }
  }, [cursorX, cursorY, isHovered, label, onHoverChange]);

  return (
    <div 
      ref={ref}
      className={`w-12 h-12 flex items-center justify-center rounded-xl transition-all duration-300 border ${
        isHovered 
          ? 'bg-emerald-500 text-slate-950 border-emerald-400 scale-125 shadow-[0_0_20px_rgba(16,185,129,0.5)]' 
          : 'bg-white/5 text-slate-400 border-white/5'
      }`}
    >
      {icon ? icon : <span className="font-black text-sm">{label}</span>}
    </div>
  );
};

export default NeuralBoard;
