"use client";

import React, { useState } from "react";
import { Project } from "@/lib/api";
import { 
  Plus, History, CheckCircle2, Loader2, AlertCircle, FileText, 
  Search, Trash2, X, Sparkles, Layers, Tag
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
  const [filterType, setFilterType] = useState<"all" | "completed" | "running">("all");

  const filteredProjects = projects.filter((p) => {
    const matchesSearch = p.idea.toLowerCase().includes(searchQuery.toLowerCase().trim());
    if (filterType === "completed") return matchesSearch && p.status === "completed";
    if (filterType === "running") return matchesSearch && p.status === "running";
    return matchesSearch;
  });

  return (
    <aside className="w-80 h-[calc(100vh-4rem)] border-r border-slate-800/80 bg-[#0d121f]/95 backdrop-blur-xl flex flex-col hidden lg:flex shrink-0">
      {/* Studio Drawer Header */}
      <div className="p-4 border-b border-slate-800/80 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-slate-300 font-bold text-xs uppercase tracking-wider">
            <History className="w-4 h-4 text-blue-400" />
            <span>Studio History ({projects.length})</span>
          </div>
          <button
            onClick={onNewProject}
            title="Create New Studio Run"
            className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-blue-600/20 border border-blue-500/30 text-blue-300 hover:bg-blue-600 hover:text-white transition-all text-xs font-bold cursor-pointer"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>New</span>
          </button>
        </div>

        {/* Search Input */}
        <div className="relative">
          <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search history..."
            className="w-full pl-8 pr-7 py-1.5 rounded-xl bg-slate-950/90 border border-slate-800 text-slate-200 placeholder-slate-500 text-xs focus:outline-none focus:border-blue-500 transition-all"
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

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 pt-1">
          {[
            { id: "all", label: "All" },
            { id: "completed", label: "Ready" },
            { id: "running", label: "Active" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setFilterType(tab.id as any)}
              className={`px-2.5 py-1 rounded-lg text-[10px] font-bold transition-all cursor-pointer ${
                filterType === tab.id
                  ? "bg-blue-600/30 text-blue-300 border border-blue-500/40"
                  : "bg-slate-900/60 text-slate-400 border border-slate-800 hover:text-slate-200"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Projects List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {isLoading && projects.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-8 text-slate-500 gap-2">
            <Loader2 className="w-5 h-5 animate-spin text-blue-400" />
            <span className="text-xs">Loading studio history...</span>
          </div>
        ) : filteredProjects.length === 0 ? (
          <div className="p-6 text-center text-slate-500 rounded-2xl border border-dashed border-slate-800">
            <FileText className="w-8 h-8 mx-auto mb-2 text-slate-600 stroke-[1.5]" />
            <p className="text-xs font-medium">
              {searchQuery ? `No results for "${searchQuery}"` : "No studio history yet."}
            </p>
          </div>
        ) : (
          filteredProjects.map((proj) => {
            const isActive = proj.id === activeProjectId;
            const isCompleted = proj.status === "completed";
            const isRunning = proj.status === "running";
            
            // Extract business category if blueprint classification exists
            const classification = proj.blueprint?.classification || {};
            const bizType = classification.business_type ? classification.business_type.replace("_", " ").toUpperCase() : null;

            return (
              <div
                key={proj.id}
                className={`group relative rounded-xl transition-all duration-200 border ${
                  isActive
                    ? "bg-gradient-to-r from-blue-950/80 via-slate-900 to-indigo-950/60 border-blue-500/60 shadow-lg shadow-blue-950/40"
                    : "bg-slate-900/40 border-slate-800/60 hover:bg-slate-900/80 hover:border-slate-700"
                }`}
              >
                <button
                  onClick={() => onSelectProject(proj.id)}
                  className="w-full text-left p-3 pr-8"
                >
                  <div className="flex items-start justify-between gap-2 mb-1.5">
                    <span className="text-xs font-bold text-slate-200 line-clamp-2 leading-snug group-hover:text-white">
                      {proj.idea}
                    </span>
                    {isCompleted ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    ) : isRunning ? (
                      <Loader2 className="w-4 h-4 text-blue-400 animate-spin shrink-0 mt-0.5" />
                    ) : (
                      <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                    )}
                  </div>

                  <div className="flex items-center justify-between text-[10px] text-slate-400 font-medium">
                    {bizType ? (
                      <span className="px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 font-bold">
                        {bizType}
                      </span>
                    ) : (
                      <span>{isCompleted ? "Blueprint Ready" : isRunning ? "Agents Active" : "Draft"}</span>
                    )}
                    <span>{new Date(proj.created_at).toLocaleDateString(undefined, { month: "short", day: "numeric" })}</span>
                  </div>
                </button>

                {/* Delete button on hover */}
                {onDeleteProject && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      if (confirm("Delete this history item?")) {
                        onDeleteProject(proj.id);
                      }
                    }}
                    title="Delete item"
                    className="absolute right-2 top-2 p-1.5 rounded-lg text-slate-500 opacity-0 group-hover:opacity-100 hover:text-rose-400 hover:bg-rose-500/10 transition-all cursor-pointer"
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
