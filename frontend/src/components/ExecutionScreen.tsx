"use client";

import React, { useEffect, useState, useRef } from "react";
import { getProjectStreamUrl, getProject, Project } from "@/lib/api";
import { 
  Search, Users, Layout, ShieldCheck, Calendar, Presentation, 
  CheckCircle2, Loader2, Sparkles, Activity, Layers, ShieldAlert, Cpu
} from "lucide-react";

interface ExecutionScreenProps {
  project: Project;
  onExecutionComplete: () => void;
}

interface StepLog {
  project_id: string;
  step: string;
  status: "pending" | "running" | "completed" | "failed";
  progress_percentage: number;
  message: string;
  timestamp: string;
  step_data?: any;
}

const AGENTS_LIST = [
  { id: "classification", name: "1. Idea Classification Agent", icon: Layers, role: "Business Type & Anti-Pattern Rules", userMessage: "Classifying business type & domain anti-patterns..." },
  { id: "research", name: "2. Market Research Agent", icon: Search, role: "Industry TAM/SAM/SOM & Personas", userMessage: "Researching market dynamics & customer pain points..." },
  { id: "competitor", name: "3. Competitor Intelligence Agent", icon: Users, role: "Real Incumbents & Moat Strategy", userMessage: "Benchmarking competitors & defensibility gaps..." },
  { id: "product", name: "4. MVP Product Manager Agent", icon: Layout, role: "Domain Features & Priority Matrix", userMessage: "Designing MVP features matching business category..." },
  { id: "roadmap", name: "5. Agile Roadmap Agent", icon: Calendar, role: "4-Week Category Execution Plan", userMessage: "Building 4-week execution roadmap..." },
  { id: "pitch", name: "6. VC Pitch & Strategy Agent", icon: Presentation, role: "Business Model & Revenue Streams", userMessage: "Crafting investor pitch & monetization model..." },
  { id: "validation", name: "7. Validation & Strategy Mentor", icon: ShieldCheck, role: "YC/VC Scores, Risks & Verdict", userMessage: "Conducting viability assessment & mentor verdict..." },
  { id: "quality_control", name: "8. Quality Control Audit Agent", icon: ShieldAlert, role: "Anti-SaaS Verification & Audit", userMessage: "Auditing outputs for category consistency..." },
];

