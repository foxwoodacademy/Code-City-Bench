
import React from 'react';

const ARKeyboard: React.FC<{ active: boolean }> = ({ active }) => {
  const keys = [
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M']
  ];

  return (
    <div className={`etched-glass p-10 rounded-[4rem] border-white/5 backdrop-blur-3xl shadow-2xl transition-all duration-700 ${active ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12 scale-90'}`}>
      <div className="flex items-center gap-4 mb-8">
        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
        <h4 className="text-[10px] font-black uppercase tracking-[0.5em] text-emerald-500/60">Optical Neural Board</h4>
      </div>

      <div className="space-y-3">
        {keys.map((row, i) => (
          <div key={i} className="flex justify-center gap-3">
            {row.map(k => (
              <div 
                key={k} 
                className="w-14 h-14 bg-white/5 border border-white/5 rounded-2xl flex items-center justify-center text-slate-400 font-black text-lg hover:bg-emerald-500 hover:text-slate-950 hover:scale-110 transition-all cursor-pointer"
              >
                {k}
              </div>
            ))}
          </div>
        ))}
        <div className="flex justify-center gap-3 pt-4">
           <div className="h-14 px-10 bg-white/5 border border-white/5 rounded-2xl flex items-center justify-center text-slate-500 font-black text-xs uppercase tracking-widest hover:bg-emerald-500 hover:text-slate-950 transition-all">
             Space Shard
           </div>
        </div>
      </div>
    </div>
  );
};

export default ARKeyboard;
