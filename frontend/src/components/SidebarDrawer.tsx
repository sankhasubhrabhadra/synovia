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
      {/* Backdrop Overlay */}
      <div 
        onClick={onClose}
        className="fixed inset-0 bg-black/75 backdrop-blur-xs transition-opacity animate-fade-in"
      />

      {/* Slide-over Right Drawer Container */}
      <aside className="relative w-full max-w-md h-full bg-[#231813] text-[#fffdfa] border-l-4 border-black shadow-[-10px_0px_0px_rgba(0,0,0,0.5)] flex flex-col z-10 animate-slide-in-right">
        {/* Drawer Header */}
        <div className="p-5 border-b-4 border-black space-y-4 bg-[#1a110d]">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-[#fffdfa] font-black text-sm uppercase tracking-wider">
              <History className="w-5 h-5 text-[#f59e0b]" />
              <span>Project History ({projects.length})</span>
            </div>
            
            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  onNewProject();
                  onClose();
                }}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-[#f59e0b] text-black border-2 border-black font-black text-xs uppercase shadow-[2px_2px_0px_#000000] hover:-translate-x-0.5 hover:-translate-y-0.5 hover:shadow-[4px_4px_0px_#000000] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none transition-all cursor-pointer"
              >
                <Plus className="w-4 h-4 stroke-[3]" />
                <span>New</span>
              </button>

              <button
                onClick={onClose}
                className="p-1.5 bg-[#2b1f19] text-[#fffdfa] border-2 border-black font-black shadow-[2px_2px_0px_#000000] hover:bg-[#ea580c] hover:text-white transition-all cursor-pointer"
              >
                <X className="w-5 h-5 stroke-[3]" />
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
              className="w-full pl-9 pr-8 py-2 bg-[#100a08] border-3 border-black text-[#fffdfa] placeholder-[#a39284] text-xs font-bold focus:outline-none focus:border-[#f59e0b] shadow-[3px_3px_0px_#000000] transition-all"
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
                className={`px-3 py-1 text-xs font-black uppercase transition-all cursor-pointer border-2 border-black ${
                  filterType === tab.id
                    ? "bg-[#f59e0b] text-black shadow-[3px_3px_0px_#000000]"
                    : "bg-[#2b1f19] text-[#d4c4b5] shadow-[2px_2px_0px_#000000] hover:text-[#fffdfa]"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Projects List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3.5 scrollbar-thin">
          {isLoading && projects.length === 0 ? (
            <div className="flex flex-col items-center justify-center p-12 text-[#d4c4b5] gap-3">
              <Loader2 className="w-6 h-6 animate-spin text-[#f59e0b]" />
              <span className="text-xs font-bold uppercase">Loading history from SQLite DB...</span>
            </div>
          ) : filteredProjects.length === 0 ? (
            <div className="p-8 text-center text-[#d4c4b5] border-3 border-black bg-[#1f1612] shadow-[4px_4px_0px_#000000]">
              <FileText className="w-10 h-10 mx-auto mb-3 text-[#a39284]" />
              <p className="text-xs font-black uppercase">
                {searchQuery ? `No matching history for "${searchQuery}"` : "No project history recorded yet."}
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
                  className={`group relative transition-all duration-150 border-3 border-black cursor-pointer ${
                    isActive
                      ? "bg-[#3a2820] shadow-[6px_6px_0px_#f59e0b] translate-x-[-2px] translate-y-[-2px]"
                      : "bg-[#2b1f19] shadow-[4px_4px_0px_#000000] hover:bg-[#362720] hover:shadow-[6px_6px_0px_#000000] hover:translate-x-[-1px] hover:translate-y-[-1px]"
                  }`}
                  onClick={() => {
                    onSelectProject(proj.id);
                    onClose();
                  }}
                >
                  <div className="p-4 pr-10">
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <span className="text-xs font-black text-[#fffdfa] line-clamp-2 leading-snug">
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

                    <div className="flex items-center justify-between text-[11px] text-[#d4c4b5] font-bold">
                      {bizType ? (
                        <span className="px-2 py-0.5 bg-[#f59e0b] text-black border-2 border-black font-black uppercase text-[9px] shadow-[2px_2px_0px_#000000]">
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
                      className="absolute right-3 top-3 p-1.5 bg-[#17100c] text-[#a39284] border-2 border-black opacity-0 group-hover:opacity-100 hover:text-rose-400 hover:bg-rose-950 transition-all cursor-pointer"
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