export function ExecutionScreen({ project, onExecutionComplete }: ExecutionScreenProps) {
  const [logs, setLogs] = useState<StepLog[]>([]);
  const [currentStep, setCurrentStep] = useState<string>(project.current_step || "classification");
  const [progress, setProgress] = useState<number>(10);
  const [latestMessage, setLatestMessage] = useState<string>("Initializing autonomous 8-agent swarm...");
  const isCompletedRef = useRef(false);

  useEffect(() => {
    let timer: NodeJS.Timeout;

    // Polling fallback every 2.5s ensures completion even if SSE connection drops
    const checkProjectStatus = async () => {
      if (isCompletedRef.current) return;
      try {
        const updatedProject = await getProject(project.id);
        if (updatedProject) {
          if (updatedProject.status === "completed") {
            isCompletedRef.current = true;
            setProgress(100);
            setCurrentStep("completed");
            setLatestMessage("Startup Blueprint ready!");
            onExecutionComplete();
            return;
          }
          if (updatedProject.current_step) {
            setCurrentStep(updatedProject.current_step);
          }
        }
      } catch (e) {
        console.warn("Polling status notice:", e);
      }
    };

    timer = setInterval(checkProjectStatus, 2500);

    // SSE Stream
    const streamUrl = getProjectStreamUrl(project.id);
    const eventSource = new EventSource(streamUrl);

    eventSource.onmessage = (event) => {
      try {
        const data: StepLog = JSON.parse(event.data);
        setLogs((prev) => [...prev, data]);
        setCurrentStep(data.step);
        setProgress(data.progress_percentage);
        setLatestMessage(data.message);

        if (data.step === "completed" || (data.status === "completed" && data.progress_percentage === 100)) {
          if (!isCompletedRef.current) {
            isCompletedRef.current = true;
            eventSource.close();
            onExecutionComplete();
          }
        }
      } catch (err) {
        console.error("Error parsing SSE log:", err);
      }
    };

    return () => {
      clearInterval(timer);
      eventSource.close();
    };
  }, [project.id, onExecutionComplete]);

  const getAgentStatus = (agentId: string) => {
    const agentLogs = logs.filter((l) => l.step === agentId);
    if (agentLogs.some((l) => l.status === "completed")) return "completed";
    if (agentLogs.some((l) => l.status === "running") || currentStep === agentId) return "running";
    if (progress >= 95 && agentId === "quality_control") return "completed";
    return "pending";
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Studio Header Info Banner */}
      <div className="studio-panel p-6 rounded-3xl mb-8 border border-blue-500/20 glow-gemini">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <Sparkles className="w-4 h-4 text-blue-400 animate-spin" />
              <span className="text-xs font-extrabold uppercase tracking-wider text-blue-300">
                Studio Swarm Pipeline Active (8 Agents)
              </span>
            </div>
            <h2 className="text-xl md:text-2xl font-black text-white leading-tight">
              "{project.idea}"
            </h2>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right">
              <span className="text-xs text-slate-400 block font-medium">Pipeline Progress</span>
              <span className="text-xl font-black text-gradient-gemini">{progress}%</span>
            </div>
          </div>
        </div>

        {/* Gemini Gradient Progress Bar */}
        <div className="w-full h-3 bg-slate-950 rounded-full overflow-hidden p-0.5 border border-slate-800">
          <div 
            className="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 rounded-full transition-all duration-500 shadow-lg shadow-blue-500/50"
            style={{ width: `${Math.max(progress, 5)}%` }}
          />
        </div>

        {/* Live Status Banner */}
        <div className="mt-4 p-3 rounded-xl bg-blue-950/40 border border-blue-500/30 flex items-center gap-3">
          <Loader2 className="w-4 h-4 text-blue-400 animate-spin shrink-0" />
          <span className="text-xs text-blue-200 font-medium">{latestMessage}</span>
        </div>
      </div>

      {/* 8-Agent Execution Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3.5 mb-8">
        {AGENTS_LIST.map((agent) => {
          const Icon = agent.icon;
          const status = getAgentStatus(agent.id);

          return (
            <div
              key={agent.id}
              className={`p-4 rounded-2xl border transition-all duration-300 ${
                status === "completed"
                  ? "bg-slate-900/80 border-emerald-500/40 shadow-lg shadow-emerald-500/5"
                  : status === "running"
                  ? "bg-blue-950/80 border-blue-500/80 glow-blue gemini-border-beam scanline-sweep scale-[1.02]"
                  : "bg-slate-950/40 border-slate-800/60 opacity-60"
              }`}
            >
              <div className="flex items-center justify-between mb-2.5">
                <div className={`p-2 rounded-xl ${
                  status === "completed" 
                    ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" 
                    : status === "running"
                    ? "bg-blue-500/20 text-blue-300 border border-blue-500/30"
                    : "bg-slate-800/50 text-slate-500"
                }`}>
                  <Icon className="w-4 h-4" />
                </div>

                <div>
                  {status === "completed" && (
                    <span className="inline-flex items-center gap-1 text-[9px] font-black px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 uppercase">
                      <CheckCircle2 className="w-3 h-3" /> Ready
                    </span>
                  )}
                  {status === "running" && (
                    <span className="inline-flex items-center gap-1 text-[9px] font-black px-2 py-0.5 rounded-md bg-blue-500/20 text-blue-300 border border-blue-500/40 uppercase animate-pulse">
                      <Loader2 className="w-3 h-3 animate-spin" /> Thinking
                    </span>
                  )}
                  {status === "pending" && (
                    <span className="text-[9px] font-bold text-slate-500 uppercase">
                      Queued
                    </span>
                  )}
                </div>
              </div>

              <h3 className="font-bold text-xs text-white mb-0.5 leading-snug">{agent.name}</h3>
              <p className="text-[10px] text-slate-400 font-medium mb-2">{agent.role}</p>

              {status === "running" && (
                <p className="text-[10px] text-blue-300 italic animate-pulse">
                  {agent.userMessage}
                </p>
              )}
            </div>
          );
        })}
      </div>

      {/* Live Swarm Telemetry Terminal */}
      <div className="studio-panel p-5 rounded-2xl border border-slate-800">
        <div className="flex items-center justify-between mb-3 border-b border-slate-800/80 pb-3">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-blue-400" />
            <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Live Swarm Console & Telemetry Output
            </span>
          </div>
          <span className="text-[10px] text-slate-500 font-mono">Stream Active</span>
        </div>

        <div className="bg-slate-950 p-4 rounded-xl font-mono text-xs max-h-48 overflow-y-auto space-y-2 border border-slate-900 scrollbar-thin">
          {logs.length === 0 ? (
            <p className="text-slate-500 italic">Listening for live agent telemetry stream...</p>
          ) : (
            logs.map((log, idx) => (
              <div key={idx} className="flex items-start gap-3">
                <span className="text-[10px] text-slate-600 shrink-0 mt-0.5">
                  {(() => {
                    try {
                      const d = new Date(log.timestamp);
                      return isNaN(d.getTime()) ? "00:00" : d.toLocaleTimeString();
                    } catch {
                      return "00:00";
                    }
                  })()}
                </span>
                <span className={`text-xs ${
                  log.status === "completed" ? "text-emerald-400" : log.status === "failed" ? "text-rose-400" : "text-blue-300"
                }`}>
                  [{String(log.step || "step").toUpperCase()}] {log.message}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
