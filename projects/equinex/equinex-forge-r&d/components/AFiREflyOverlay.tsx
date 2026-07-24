
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Ghost, X, Crosshair, Target, Shield, Zap, Sparkles, Wand2 } from 'lucide-react';
import { AfireflyPreset } from '../types';

const SNAP_MARGIN = 32;

const AFiREflyOverlay: React.FC = () => {
  const [pos, setPos] = useState({ x: window.innerWidth - 140, y: 100 });
  const [scale, setScale] = useState(1);
  const [opacity, setOpacity] = useState(1);
  const [isCalibrating, setIsCalibrating] = useState(false);
  const [calibProgress, setCalibProgress] = useState(0);
  const [isOpticalLinked, setIsOpticalLinked] = useState(false);
  const [showMacroRadial, setShowMacroRadial] = useState(false);
  
  const interactionRef = useRef({ offX: 0, offY: 0, initialDistance: 0, initialScale: 1 });

  const snapToEdge = useCallback((x: number, y: number) => {
    const w = window.innerWidth;
    const h = window.innerHeight;
    const targets = [
      { x: SNAP_MARGIN, y: SNAP_MARGIN }, // TL
      { x: w - 120 - SNAP_MARGIN, y: SNAP_MARGIN }, // TR
      { x: SNAP_MARGIN, y: h - 120 - SNAP_MARGIN }, // BL
      { x: w - 120 - SNAP_MARGIN, y: h - 120 - SNAP_MARGIN }, // BR
      { x: w/2 - 60, y: SNAP_MARGIN }, // TC
    ];
    let closest = targets[0];
    let minDist = Infinity;
    targets.forEach(t => {
      const d = Math.hypot(x - t.x, y - t.y);
      if (d < minDist) { minDist = d; closest = t; }
    });
    setPos(closest);
  }, []);

  useEffect(() => {
    const handleGesture = (e: any) => {
      const { distance, shards } = e.detail;
      if (shards === 2) {
        setIsOpticalLinked(true);
        if (interactionRef.current.initialDistance === 0) {
          interactionRef.current.initialDistance = distance;
          interactionRef.current.initialScale = scale;
        } else {
          const delta = distance / interactionRef.current.initialDistance;
          setScale(Math.max(0.5, Math.min(3, interactionRef.current.initialScale * delta)));
        }
      } else {
        setIsOpticalLinked(false);
        interactionRef.current.initialDistance = 0;
      }
    };

    const handleChop = () => {
      console.log("KINETIC CHOP DETECTED");
      setScale(s => s * 0.8);
      setTimeout(() => setScale(s => s / 0.8), 200);
    };

    const handlePoint = () => {
      setShowMacroRadial(true);
      setTimeout(() => setShowMacroRadial(false), 3000);
    };

    const handlePreset = (e: any) => {
      const { name } = e.detail;
      if (name === 'combat') {
        setPos({ x: window.innerWidth / 2 - 60, y: 50 });
        setScale(1.8);
        setOpacity(1);
      } else if (name === 'ghost') {
        setPos({ x: window.innerWidth - 150, y: window.innerHeight - 150 });
        setScale(0.8);
        setOpacity(0.3);
      }
    };

    window.addEventListener('optical_gesture', handleGesture);
    window.addEventListener('optical_chop', handleChop);
    window.addEventListener('optical_point', handlePoint);
    window.addEventListener('afirefly_preset_trigger', handlePreset);

    return () => {
      window.removeEventListener('optical_gesture', handleGesture);
      window.removeEventListener('optical_chop', handleChop);
      window.removeEventListener('optical_point', handlePoint);
      window.removeEventListener('afirefly_preset_trigger', handlePreset);
    };
  }, [scale]);

  return (
    <div 
      style={{ 
        left: `${pos.x}px`, top: `${pos.y}px`, 
        transform: `scale(${scale})`,
        opacity: opacity 
      }}
      className={`fixed z-[100] transition-all duration-500`}
      onMouseDown={(e) => {
        interactionRef.current.offX = e.clientX - pos.x;
        interactionRef.current.offY = e.clientY - pos.y;
        const onMove = (me: MouseEvent) => setPos({ x: me.clientX - interactionRef.current.offX, y: me.clientY - interactionRef.current.offY });
        const onUp = (ue: MouseEvent) => {
          snapToEdge(ue.clientX - interactionRef.current.offX, ue.clientY - interactionRef.current.offY);
          window.removeEventListener('mousemove', onMove);
          window.removeEventListener('mouseup', onUp);
        };
        window.addEventListener('mousemove', onMove);
        window.addEventListener('mouseup', onUp);
      }}
    >
      {/* Visual Calibration Ring */}
      {isCalibrating && (
        <div className="absolute inset-0 -m-8 border-4 border-emerald-500/20 rounded-full animate-spin">
           <div className="w-4 h-4 bg-emerald-500 rounded-full absolute top-0 left-1/2 -translate-x-1/2 shadow-[0_0_15px_#10b981]" />
        </div>
      )}

      {/* Main Shard Body */}
      <div className={`w-24 h-24 etched-glass rounded-full flex items-center justify-center relative group cursor-grab active:cursor-grabbing border ${isOpticalLinked ? 'border-emerald-400 shadow-[0_0_60px_rgba(16,185,129,0.3)]' : 'border-white/5'}`}>
        
        {/* Macro Radial */}
        {showMacroRadial && (
          <div className="absolute -inset-16 flex items-center justify-center pointer-events-none animate-in fade-in zoom-in duration-300">
            {[0, 90, 180, 270].map((deg, i) => (
              <div 
                key={i} 
                style={{ transform: `rotate(${deg}deg) translateY(-50px)` }}
                className="absolute w-10 h-10 bg-slate-900 border border-emerald-500/40 rounded-xl flex items-center justify-center shadow-lg"
              >
                <Zap size={14} className="text-emerald-500 rotate-0" style={{ transform: `rotate(${-deg}deg)` }} />
              </div>
            ))}
          </div>
        )}

        <Ghost className={`transition-all duration-500 ${isOpticalLinked ? 'text-emerald-400 scale-125' : 'text-slate-500'}`} size={28} />
        
        {/* State Indicators */}
        <div className="absolute -bottom-10 flex flex-col items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
           <span className="text-[7px] font-black uppercase tracking-[0.3em] text-emerald-500">Scout Shard</span>
           <div className="flex gap-1">
              <div className="w-1 h-1 rounded-full bg-emerald-500 animate-pulse" />
              <div className="w-1 h-1 rounded-full bg-slate-800" />
           </div>
        </div>

        <button 
          onClick={(e) => { e.stopPropagation(); setIsCalibrating(!isCalibrating); }}
          className="absolute -top-2 -left-2 p-1.5 bg-slate-900 rounded-lg border border-white/10 opacity-0 group-hover:opacity-100"
        >
          <Wand2 size={12} className="text-emerald-500" />
        </button>
      </div>
    </div>
  );
};

export default AFiREflyOverlay;
