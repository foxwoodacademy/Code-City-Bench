
import React, { useState, useEffect, useRef } from 'react';
import ForgeRing from './ForgeRing';
import ARKeyboard from './ARKeyboard';
import TopographicalMesh from './TopographicalMesh';
import { resonance } from '../services/audio';

interface RDWorkspaceProps {
  gestureData: any;
}

const RDWorkspace: React.FC<RDWorkspaceProps> = ({ gestureData }) => {
  const [scale, setScale] = useState(1);
  const [rotation, setRotation] = useState(0);
  const [manualInteraction, setManualInteraction] = useState(false);
  const [isGesturing, setIsGesturing] = useState(false);
  
  const interactionRef = useRef({
    isDown: false,
    startX: 0,
    startRotation: 0,
    startDistance: 0,
    startScale: 1
  });

  const lastStateRef = useRef({ fractured: false });

  const handleStart = (clientX: number, distance: number = 0) => {
    interactionRef.current.isDown = true;
    interactionRef.current.startX = clientX;
    interactionRef.current.startRotation = rotation;
    interactionRef.current.startDistance = distance;
    interactionRef.current.startScale = scale;
    setManualInteraction(true);
    setIsGesturing(true);
  };

  const handleMove = (clientX: number, distance: number = 0) => {
    if (!interactionRef.current.isDown) return;

    const deltaX = clientX - interactionRef.current.startX;
    setRotation(interactionRef.current.startRotation + deltaX * 0.4);

    if (distance > 0 && interactionRef.current.startDistance > 0) {
      const ratio = distance / interactionRef.current.startDistance;
      const targetScale = Math.max(0.6, Math.min(4, interactionRef.current.startScale * ratio));
      setScale(targetScale);
    }
  };

  const handleEnd = () => {
    interactionRef.current.isDown = false;
    setIsGesturing(false);
  };

  // Sync with Optical Engine
  useEffect(() => {
    if (gestureData && gestureData.shards === 2 && !manualInteraction) {
      const dist = gestureData.distance;
      const targetScale = Math.max(0.6, Math.min(4, dist / 80));
      setScale(prev => prev + (targetScale - prev) * 0.15);
      if (gestureData.angle) setRotation(gestureData.angle);
    }
  }, [gestureData, manualInteraction]);

  // Swell Audio logic
  useEffect(() => {
    const isFractured = scale > 1.4;
    if (isFractured !== lastStateRef.current.fractured) {
      isFractured ? resonance.playPluck(1200, 0.2) : resonance.playSwell(220, 0.3);
      lastStateRef.current.fractured = isFractured;
    }
  }, [scale]);

  return (
    <div 
      className="relative w-screen h-screen flex items-center justify-center overflow-hidden perspective-[2500px] touch-none select-none bg-slate-950"
      onMouseDown={(e) => handleStart(e.clientX)}
      onMouseMove={(e) => handleMove(e.clientX)}
      onMouseUp={handleEnd}
      onMouseLeave={handleEnd}
      onTouchStart={(e) => {
        const t1 = e.touches[0];
        const t2 = e.touches[1];
        if (t2) {
          const d = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
          handleStart(t1.clientX, d);
        } else {
          handleStart(t1.clientX);
        }
      }}
      onTouchMove={(e) => {
        const t1 = e.touches[0];
        const t2 = e.touches[1];
        if (t2) {
          const d = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
          handleMove(t1.clientX, d);
        } else {
          handleMove(t1.clientX);
        }
      }}
      onTouchEnd={handleEnd}
      onWheel={(e) => {
        setManualInteraction(true);
        const delta = e.deltaY * -0.004;
        setScale(s => Math.max(0.6, Math.min(4, s + delta)));
      }}
    >
      <TopographicalMesh scale={scale} rotation={rotation} />

      <div 
        style={{ 
          transform: `translateZ(${isGesturing ? '100px' : '0px'}) scale(${isGesturing ? 1.05 : 1})`,
          transformStyle: 'preserve-3d'
        }}
        className="z-10 transition-all duration-700 pointer-events-none"
      >
        <ForgeRing 
          active={true} 
          scale={scale} 
          rotation={rotation}
        />
      </div>
      
      {scale < 2 && (
        <div 
          className="fixed bottom-32 left-1/2 -translate-x-1/2 px-8 py-4 etched-glass rounded-full border border-emerald-500/20 text-[10px] font-black uppercase tracking-[0.4em] text-emerald-400 animate-pulse pointer-events-none z-50">
          Interaction Mode: Tactile Aperture
        </div>
      )}

      {/* Mobile-specific depth indicators */}
      <div className="fixed bottom-12 right-12 flex flex-col items-end gap-1 opacity-40">
        <div className="h-48 w-1 bg-white/5 rounded-full relative overflow-hidden">
          <div 
            className="absolute bottom-0 w-full bg-emerald-500 transition-all duration-300" 
            style={{ height: `${(scale / 4) * 100}%` }} 
          />
        </div>
        <span className="text-[8px] font-black uppercase text-slate-600 mt-2">Scale_Z</span>
      </div>
    </div>
  );
};

export default RDWorkspace;
