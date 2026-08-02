"use client";

import React, { useState, useEffect } from "react";
import { createProject, listProjects, getProject, deleteProject, Project } from "@/lib/api";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { LandingHero } from "@/components/LandingHero";
import { ExecutionScreen } from "@/components/ExecutionScreen";
import { BlueprintView } from "@/components/BlueprintView";

export default function Home() {
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
    } catch (err) {
      console.error("Failed to start project execution:", err);
      alert("Failed to connect to backend server. Please try again in a moment.");
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

  // Handle deleting a single history item
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

  // Reset to landing view
  const handleNewProjectClick = () => {
    setActiveProject(null);
    setViewState("landing");
  };

  // Callback when execution completes
  const handleExecutionComplete = async () => {
    if (activeProject) {
      try {
        const updated = await getProject(activeProject.id);
        setActiveProject(updated);
        setViewState("blueprint");
        fetchHistory();
      } catch (err) {
        console.error("Error refreshing project after completion:", err);
      }
    }
  };

  return (
    <div className="min-h-screen bg-[#080c14] text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar
        onNewProject={handleNewProjectClick}
        activeProjectIdea={activeProject?.idea}
        isExecuting={viewState === "executing"}
      />

      {/* Main Workspace Layout */}
      <div className="flex-1 flex">
        {/* Left Sidebar supporting 100+ items */}
        <Sidebar
          projects={projects}
          activeProjectId={activeProject?.id || null}
          onSelectProject={handleSelectProject}
          onNewProject={handleNewProjectClick}
          onDeleteProject={handleDeleteProject}
          isLoading={isLoadingHistory}
        />

        {/* Central Content Area */}
        <main className="flex-1 overflow-y-auto">
          {viewState === "landing" && (
            <LandingHero onSubmitIdea={handleCreateProject} isSubmitting={isSubmitting} />
          )}

          {viewState === "executing" && activeProject && (
            <ExecutionScreen
              project={activeProject}
              onExecutionComplete={handleExecutionComplete}
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
