"use client";

import React from "react";
import { Project } from "@/lib/api";
import { Plus, History, CheckCircle2, Loader2, AlertCircle, FileText, ChevronRight } from "lucide-react";

interface SidebarProps {
  projects: Project[];
  activeProjectId: string | null;
  onSelectProject: (id: string) => void;
  onNewProject: () => void;
  isLoading: boolean;
}

export function Sidebar({ projects, activeProjectId, onSelectProject, onNewProject, isLoading }: SidebarProps) {
  return (
    <aside className="w-80 h-[calc(100vh-4rem)] border-r border-slate-800/80 bg-slate-950/60 backdrop-blur-xl flex flex-col hidden lg:flex">
      {/* Header section */}
      <div className="p-4 border-b border-slate-800/60 flex items-center justify-between">
        <div className="flex items-center gap-2 text-slate-300 font-semibold text-xs uppercase tracking-wider">
          <History className="w-4 h-4 text-indigo-400" />
          <span>Project History ({projects.length})</span>
        </div>
        <button
          onClick={onNewProject}
          title="Create New Startup Idea"
          className="p-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-indigo-500/40 transition-colors"
        >
          <Plus className="w-4 h-4" />
        </button>
      </div>

      {/* Projects list */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {isLoading && projects.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-8 text-slate-500 gap-2">
            <Loader2 className="w-5 h-5 animate-spin text-indigo-400" />
            <span className="text-xs">Loading history...</span>
          </div>
        ) : projects.length === 0 ? (
          <div className="p-6 text-center text-slate-500 rounded-xl border border-dashed border-slate-800">
            <FileText className="w-8 h-8 mx-auto mb-2 text-slate-600 stroke-[1.5]" />
            <p className="text-xs font-medium">No blueprints created yet.</p>
            <p className="text-[11px] text-slate-600 mt-1">Enter a startup idea to trigger your autonomous agents.</p>
          </div>
        ) : (
          projects.map((proj) => {
            const isActive = proj.id === activeProjectId;
            const isCompleted = proj.status === "completed";
            const isRunning = proj.status === "running";

            return (
              <button
                key={proj.id}
                onClick={() => onSelectProject(proj.id)}
                className={`w-full text-left p-3 rounded-xl transition-all duration-200 group relative border ${
                  isActive
                    ? "bg-gradient-to-r from-indigo-950/80 to-purple-950/40 border-indigo-500/50 shadow-md shadow-indigo-950/50"
                    : "bg-slate-900/40 border-slate-800/60 hover:bg-slate-900/80 hover:border-slate-700"
                }`}
              >
                <div className="flex items-start justify-between gap-2 mb-1.5">
                  <span className="text-xs font-semibold text-slate-200 line-clamp-2 leading-snug group-hover:text-white">
                    {proj.idea}
                  </span>
                  {isCompleted ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  ) : isRunning ? (
                    <Loader2 className="w-4 h-4 text-indigo-400 animate-spin shrink-0 mt-0.5" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                  )}
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-500 font-medium">
                  <span className="capitalize">{isCompleted ? "Blueprint Ready" : isRunning ? "Agents Active" : "Draft"}</span>
                  <span>{new Date(proj.created_at).toLocaleDateString(undefined, { month: "short", day: "numeric" })}</span>
                </div>

                {isActive && (
                  <div className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <ChevronRight className="w-4 h-4 text-indigo-400" />
                  </div>
                )}
              </button>
            );
          })
        )}
      </div>
    </aside>
  );
}
