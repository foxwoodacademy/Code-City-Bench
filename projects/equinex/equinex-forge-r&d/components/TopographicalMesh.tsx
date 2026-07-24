
import React from 'react';

interface TopographicalMeshProps {
  scale: number;
  rotation: number;
}

const TopographicalMesh: React.FC<TopographicalMeshProps> = ({ scale, rotation }) => {
  const depth = Math.max(0, (scale - 1) * 400);
  
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden bg-[#01030d]">
      <div 
        style={{ 
          transform: `rotateX(65deg) rotateZ(${rotation * 0.05}deg) translateZ(${-800 + depth}px)`,
          transformStyle: 'preserve-3d'
        }}
        className="absolute inset-[-150%] transition-transform duration-[1000ms] ease-out"
      >
        {/* Glow Foundation */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(16,185,129,0.15),transparent_70%)]" />

        {/* The Grid: 3D Refractive Lines */}
        <div 
          className="absolute inset-0 bg-[linear-gradient(rgba(16,185,129,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(16,185,129,0.1)_1px,transparent_1px)] bg-[size:80px_80px]"
          style={{ 
            maskImage: 'radial-gradient(circle at center, black 10%, transparent 90%)',
            boxShadow: 'inset 0 0 100px rgba(16,185,129,0.05)'
          }}
        >
          {/* Subtle Secondary Detail Grid */}
          <div className="absolute inset-0 bg-[linear-gradient(rgba(16,185,129,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(16,185,129,0.02)_1px,transparent_1px)] bg-[size:20px_20px]" />
        </div>

        {/* Lexeme Data Spikes */}
        {[...Array(20)].map((_, i) => {
          const x = (i * 37) % 100;
          const y = (i * 13) % 100;
          const h = 50 + (i * 15) + (scale * 20);
          
          return (
            <div 
              key={i}
              style={{ 
                left: `${x}%`, 
                top: `${y}%`,
                height: `${h}px`,
                transform: `translateZ(0) rotateX(-90deg)`,
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                boxShadow: `0 0 40px rgba(16, 185, 129, 0.2)`
              }}
              className="absolute w-1 border-t-2 border-emerald-400 opacity-30"
            />
          );
        })}

        {/* Refractive Depth Fog */}
        <div 
          className="absolute inset-0 bg-gradient-to-t from-[#01030d] via-transparent to-transparent opacity-90"
          style={{ transform: 'translateZ(500px) rotateX(-65deg)' }}
        />
      </div>
    </div>
  );
};

export default TopographicalMesh;
