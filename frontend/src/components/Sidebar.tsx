"use client";

import React, { useState } from "react";
import { Project } from "@/lib/api";
import { 
  Plus, History, CheckCircle2, Loader2, AlertCircle, FileText, 
  ChevronRight, Search, Trash2, X, Sparkles
} from "lucide-react";

interface SidebarProps {
  projects: Project[];
  activeProjectId: string | null;
  onSelectProject: (id: string) => void;
  onNewProject: () => void;
  onDeleteProject?: (id: string) => void;
  isLoading: boolean;
}

export function Sidebar({ 
  projects, 
  activeProjectId, 
  onSelectProject, 
  onNewProject, 
  onDeleteProject,
  isLoading 
}: SidebarProps) {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredProjects = projects.filter((p) =>
    p.idea.toLowerCase().includes(searchQuery.toLowerCase().trim())
  );

  return (
    <aside className="w-80 h-[calc(100vh-4rem)] border-r border-slate-800/80 bg-slate-950/80 backdrop-blur-xl flex flex-col hidden lg:flex shrink-0">
      {/* Header section */}
      <div className="p-4 border-b border-slate-800/60 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-slate-300 font-semibold text-xs uppercase tracking-wider">
            <History className="w-4 h-4 text-indigo-400" />
            <span>Work History ({projects.length})</span>
          </div>
          <button
            onClick={onNewProject}
            title="Create New Startup Idea"
            className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-indigo-600/20 border border-indigo-500/30 text-indigo-300 hover:bg-indigo-600 hover:text-white transition-all text-xs font-semibold"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>New</span>
          </button>
        </div>

        {/* Search input for 100+ projects */}
        <div className="relative">
          <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search 100+ history items..."
            className="w-full pl-8 pr-7 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-200 placeholder-slate-500 text-xs focus:outline-none focus:border-indigo-500 transition-all"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>

      {/* Projects list */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {isLoading && projects.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-8 text-slate-500 gap-2">
            <Loader2 className="w-5 h-5 animate-spin text-indigo-400" />
            <span className="text-xs">Loading history...</span>
          </div>
        ) : filteredProjects.length === 0 ? (
          <div className="p-6 text-center text-slate-500 rounded-xl border border-dashed border-slate-800">
            <FileText className="w-8 h-8 mx-auto mb-2 text-slate-600 stroke-[1.5]" />
            <p className="text-xs font-medium">
              {searchQuery ? `No results for "${searchQuery}"` : "No work history yet."}
            </p>
            <p className="text-[11px] text-slate-600 mt-1">
              {searchQuery ? "Try a different search term." : "Generate a startup blueprint to start building your history."}
            </p>
          </div>
        ) : (
          filteredProjects.map((proj) => {
            const isActive = proj.id === activeProjectId;
            const isCompleted = proj.status === "completed";
            const isRunning = proj.status === "running";

            return (
              <div
                key={proj.id}
                className={`group relative rounded-xl transition-all duration-200 border ${
                  isActive
                    ? "bg-gradient-to-r from-indigo-950/90 to-purple-950/50 border-indigo-500/60 shadow-md shadow-indigo-950/50"
                    : "bg-slate-900/40 border-slate-800/60 hover:bg-slate-900/80 hover:border-slate-700"
                }`}
              >
                <button
                  onClick={() => onSelectProject(proj.id)}
                  className="w-full text-left p-3 pr-8"
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
                </button>

                {/* Delete button on hover */}
                {onDeleteProject && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      if (confirm("Delete this history blueprint?")) {
                        onDeleteProject(proj.id);
                      }
                    }}
                    title="Delete item"
                    className="absolute right-2 top-2 p-1.5 rounded-lg text-slate-500 opacity-0 group-hover:opacity-100 hover:text-rose-400 hover:bg-rose-500/10 transition-all"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
            );
          })
        )}
      </div>
    </aside>
  );
}
