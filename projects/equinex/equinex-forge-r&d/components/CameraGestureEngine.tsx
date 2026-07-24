
import React, { useRef, useEffect, useState } from 'react';

const CameraGestureEngine: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isActive, setIsActive] = useState(false);

  // Targets high saturation green/neon sharpie cap colors
  const TARGET_COLOR = { r: 16, g: 185, b: 129 }; 
  const TOLERANCE = 80;

  useEffect(() => {
    if (!isActive) return;

    let animationFrame: number;
    let localStream: MediaStream | null = null;

    navigator.mediaDevices.getUserMedia({ video: { width: 320, height: 240 } })
      .then(s => { 
        localStream = s;
        if (videoRef.current) videoRef.current.srcObject = s; 
      })
      .catch(err => console.error("Optical Link error:", err));

    const processFrame = () => {
      if (!canvasRef.current || !videoRef.current) return;
      const ctx = canvasRef.current.getContext('2d', { willReadFrequently: true });
      if (!ctx) return;

      ctx.drawImage(videoRef.current, 0, 0, 320, 240);
      const frame = ctx.getImageData(0, 0, 320, 240);
      const pixels = frame.data;
      const points: { x: number, y: number }[] = [];

      // Detect up to 2 high-saturation points (Sharpie Caps)
      for (let i = 0; i < pixels.length; i += 16) { 
        const r = pixels[i];
        const g = pixels[i + 1];
        const b = pixels[i + 2];
        const diff = Math.abs(r - TARGET_COLOR.r) + Math.abs(g - TARGET_COLOR.g) + Math.abs(b - TARGET_COLOR.b);
        
        if (diff < TOLERANCE) {
          const x = (i / 4) % 320;
          const y = Math.floor((i / 4) / 320);
          
          // Cluster detection: Ensure points are far enough apart to be distinct caps
          if (points.length === 0 || Math.hypot(x - points[0].x, y - points[0].y) > 60) {
            points.push({ x, y });
          }
        }
        if (points.length >= 2) break;
      }

      if (points.length >= 1) {
        const midX = points.length === 2 ? (points[0].x + points[1].x) / 2 : points[0].x;
        const midY = points.length === 2 ? (points[0].y + points[1].y) / 2 : points[0].y;
        const distance = points.length === 2 ? Math.hypot(points[0].x - points[1].x, points[0].y - points[1].y) : 0;
        
        // Calculate angle between points for rotation
        let angle = 0;
        if (points.length === 2) {
           angle = Math.atan2(points[1].y - points[0].y, points[1].x - points[0].x) * (180 / Math.PI);
        }

        window.dispatchEvent(new CustomEvent('optical_gesture', { 
          detail: { 
            midX, 
            midY, 
            shards: points.length,
            distance,
            angle
          } 
        }));
      }

      animationFrame = requestAnimationFrame(processFrame);
    };

    processFrame();
    return () => {
      cancelAnimationFrame(animationFrame);
      if (localStream) localStream.getTracks().forEach(t => t.stop());
    };
  }, [isActive]);

  return (
    <div className="fixed top-8 left-1/2 -translate-x-1/2 z-[200]">
      <button 
        onClick={() => setIsActive(!isActive)}
        className={`px-8 py-3 rounded-2xl font-black uppercase text-[10px] tracking-widest transition-all ${isActive ? 'bg-emerald-500 text-slate-950 shadow-[0_0_30px_rgba(16,185,129,0.3)]' : 'etched-glass text-slate-500 border-white/5 hover:text-white'}`}
      >
        {isActive ? 'Aperture Active' : 'Calibrate Aperture'}
      </button>

      {isActive && (
        <div className="absolute top-16 left-1/2 -translate-x-1/2 w-48 h-36 etched-glass rounded-2xl overflow-hidden border border-emerald-500/20 group">
          <video ref={videoRef} autoPlay playsInline className="w-full h-full object-cover grayscale opacity-20 group-hover:opacity-40 transition-opacity" />
          <canvas ref={canvasRef} width={320} height={240} className="hidden" />
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="w-10 h-10 border border-emerald-500/20 rounded-full animate-ping" />
          </div>
        </div>
      )}
    </div>
  );
};

export default CameraGestureEngine;
