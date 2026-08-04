"use client";

import React, { useEffect, useState, useRef } from "react";
import { getProjectStreamUrl, getProject, Project } from "@/lib/api";
import { 
  Search, Users, Layout, ShieldCheck, Calendar, Presentation, 
  CheckCircle2, Loader2, Sparkles, Activity
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
  { id: "research", name: "Market Research Agent", icon: Search, role: "TAM/SAM/SOM & Personas", userMessage: "Researching market size & customer pain points..." },
  { id: "competitor", name: "Competitor Intelligence Agent", icon: Users, role: "Strengths, Weaknesses & Gaps", userMessage: "Finding competitors & market defensibility gaps..." },
  { id: "product", name: "Product Manager Agent", icon: Layout, role: "MVP Features & Priority Matrix", userMessage: "Designing MVP specs & user journey..." },
  { id: "roadmap", name: "Agile Roadmap Agent", icon: Calendar, role: "4-Week Schedule & Milestones", userMessage: "Building 4-week execution roadmap..." },
  { id: "pitch", name: "VC Pitch Strategy Agent", icon: Presentation, role: "USP, Business Model & Pitch", userMessage: "Preparing investor pitch deck & 60s pitch..." },
  { id: "validation", name: "Validation & Strategy Mentor", icon: ShieldCheck, role: "VC Scores, Risks & Verdict", userMessage: "Evaluating startup viability, risks & mentor verdict..." },
];

export function ExecutionScreen({ project, onExecutionComplete }: ExecutionScreenProps) {
  const [logs, setLogs] = useState<StepLog[]>([]);
  const [currentStep, setCurrentStep] = useState<string>(project.current_step || "research");
  const [progress, setProgress] = useState<number>(10);
  const [latestMessage, setLatestMessage] = useState<string>("Initializing autonomous agent swarm...");
  const isCompletedRef = useRef(false);

  useEffect(() => {
    let timer: NodeJS.Timeout;

    // Polling fallback to check project status every 2.5s guarantees execution completion even if SSE drops
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

        if (data.step === "completed" || data.status === "completed" && data.progress_percentage === 100) {
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

    eventSource.onerror = () => {
      // Do NOT close stream permanently on transient error; polling backup handles state
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
    if (progress >= 95 && agentId === "validation") return "completed";
    return "pending";
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Header Info */}
      <div className="glass-panel p-6 rounded-2xl mb-8 border border-indigo-500/20 glow-purple">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Sparkles className="w-4 h-4 text-indigo-400 animate-spin" />
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-300">
                Autonomous Pipeline Active
              </span>
            </div>
            <h2 className="text-xl md:text-2xl font-bold text-white leading-tight">
              "{project.idea}"
            </h2>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right">
              <span className="text-xs text-slate-400 block font-medium">Overall Progress</span>
              <span className="text-lg font-black text-indigo-400">{progress}%</span>
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden p-0.5 border border-slate-800">
          <div 
            className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-400 rounded-full transition-all duration-500 shadow-lg shadow-indigo-500/50"
            style={{ width: `${Math.max(progress, 5)}%` }}
          />
        </div>

        {/* Latest Activity Banner */}
        <div className="mt-4 p-3 rounded-xl bg-indigo-950/40 border border-indigo-500/30 flex items-center gap-3">
          <Loader2 className="w-4 h-4 text-indigo-400 animate-spin shrink-0" />
          <span className="text-xs text-indigo-200 font-medium">{latestMessage}</span>
        </div>
      </div>

      {/* Agents Execution Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mb-8">
        {AGENTS_LIST.map((agent) => {
          const Icon = agent.icon;
          const status = getAgentStatus(agent.id);

          return (
            <div
              key={agent.id}
              className={`p-5 rounded-2xl border transition-all duration-300 ${
                status === "completed"
                  ? "bg-slate-900/80 border-emerald-500/40 shadow-lg shadow-emerald-500/5"
                  : status === "running"
                  ? "bg-indigo-950/50 border-indigo-500/60 glow-purple scale-[1.02]"
                  : "bg-slate-950/40 border-slate-800/60 opacity-60"
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <div className={`p-2.5 rounded-xl ${
                  status === "completed" 
                    ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" 
                    : status === "running"
                    ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
                    : "bg-slate-800/50 text-slate-500"
                }`}>
                  <Icon className="w-5 h-5" />
                </div>

                <div>
                  {status === "completed" && (
                    <span className="inline-flex items-center gap-1 text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 uppercase">
                      <CheckCircle2 className="w-3 h-3" /> Done
                    </span>
                  )}
                  {status === "running" && (
                    <span className="inline-flex items-center gap-1 text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 uppercase animate-pulse">
                      <Loader2 className="w-3 h-3 animate-spin" /> Thinking
                    </span>
                  )}
                  {status === "pending" && (
                    <span className="text-[10px] font-semibold text-slate-500 uppercase">
                      Queued
                    </span>
                  )}
                </div>
              </div>

              <h3 className="font-bold text-sm text-white mb-1">{agent.name}</h3>
              <p className="text-[11px] text-slate-400 font-medium mb-3">{agent.role}</p>

              {status === "running" && (
                <p className="text-[11px] text-indigo-300 italic animate-pulse">
                  {agent.userMessage}
                </p>
              )}
            </div>
          );
        })}
      </div>

      {/* Terminal Live Activity Log */}
      <div className="glass-panel p-5 rounded-2xl border border-slate-800">
        <div className="flex items-center justify-between mb-3 border-b border-slate-800/80 pb-3">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-indigo-400" />
            <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Live Swarm Telemetry & Log Output
            </span>
          </div>
          <span className="text-[10px] text-slate-500 font-mono">SSE Stream Connected</span>
        </div>

        <div className="bg-slate-950 p-4 rounded-xl font-mono text-xs max-h-48 overflow-y-auto space-y-2 border border-slate-900 scrollbar-thin">
          {logs.length === 0 ? (
            <p className="text-slate-500 italic">Listening for active agent telemetry...</p>
          ) : (
            logs.map((log, idx) => (
              <div key={idx} className="flex items-start gap-3">
                <span className="text-[10px] text-slate-600 shrink-0 mt-0.5">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
                <span className={`text-xs ${
                  log.status === "completed" ? "text-emerald-400" : log.status === "failed" ? "text-rose-400" : "text-indigo-300"
                }`}>
                  [{log.step.toUpperCase()}] {log.message}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
