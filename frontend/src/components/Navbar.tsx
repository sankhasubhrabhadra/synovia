"use client";

import React from "react";
import { Sparkles, Plus, Cpu, Sliders, ShieldCheck, History } from "lucide-react";

interface NavbarProps {
  onNewProject: () => void;
  onOpenHistory: () => void;
  historyCount: number;
  activeProjectIdea?: string;
  isExecuting?: boolean;
}

export function Navbar({ 
  onNewProject, 
  onOpenHistory,
  historyCount,
  activeProjectIdea, 
  isExecuting 
}: NavbarProps) {
  return (
    <header className="h-16 border-b-4 border-black bg-[#231813] sticky top-0 z-40 px-4 md:px-6 flex items-center justify-between shadow-[0_4px_0px_#000000]">
      {/* Left: Brand Logo & Studio Identity */}
      <div className="flex items-center gap-3 cursor-pointer group" onClick={onNewProject}>
        <div className="w-10 h-10 rounded-none bg-[#f59e0b] border-3 border-black shadow-[3px_3px_0px_#000000] flex items-center justify-center transition-all group-hover:-translate-x-0.5 group-hover:-translate-y-0.5 group-hover:shadow-[5px_5px_0px_#000000]">
          <Sparkles className="w-6 h-6 text-black fill-black" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-black text-xl tracking-tight text-[#fffdfa] uppercase">SYNOVIA</span>
            <span className="px-2 py-0.5 text-[10px] font-black bg-[#f59e0b] text-black border-2 border-black shadow-[2px_2px_0px_#000000] uppercase tracking-wider">
              AI STUDIO v2.0
            </span>
          </div>
          <p className="text-[11px] text-[#d4c4b5] font-bold uppercase tracking-wide hidden md:block">
            Autonomous Startup Intelligence Engine
          </p>
        </div>
      </div>

      {/* Center: System Parameter Badges */}
      <div className="hidden xl:flex items-center gap-2.5 px-4 py-1.5 bg-[#17100c] border-3 border-black shadow-[4px_4px_0px_#000000] text-xs text-[#fffdfa] font-bold">
        <div className="flex items-center gap-1.5 px-2 py-0.5 bg-[#2b1f19] border-2 border-black shadow-[2px_2px_0px_#000000]">
          <Cpu className="w-3.5 h-3.5 text-[#f59e0b]" />
          <span>Engine: <strong className="text-[#f59e0b]">Qwen 2.5 1.5B / Gemini</strong></span>
        </div>
        <span className="text-black font-black">•</span>
        <div className="flex items-center gap-1.5 px-2 py-0.5 bg-[#2b1f19] border-2 border-black shadow-[2px_2px_0px_#000000]">
          <Sliders className="w-3.5 h-3.5 text-purple-400" />
          <span>Agents: <strong className="text-purple-300">8 Swarm</strong></span>
        </div>
        <span className="text-black font-black">•</span>
        <div className="flex items-center gap-1.5 px-2 py-0.5 bg-[#2b1f19] border-2 border-black shadow-[2px_2px_0px_#000000]">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>Pipeline: <strong className="text-emerald-400">Active</strong></span>
        </div>
      </div>

      {/* Execution Indicator */}
      {isExecuting && (
        <div className="flex items-center gap-2 px-3 py-1 bg-[#ea580c] text-white border-2 border-black shadow-[3px_3px_0px_#000000] text-xs font-black uppercase animate-pulse">
          <div className="w-2.5 h-2.5 rounded-none bg-black animate-ping" />
          <span className="truncate max-w-[120px] sm:max-w-xs">
            {activeProjectIdea ? `Running: "${activeProjectIdea}"` : "Executing Swarm..."}
          </span>
        </div>
      )}

      {/* Right: Actions */}
      <div className="flex items-center gap-3">
        {/* Toggle History Button */}
        <button
          onClick={onOpenHistory}
          className="flex items-center gap-2 px-3.5 py-2 text-xs font-black bg-[#2b1f1a] text-[#fffdfa] border-3 border-black shadow-[3px_3px_0px_#000000] hover:-translate-x-0.5 hover:-translate-y-0.5 hover:shadow-[5px_5px_0px_#000000] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none transition-all cursor-pointer uppercase"
        >
          <History className="w-4 h-4 text-[#f59e0b]" />
          <span>History</span>
          <span className="px-2 py-0.2 bg-[#f59e0b] text-black border-2 border-black font-black text-[11px]">
            {historyCount}
          </span>
        </button>

        {/* New Blueprint Button */}
        <button
          onClick={onNewProject}
          className="flex items-center gap-2 px-4 py-2 text-xs font-black bg-[#f59e0b] text-black border-3 border-black shadow-[4px_4px_0px_#000000] hover:bg-[#fbbf24] hover:-translate-x-0.5 hover:-translate-y-0.5 hover:shadow-[6px_6px_0px_#000000] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none transition-all cursor-pointer uppercase"
        >
          <Plus className="w-4 h-4 stroke-[3]" />
          <span className="hidden sm:inline">New Blueprint</span>
        </button>
      </div>
    </header>
  );
}
