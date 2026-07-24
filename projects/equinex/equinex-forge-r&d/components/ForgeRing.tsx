
import React, { useMemo, useEffect, useState } from 'react';
import { useSecurityMesh } from '../hooks/useSecurityMesh';

interface ForgeRingProps {
  active: boolean;
  scale: number;
  rotation: number;
}

const ForgeRing: React.FC<ForgeRingProps> = ({ active, scale, rotation }) => {
  const [time, setTime] = useState(0);
  const { globalRisk } = useSecurityMesh();

  useEffect(() => {
    let frame = 0;
    const loop = () => {
      // Risk modulates the time-delta (agitation)
      const agitation = 0.02 + (globalRisk / 2000);
      setTime(t => t + agitation);
      frame = requestAnimationFrame(loop);
    };
    loop();
    return () => cancelAnimationFrame(frame);
  }, [globalRisk]);

  const isFractured = scale > 1.4;
  const fractureProgress = Math.pow(Math.max(0, (scale - 1.4) * 1.5), 0.35);

  // Risk-based color mapping
  const baseColor = globalRisk > 50 ? '239, 68, 68' : '16, 185, 129';
  const hubColor = globalRisk > 70 ? '#ef4444' : (globalRisk > 30 ? '#f59e0b' : '#10b981');

  return (
    <div className="relative flex items-center justify-center perspective-[2000px]">
      <div 
        style={{ 
          transform: `scale(${scale}) rotateX(25deg) rotateY(${rotation * 0.1}deg)`,
          transformStyle: 'preserve-3d'
        }}
        className="relative transition-transform duration-[800ms] ease-out"
      >
        
        {/* Refractive Core Shroud */}
        <div 
          className="absolute w-[300px] h-[300px] rounded-full border border-white/5 blur-[2px]"
          style={{ 
            background: `radial-gradient(circle at 30% 30%, rgba(${baseColor}, 0.15) 0%, transparent 70%)`,
            transform: 'translateZ(-50px)' 
          }}
        />

        {/* Spherical Projection Shards */}
        {[...Array(24)].map((_, i) => {
          const phi = Math.acos(-1 + (2 * i) / 24);
          const theta = Math.sqrt(24 * Math.PI) * phi + (time * 0.5);
          
          const radius = isFractured ? 180 + (fractureProgress * 150) : 120;
          const x = radius * Math.sin(phi) * Math.cos(theta);
          const y = radius * Math.sin(phi) * Math.sin(theta);
          const z = radius * Math.cos(phi);

          const glowIntensity = 0.3 + Math.sin(time + i) * 0.2;

          return (
            <div 
              key={`shard-${i}`}
              style={{ 
                transform: `translate3d(${x}px, ${y}px, ${z}px) rotateY(${theta}rad) rotateX(${phi}rad)`,
                opacity: active ? (isFractured ? 0.3 : 0.6) : 0.1,
                filter: isFractured ? `drop-shadow(2px 0 1px rgba(${baseColor},${glowIntensity}))` : 'none'
              }}
              className="absolute w-8 h-20 transition-all duration-700 ease-out"
            >
              <div 
                className="w-full h-full rounded-full"
                style={{
                  background: `linear-gradient(135deg, rgba(${baseColor}, 0.4) 0%, rgba(${baseColor}, 0.05) 100%)`,
                  boxShadow: `
                    inset 0 0 15px rgba(255, 255, 255, 0.1),
                    0 0 20px rgba(${baseColor}, ${glowIntensity * 0.5})
                  `,
                  backdropFilter: 'blur(8px)',
                  border: '1px solid rgba(255, 255, 255, 0.05)'
                }}
              />
            </div>
          );
        })}

        {/* The Central Singularity */}
        <div 
          style={{ 
            transform: 'translateZ(20px)',
            background: `radial-gradient(circle at center, ${hubColor} 0%, #000 100%)`,
            boxShadow: `0 0 80px ${hubColor}66`
          }}
          className={`w-32 h-32 rounded-full border-4 border-white/20 flex items-center justify-center transition-all duration-1000 ${active ? 'scale-110' : 'scale-90 opacity-50'}`}
        >
           <div className={`w-4 h-4 bg-white rounded-full shadow-[0_0_30px_#fff] ${globalRisk > 50 ? 'animate-ping' : 'animate-pulse'}`} />
        </div>
      </div>
    </div>
  );
};

export default ForgeRing;
