"use client";

import React, { useEffect, useState } from "react";
import { getProjectStreamUrl, Project } from "@/lib/api";
import { 
  Bot, Search, Users, Layout, ShieldCheck, Calendar, Presentation, 
  CheckCircle2, Loader2, Clock, Sparkles, Terminal, Activity, ArrowRight
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
  const [progress, setProgress] = useState<number>(5);
  const [latestMessage, setLatestMessage] = useState<string>("Initializing autonomous agent swarm...");

  useEffect(() => {
    const streamUrl = getProjectStreamUrl(project.id);
    const eventSource = new EventSource(streamUrl);

    eventSource.onmessage = (event) => {
      try {
        const data: StepLog = JSON.parse(event.data);
        setLogs((prev) => [...prev, data]);
        setCurrentStep(data.step);
        setProgress(data.progress_percentage);
        setLatestMessage(data.message);

        if (data.step === "completed" || data.status === "failed") {
          eventSource.close();
          if (data.step === "completed") {
            onExecutionComplete();
          }
        }
      } catch (err) {
        console.error("Error parsing SSE log:", err);
      }
    };

    eventSource.onerror = (err) => {
      console.error("SSE stream error:", err);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [project.id, onExecutionComplete]);

  const getAgentStatus = (agentId: string) => {
    const agentLogs = logs.filter((l) => l.step === agentId);
    if (agentLogs.some((l) => l.status === "completed")) return "completed";
    if (agentLogs.some((l) => l.status === "running") || currentStep === agentId) return "running";
    return "pending";
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Header Info */}
      <div className="glass-panel p-6 rounded-2xl mb-8 border border-indigo-500/20">
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
        <div className="w-full h-2.5 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
          <div
            className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-400 transition-all duration-500 rounded-full"
            style={{ width: `${Math.max(progress, 5)}%` }}
          />
        </div>

        {/* Status Message */}
        <div className="mt-3 flex items-center gap-2 text-xs font-medium text-slate-300">
          <Activity className="w-4 h-4 text-indigo-400 animate-pulse" />
          <span>{latestMessage}</span>
        </div>
      </div>

      {/* Agents Status Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {AGENTS_LIST.map((agent) => {
          const status = getAgentStatus(agent.id);
          const Icon = agent.icon;

          return (
            <div
              key={agent.id}
              className={`p-5 rounded-2xl border transition-all duration-300 relative overflow-hidden ${
                status === "completed"
                  ? "bg-slate-900/80 border-emerald-500/40 shadow-lg shadow-emerald-950/20"
                  : status === "running"
                  ? "bg-gradient-to-br from-indigo-950/90 to-purple-950/40 border-indigo-500/60 shadow-xl shadow-indigo-500/10 ring-1 ring-indigo-500/30"
                  : "bg-slate-900/30 border-slate-800/60 opacity-60"
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className={`p-2.5 rounded-xl border ${
                  status === "completed"
                    ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
                    : status === "running"
                    ? "bg-indigo-500/10 border-indigo-500/30 text-indigo-400"
                    : "bg-slate-800 border-slate-700 text-slate-500"
                }`}>
                  <Icon className="w-5 h-5" />
                </div>

                {/* Status Badge */}
                {status === "completed" ? (
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>Completed</span>
                  </span>
                ) : status === "running" ? (
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 animate-pulse">
                    <Loader2 className="w-3 h-3 animate-spin text-indigo-400" />
                    <span>Running...</span>
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-medium bg-slate-800/60 text-slate-500 border border-slate-700/60">
                    <Clock className="w-3 h-3" />
                    <span>Pending</span>
                  </span>
                )}
              </div>

              <h3 className="font-bold text-sm text-white mb-1">{agent.name}</h3>
              <p className="text-xs text-slate-400 mb-3">{agent.role}</p>

              {/* Status Indicator Bar */}
              <div className="pt-2 border-t border-slate-800/80 text-[11px] text-slate-400 font-medium">
                {status === "completed" ? (
                  <span className="text-emerald-400 font-semibold">Data synthesis finished</span>
                ) : status === "running" ? (
                  <span className="text-indigo-300 flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-ping" />
                    {agent.userMessage}
                  </span>
                ) : (
                  <span>Waiting in swarm sequence</span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Real-time Agent Activity Feed */}
      <div className="glass-panel rounded-2xl p-5 border border-slate-800">
        <div className="flex items-center justify-between mb-3 border-b border-slate-800/80 pb-3">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-300 uppercase tracking-wider">
            <Terminal className="w-4 h-4 text-indigo-400" />
            <span>Agent Activity Stream Log</span>
          </div>
          <span className="text-[11px] text-slate-500">{logs.length} events logged</span>
        </div>

        <div className="font-mono text-xs space-y-2 max-h-48 overflow-y-auto pr-2">
          {logs.length === 0 ? (
            <div className="text-slate-500 italic text-center py-4">
              Connecting to SSE execution stream...
            </div>
          ) : (
            logs.map((log, idx) => (
              <div key={idx} className="flex items-start gap-3 py-1 border-b border-slate-900/60 last:border-0">
                <span className="text-slate-500 text-[10px] shrink-0 font-medium">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
                <span className={`uppercase font-bold text-[10px] px-1.5 py-0.5 rounded shrink-0 ${
                  log.status === "completed"
                    ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                    : "bg-indigo-950 text-indigo-300 border border-indigo-800"
                }`}>
                  [{log.step}]
                </span>
                <span className="text-slate-300 leading-normal">{log.message}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
