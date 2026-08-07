"use client";

import React, { useState } from "react";
import { Project } from "@/lib/api";
import { 
  Plus, History, CheckCircle2, Loader2, AlertCircle, FileText, 
  Search, Trash2, X, Sparkles, Layers, ArrowRight
} from "lucide-react";

interface SidebarDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  projects: Project[];
  activeProjectId: string | null;
  onSelectProject: (id: string) => void;
  onNewProject: () => void;
  onDeleteProject?: (id: string) => void;
  isLoading: boolean;
}

export function SidebarDrawer({
  isOpen,
  onClose,
  projects,
  activeProjectId,
  onSelectProject,
  onNewProject,
  onDeleteProject,
  isLoading
}: SidebarDrawerProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState<"all" | "completed" | "running">("all");

  if (!isOpen) return null;

  const filteredProjects = projects.filter((p) => {
    const matchesSearch = p.idea.toLowerCase().includes(searchQuery.toLowerCase().trim());
    if (filterType === "completed") return matchesSearch && p.status === "completed";
    if (filterType === "running") return matchesSearch && p.status === "running";
    return matchesSearch;
  });

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Blurred Backdrop Overlay */}
      <div 
        onClick={onClose}
        className="fixed inset-0 bg-black/65 backdrop-blur-md transition-opacity animate-fade-in"
      />

      {/* Slide-over Right Drawer Container */}
      <aside className="relative w-full max-w-md h-full bg-[#1c1411]/95 text-[#fffdfa] border-l border-[#e8ded2]/20 backdrop-blur-2xl shadow-2xl flex flex-col z-10 animate-slide-in-right">
        {/* Drawer Header */}
        <div className="p-5 border-b border-[#e8ded2]/15 space-y-4 bg-[#261c17]/80">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-[#fefae0] font-black text-sm uppercase tracking-wider">
              <History className="w-5 h-5 text-[#f59e0b]" />
              <span>Project History ({projects.length})</span>
            </div>
            
            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  onNewProject();
                  onClose();
                }}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#d97706]/20 border border-[#f59e0b]/40 text-[#fef3c7] hover:bg-[#d97706] hover:text-white transition-all text-xs font-bold cursor-pointer"
              >
                <Plus className="w-4 h-4" />
                <span>New</span>
              </button>

              <button
                onClick={onClose}
                className="p-1.5 rounded-xl bg-[#33251e] text-[#d4c4b5] hover:text-white hover:bg-[#443228] transition-all cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Search Bar */}
          <div className="relative">
            <Search className="w-4 h-4 text-[#d4c4b5] absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search past blueprints & ideas..."
              className="w-full pl-9 pr-8 py-2 rounded-xl bg-[#120c0a] border border-[#e8ded2]/20 text-[#fffdfa] placeholder-[#a39284] text-xs focus:outline-none focus:border-[#f59e0b] transition-all"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery("")}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#a39284] hover:text-[#fffdfa]"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-2">
            {[
              { id: "all", label: "All Runs" },
              { id: "completed", label: "Completed" },
              { id: "running", label: "Active Swarm" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setFilterType(tab.id as any)}
                className={`px-3 py-1 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                  filterType === tab.id
                    ? "bg-[#d97706]/30 text-[#fefae0] border border-[#f59e0b]/50 shadow-md shadow-amber-900/30"
                    : "bg-[#1f1613] text-[#d4c4b5] border border-[#e8ded2]/10 hover:text-[#fffdfa]"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Projects List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3 scrollbar-thin">
          {isLoading && projects.length === 0 ? (
            <div className="flex flex-col items-center justify-center p-12 text-[#d4c4b5] gap-3">
              <Loader2 className="w-6 h-6 animate-spin text-[#f59e0b]" />
              <span className="text-xs font-medium">Loading history from SQLite DB...</span>
            </div>
          ) : filteredProjects.length === 0 ? (
            <div className="p-8 text-center text-[#d4c4b5] rounded-2xl border border-dashed border-[#e8ded2]/20 bg-[#241a15]/50">
              <FileText className="w-10 h-10 mx-auto mb-3 text-[#a39284]" />
              <p className="text-xs font-semibold">
                {searchQuery ? `No matching history found for "${searchQuery}"` : "No project history recorded yet."}
              </p>
            </div>
          ) : (
            filteredProjects.map((proj) => {
              const isActive = proj.id === activeProjectId;
              const isCompleted = proj.status === "completed";
              const isRunning = proj.status === "running";
              
              const classification = proj.blueprint?.classification || {};
              const bizType = classification.business_type ? classification.business_type.replace("_", " ").toUpperCase() : null;

              return (
                <div
                  key={proj.id}
                  className={`group relative rounded-2xl transition-all duration-200 border cursor-pointer ${
                    isActive
                      ? "bg-gradient-to-r from-[#3a2820] to-[#2d1e18] border-[#f59e0b] shadow-xl shadow-amber-950/50"
                      : "bg-[#251b17]/80 border-[#e8ded2]/15 hover:bg-[#33241e] hover:border-[#f59e0b]/40"
                  }`}
                  onClick={() => {
                    onSelectProject(proj.id);
                    onClose();
                  }}
                >
                  <div className="p-4 pr-10">
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <span className="text-xs font-bold text-[#fffdfa] line-clamp-2 leading-snug group-hover:text-[#fefae0]">
                        {proj.idea}
                      </span>
                      {isCompleted ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      ) : isRunning ? (
                        <Loader2 className="w-4 h-4 text-amber-400 animate-spin shrink-0 mt-0.5" />
                      ) : (
                        <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                      )}
                    </div>

                    <div className="flex items-center justify-between text-[11px] text-[#d4c4b5] font-medium">
                      {bizType ? (
                        <span className="px-2 py-0.5 rounded-md bg-[#d97706]/20 text-[#fef3c7] border border-[#f59e0b]/30 font-extrabold uppercase text-[9px]">
                          {bizType}
                        </span>
                      ) : (
                        <span>{isCompleted ? "Blueprint Ready" : isRunning ? "Swarm Executing" : "Draft"}</span>
                      )}
                      <span>{new Date(proj.created_at).toLocaleDateString(undefined, { month: "short", day: "numeric" })}</span>
                    </div>
                  </div>

                  {/* Delete Option */}
                  {onDeleteProject && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        if (confirm("Permanently delete this project from history?")) {
                          onDeleteProject(proj.id);
                        }
                      }}
                      title="Delete item"
                      className="absolute right-3 top-3 p-1.5 rounded-lg text-[#a39284] opacity-0 group-hover:opacity-100 hover:text-rose-400 hover:bg-rose-500/20 transition-all cursor-pointer"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              );
            })
          )}
        </div>
      </aside>
    </div>
  );
}
