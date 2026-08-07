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
  { id: "classification", name: "1. Idea Classification Agent", icon: Layers, role: "Business Type & Domain Anti-Patterns", userMessage: "Classifying business type & domain anti-patterns..." },
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
    <div className="max-w-5xl mx-auto px-4 py-8 relative z-10">
      {/* Studio Header Info Banner */}
      <div className="studio-panel p-6 bg-white border-4 border-black shadow-[8px_8px_0px_#000000] mb-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <Sparkles className="w-4 h-4 text-black animate-spin" />
              <span className="text-xs font-black uppercase tracking-wider text-black">
                Studio Swarm Pipeline Active (8 Agents)
              </span>
            </div>
            <h2 className="text-xl md:text-2xl font-black text-black uppercase leading-tight">
              "{project.idea}"
            </h2>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right">
              <span className="text-xs text-gray-700 block font-black uppercase">Pipeline Progress</span>
              <span className="text-3xl font-black text-[#ea580c]">{progress}%</span>
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full h-4 bg-white border-3 border-black shadow-[3px_3px_0px_#000000]">
          <div 
            className="h-full bg-[#f59e0b] border-r-2 border-black transition-all duration-500"
            style={{ width: `${Math.max(progress, 5)}%` }}
          />
        </div>

        {/* Live Status Banner */}
        <div className="mt-4 p-3.5 bg-[#fefae0] border-3 border-black shadow-[3px_3px_0px_#000000] flex items-center gap-3">
          <Loader2 className="w-4 h-4 text-black animate-spin shrink-0 stroke-[3]" />
          <span className="text-xs text-black font-black uppercase">{latestMessage}</span>
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
              className={`p-4 border-3 border-black transition-all duration-150 ${
                status === "completed"
                  ? "bg-[#dcfce7] shadow-[5px_5px_0px_#000000]"
                  : status === "running"
                  ? "bg-[#fef08a] shadow-[7px_7px_0px_#000000] translate-x-[-2px] translate-y-[-2px]"
                  : "bg-white opacity-70 shadow-[3px_3px_0px_#000000]"
              }`}
            >
              <div className="flex items-center justify-between mb-2.5">
                <div className={`p-2 border-2 border-black shadow-[2px_2px_0px_#000000] ${
                  status === "completed" 
                    ? "bg-[#10b981] text-black" 
                    : status === "running"
                    ? "bg-[#f59e0b] text-black"
                    : "bg-gray-100 text-gray-700"
                }`}>
                  <Icon className="w-4 h-4 stroke-[2.5]" />
                </div>

                <div>
                  {status === "completed" && (
                    <span className="inline-flex items-center gap-1 text-[9px] font-black px-2 py-0.5 bg-[#10b981] text-black border-2 border-black uppercase shadow-[1.5px_1.5px_0px_#000000]">
                      <CheckCircle2 className="w-3 h-3 stroke-[3]" /> Ready
                    </span>
                  )}
                  {status === "running" && (
                    <span className="inline-flex items-center gap-1 text-[9px] font-black px-2 py-0.5 bg-[#ea580c] text-white border-2 border-black uppercase shadow-[1.5px_1.5px_0px_#000000] animate-pulse">
                      <Loader2 className="w-3 h-3 animate-spin stroke-[3]" /> Thinking
                    </span>
                  )}
                  {status === "pending" && (
                    <span className="text-[9px] font-black text-gray-600 uppercase">
                      Queued
                    </span>
                  )}
                </div>
              </div>

              <h3 className="font-black text-xs text-black mb-0.5 uppercase leading-snug">{agent.name}</h3>
              <p className="text-[10px] text-gray-700 font-bold mb-2">{agent.role}</p>

              {status === "running" && (
                <p className="text-[10px] text-black font-black italic uppercase">
                  {agent.userMessage}
                </p>
              )}
            </div>
          );
        })}
      </div>

      {/* Live Swarm Telemetry Terminal */}
      <div className="studio-panel p-5 bg-white border-4 border-black shadow-[8px_8px_0px_#000000]">
        <div className="flex items-center justify-between mb-3 border-b-3 border-black pb-3">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-black" />
            <span className="text-xs font-black uppercase tracking-wider text-black">
              Live Swarm Console & Telemetry Output
            </span>
          </div>
          <span className="text-[10px] text-black font-mono font-bold bg-[#fefae0] px-2 py-0.5 border-2 border-black shadow-[1.5px_1.5px_0px_#000000]">Stream Active</span>
        </div>

        <div className="bg-white p-4 font-mono text-xs max-h-48 overflow-y-auto space-y-2 border-3 border-black shadow-[4px_4px_0px_#000000] scrollbar-thin">
          {logs.length === 0 ? (
            <p className="text-gray-500 italic font-bold">Listening for live agent telemetry stream...</p>
          ) : (
            logs.map((log, idx) => (
              <div key={idx} className="flex items-start gap-3">
                <span className="text-[10px] text-gray-500 font-bold shrink-0 mt-0.5">
                  {(() => {
                    try {
                      const d = new Date(log.timestamp);
                      return isNaN(d.getTime()) ? "00:00" : d.toLocaleTimeString();
                    } catch {
                      return "00:00";
                    }
                  })()}
                </span>
                <span className={`text-xs font-bold ${
                  log.status === "completed" ? "text-emerald-700" : log.status === "failed" ? "text-rose-700" : "text-black"
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
