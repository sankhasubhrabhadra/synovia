"use client";

import React, { useState, useEffect } from "react";
import { 
  createProject, listProjects, getProject, deleteProject, Project 
} from "@/lib/api";
import { Navbar } from "@/components/Navbar";
import { SidebarDrawer } from "@/components/SidebarDrawer";
import { LandingHero } from "@/components/LandingHero";
import { ExecutionScreen } from "@/components/ExecutionScreen";
import { BlueprintView } from "@/components/BlueprintView";
import { ErrorBoundary } from "@/components/ErrorBoundary";
import { IntroSplash } from "@/components/IntroSplash";
import { BackgroundCanvas } from "@/components/BackgroundCanvas";
import { CinematicLanding } from "@/components/CinematicLanding";

export function SynoviaApp() {
  const [showSplash, setShowSplash] = useState<boolean>(true);
  const [projects, setProjects] = useState<Project[]>([]);
  const [activeProject, setActiveProject] = useState<Project | null>(null);
  const [viewState, setViewState] = useState<"cinematic" | "prompt_workspace" | "executing" | "blueprint">("cinematic");
  const [isLoadingHistory, setIsLoadingHistory] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState<boolean>(false);

  // Load project history
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

  // Handle selecting a project from history drawer
  const handleSelectProject = async (id: string) => {
    try {
      const proj = await getProject(id);
      setActiveProject(proj);
      if (proj.status === "completed" && proj.blueprint) {
        setViewState("blueprint");
      } else {
        setViewState("executing");
      }
    } catch (err: any) {
      console.error("Failed to fetch project details:", err);
      alert(err.message || "Could not load project blueprint");
    }
  };

  // Handle deleting a single project
  const handleDeleteProject = async (id: string) => {
    try {
      await deleteProject(id);
      if (activeProject?.id === id) {
        setActiveProject(null);
        setViewState("cinematic");
      }
      fetchHistory();
    } catch (err) {
      console.error("Failed to delete project:", err);
    }
  };

  // Handle resetting back to cinematic landing screen
  const handleNewProject = () => {
    setActiveProject(null);
    setViewState("prompt_workspace");
  };

  return (
    <>
      {/* 1. Animated Intro Splash Screen with Logo */}
      {showSplash && (
        <IntroSplash onComplete={() => setShowSplash(false)} />
      )}

      <div className="min-h-screen bg-white text-black font-sans selection:bg-amber-400 selection:text-black relative overflow-x-hidden flex flex-col studio-canvas">
        {/* 2. Interactive 60FPS Neo-Brutalist Floating Background Animation */}
        <BackgroundCanvas />

        {/* Shifting Ambient Color Overlay */}
        <div className="colorful-bg-overlay" />

        {/* Persistent Header Navbar */}
        <Navbar
          onNewProject={handleNewProject}
          onOpenHistory={() => setIsHistoryOpen(true)}
          historyCount={projects.length}
          activeProjectIdea={activeProject?.idea}
          isExecuting={viewState === "executing"}
        />

        {/* 3. Hidden History Drawer */}
        <SidebarDrawer
          isOpen={isHistoryOpen}
          onClose={() => setIsHistoryOpen(false)}
          projects={projects}
          activeProjectId={activeProject?.id || null}
          onSelectProject={handleSelectProject}
          onNewProject={handleNewProject}
          onDeleteProject={handleDeleteProject}
          isLoading={isLoadingHistory}
        />

        {/* 4. Main Dynamic View Area */}
        <main className="flex-1 flex flex-col min-w-0 transition-all duration-300 relative z-10">
          {viewState === "cinematic" && (
            <CinematicLanding
              onEnterStudio={() => setViewState("prompt_workspace")}
              onSelectPreset={(idea, market) => handleCreateProject(idea, market)}
              onOpenHistory={() => setIsHistoryOpen(true)}
              historyCount={projects.length}
            />
          )}

          {viewState === "prompt_workspace" && (
            <LandingHero
              onSubmitIdea={handleCreateProject}
              isSubmitting={isSubmitting}
            />
          )}

          {viewState === "executing" && activeProject && (
            <ErrorBoundary fallbackMessage="An error occurred while tracking live agent progress. Your project will still complete in the background.">
              <ExecutionScreen
                project={activeProject}
                onExecutionComplete={async () => {
                  try {
                    const updated = await getProject(activeProject.id);
                    setActiveProject(updated);
                    setViewState("blueprint");
                    fetchHistory();
                  } catch (err) {
                    console.error("Error fetching completed project details:", err);
                  }
                }}
              />
            </ErrorBoundary>
          )}

          {viewState === "blueprint" && activeProject && (
            <ErrorBoundary fallbackMessage="An issue occurred while rendering this blueprint report. Please select another project or reload.">
              <BlueprintView project={activeProject} />
            </ErrorBoundary>
          )}
        </main>
      </div>
    </>
  );
}
