"use client";

import React, { useState, useEffect } from "react";
import { createProject, listProjects, getProject, deleteProject, Project } from "@/lib/api";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { LandingHero } from "@/components/LandingHero";
import { ExecutionScreen } from "@/components/ExecutionScreen";
import { BlueprintView } from "@/components/BlueprintView";

export function SynoviaApp() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [activeProject, setActiveProject] = useState<Project | null>(null);
  const [viewState, setViewState] = useState<"landing" | "executing" | "blueprint">("landing");
  const [isLoadingHistory, setIsLoadingHistory] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  // Load 100+ project history items on mount
  const fetchHistory = async () => {
    try {
      setIsLoadingHistory(true);
      const data = await listProjects(200);
      setProjects(data);
    } catch (err) {
      console.error("Failed to load project history:", err);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  // Handle new idea submission
  const handleCreateProject = async (idea: string, targetMarket?: string) => {
    try {
      setIsSubmitting(true);
      const newProj = await createProject(idea, targetMarket);
      setActiveProject(newProj);
      setViewState("executing");
      fetchHistory();
    } catch (err: any) {
      console.error("Failed to start project execution:", err);
      alert(`Failed to connect to backend: ${err.message || "Please check your network connection"}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle selecting a project from history sidebar
  const handleSelectProject = async (id: string) => {
    try {
      const proj = await getProject(id);
      setActiveProject(proj);
      if (proj.status === "completed" && proj.blueprint) {
        setViewState("blueprint");
      } else {
        setViewState("executing");
      }
    } catch (err) {
      console.error("Failed to fetch project details:", err);
    }
  };

  // Handle deleting a single project
  const handleDeleteProject = async (id: string) => {
    try {
      await deleteProject(id);
      if (activeProject?.id === id) {
        setActiveProject(null);
        setViewState("landing");
      }
      fetchHistory();
    } catch (err) {
      console.error("Failed to delete project:", err);
    }
  };

  // Handle resetting back to landing screen
  const handleNewProject = () => {
    setActiveProject(null);
    setViewState("landing");
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500 selection:text-white relative overflow-x-hidden flex flex-col">
      {/* Background Ambient Glow Effects */}
      <div className="fixed top-0 left-1/4 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none -z-10" />
      <div className="fixed bottom-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl pointer-events-none -z-10" />
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-cyan-600/5 rounded-full blur-3xl pointer-events-none -z-10" />

      {/* Persistent Navbar Header */}
      <Navbar
        onNewProject={handleNewProject}
        activeProjectIdea={activeProject?.idea}
        isExecuting={viewState === "executing"}
      />

      {/* Main Content Area */}
      <div className="flex flex-1 relative">
        {/* Left Project History Drawer */}
        <Sidebar
          projects={projects}
          activeProjectId={activeProject?.id || null}
          onSelectProject={handleSelectProject}
          onNewProject={handleNewProject}
          onDeleteProject={handleDeleteProject}
          isLoading={isLoadingHistory}
        />

        {/* Dynamic View States */}
        <main className="flex-1 flex flex-col min-w-0 transition-all duration-300">
          {viewState === "landing" && (
            <LandingHero
              onSubmitIdea={handleCreateProject}
              isSubmitting={isSubmitting}
            />
          )}

          {viewState === "executing" && activeProject && (
            <ExecutionScreen
              project={activeProject}
              onExecutionComplete={async () => {
                const updated = await getProject(activeProject.id);
                setActiveProject(updated);
                setViewState("blueprint");
                fetchHistory();
              }}
            />
          )}

          {viewState === "blueprint" && activeProject && (
            <BlueprintView project={activeProject} />
          )}
        </main>
      </div>
    </div>
  );
}
