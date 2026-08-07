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
    <header className="h-16 border-b border-[#e8ded2]/15 bg-[#1b1310]/90 backdrop-blur-xl sticky top-0 z-40 px-4 md:px-6 flex items-center justify-between shadow-lg">
      {/* Left: Brand Logo & Studio Identity */}
      <div className="flex items-center gap-3 cursor-pointer" onClick={onNewProject}>
        <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-600 via-rose-500 to-indigo-500 p-[1.5px] flex items-center justify-center shadow-lg shadow-amber-950/40">
          <div className="w-full h-full bg-[#18110e] rounded-[14px] flex items-center justify-center border border-[#e8ded2]/20">
            <Sparkles className="w-5 h-5 text-[#fefae0]" />
          </div>
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-black text-lg tracking-tight text-[#fffdfa]">SYNOVIA</span>
            <span className="px-2 py-0.5 text-[10px] font-black rounded-md bg-[#d97706]/20 text-[#fef3c7] border border-[#f59e0b]/40 uppercase tracking-wider">
              AI STUDIO v2.0
            </span>
          </div>
          <p className="text-[11px] text-[#d4c4b5] font-medium hidden md:block">
            Autonomous Startup Intelligence Engine
          </p>
        </div>
      </div>

      {/* Center: System Parameter Badges */}
      <div className="hidden xl:flex items-center gap-2 px-3.5 py-1.5 rounded-2xl bg-[#261c17]/90 border border-[#e8ded2]/15 text-xs text-[#eae0d5] font-medium shadow-sm">
        <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-lg bg-[#33251f] text-[#fefae0]">
          <Cpu className="w-3.5 h-3.5 text-[#f59e0b]" />
          <span>Engine: <strong className="text-white">Qwen 2.5 1.5B / Gemini</strong></span>
        </div>
        <span className="text-[#a39284]">•</span>
        <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-lg bg-[#33251f] text-[#fefae0]">
          <Sliders className="w-3.5 h-3.5 text-purple-400" />
          <span>Agents: <strong className="text-white">8 Swarm</strong></span>
        </div>
        <span className="text-[#a39284]">•</span>
        <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-lg bg-[#33251f] text-[#fefae0]">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>Pipeline: <strong className="text-emerald-400">Active</strong></span>
        </div>
      </div>

      {/* Execution Indicator */}
      {isExecuting && (
        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-[#d97706]/20 border border-[#f59e0b]/40 text-[#fef3c7] text-xs font-semibold animate-pulse">
          <div className="w-2 h-2 rounded-full bg-[#f59e0b] animate-ping" />
          <span className="truncate max-w-[120px] sm:max-w-xs">
            {activeProjectIdea ? `Running: "${activeProjectIdea}"` : "Executing Swarm..."}
          </span>
        </div>
      )}

      {/* Right: Actions (History Button & New Blueprint Button) */}
      <div className="flex items-center gap-2.5">
        {/* Toggle History Button */}
        <button
          onClick={onOpenHistory}
          className="flex items-center gap-2 px-3.5 py-2 text-xs font-bold rounded-xl bg-[#2b1f1a] hover:bg-[#3d2c25] text-[#fefae0] border border-[#e8ded2]/20 shadow-md transition-all cursor-pointer hover:border-[#f59e0b]/50"
        >
          <History className="w-4 h-4 text-[#f59e0b]" />
          <span>History</span>
          <span className="px-1.5 py-0.2 rounded-md bg-[#d97706]/30 text-[#fef3c7] text-[10px] font-black">
            {historyCount}
          </span>
        </button>

        {/* New Blueprint Button */}
        <button
          onClick={onNewProject}
          className="flex items-center gap-2 px-4 py-2 text-xs font-bold rounded-xl bg-gradient-to-r from-amber-600 via-amber-700 to-rose-700 hover:from-amber-500 hover:to-rose-600 text-white shadow-lg shadow-amber-950/40 transition-all hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span className="hidden sm:inline">New Blueprint</span>
        </button>
      </div>
    </header>
  );
}
