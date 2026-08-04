"use client";

import React from "react";
import { Sparkles, Plus, Cpu, Sliders, ShieldCheck } from "lucide-react";

interface NavbarProps {
  onNewProject: () => void;
  activeProjectIdea?: string;
  isExecuting?: boolean;
}

export function Navbar({ 
  onNewProject, 
  activeProjectIdea, 
  isExecuting 
}: NavbarProps) {
  return (
    <header className="h-16 border-b border-slate-800/80 bg-[#0d121f]/90 backdrop-blur-xl sticky top-0 z-40 px-4 md:px-6 flex items-center justify-between">
      {/* Left: Brand Logo & Studio Identity */}
      <div className="flex items-center gap-3 cursor-pointer" onClick={onNewProject}>
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-500 p-[1px] flex items-center justify-center shadow-lg shadow-blue-500/20">
          <div className="w-full h-full bg-[#090d16] rounded-[11px] flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-blue-400" />
          </div>
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-black text-lg tracking-tight text-white">SYNOVIA</span>
            <span className="px-2 py-0.5 text-[10px] font-black rounded-md bg-blue-500/10 text-blue-400 border border-blue-500/30 uppercase tracking-wider">
              AI STUDIO v2.0
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-medium hidden md:block">
            Autonomous Startup Intelligence & Classification Engine
          </p>
        </div>
      </div>

      {/* Center: System Parameter Badges */}
      <div className="hidden xl:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 font-medium">
        <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-slate-800/60 text-slate-300">
          <Cpu className="w-3.5 h-3.5 text-blue-400" />
          <span>Engine: <strong className="text-white">Qwen 2.5 1.5B / Gemini</strong></span>
        </div>
        <span className="text-slate-600">•</span>
        <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-slate-800/60 text-slate-300">
          <Sliders className="w-3.5 h-3.5 text-purple-400" />
          <span>Agents: <strong className="text-white">8 Swarm</strong></span>
        </div>
        <span className="text-slate-600">•</span>
        <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-slate-800/60 text-slate-300">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>Pipeline: <strong className="text-emerald-400">Active</strong></span>
        </div>
      </div>

      {/* Execution Indicator */}
      {isExecuting && (
        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-semibold animate-pulse">
          <div className="w-2 h-2 rounded-full bg-blue-400 animate-ping" />
          <span className="truncate max-w-[120px] sm:max-w-xs">
            {activeProjectIdea ? `Running: "${activeProjectIdea}"` : "Executing..."}
          </span>
        </div>
      )}

      {/* Right: Actions */}
      <div className="flex items-center gap-2">
        <button
          onClick={onNewProject}
          className="flex items-center gap-2 px-3.5 py-2 text-xs font-bold rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white shadow-lg shadow-blue-500/20 transition-all hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span className="hidden sm:inline">New Blueprint</span>
        </button>
      </div>
    </header>
  );
}
