"use client";

import React from "react";
import { Sparkles, Plus, Rocket, Terminal, Layers } from "lucide-react";

interface NavbarProps {
  onNewProject: () => void;
  activeProjectIdea?: string;
  isExecuting?: boolean;
}

export function Navbar({ onNewProject, activeProjectIdea, isExecuting }: NavbarProps) {
  return (
    <header className="h-16 border-b border-slate-800/80 glass-panel sticky top-0 z-40 px-4 md:px-8 flex items-center justify-between">
      {/* Brand Logo */}
      <div className="flex items-center gap-3 cursor-pointer" onClick={onNewProject}>
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-cyan-400 p-[1px] flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <div className="w-full h-full bg-slate-950 rounded-[11px] flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-indigo-400" />
          </div>
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-lg tracking-tight text-white">SYNOVIA</span>
            <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase tracking-widest">
              AI Co-Founder
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-medium hidden sm:block">Autonomous Multi-Agent Startup Synthesizer</p>
        </div>
      </div>

      {/* Center status banner if actively generating */}
      {isExecuting && (
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-950/60 border border-indigo-500/30 animate-pulse">
          <div className="w-2 h-2 rounded-full bg-indigo-400 animate-ping" />
          <span className="text-xs font-semibold text-indigo-300">
            Agents Operating: {activeProjectIdea ? `"${activeProjectIdea.slice(0, 30)}..."` : "Processing..."}
          </span>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-3">
        <button
          onClick={onNewProject}
          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white shadow-md shadow-indigo-600/20 transition-all hover:scale-[1.02] active:scale-[0.98]"
        >
          <Plus className="w-4 h-4" />
          <span>New Blueprint</span>
        </button>
      </div>
    </header>
  );
}
