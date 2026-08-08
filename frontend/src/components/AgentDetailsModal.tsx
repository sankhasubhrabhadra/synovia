import React from "react";
import { 
  X, CheckCircle, AlertTriangle, FileText, Download, ShieldCheck, Cpu, 
  Activity, ExternalLink, FileSpreadsheet, Code
} from "lucide-react";
import { downloadAgentReportFile } from "@/lib/api";

interface ChecklistItem {
  name: string;
  completed: boolean;
  is_evidence?: boolean;
  details?: string;
}

interface AgentChecklist {
  agent_name: string;
  total_items: number;
  completed_items: number;
  completion_percentage: number;
  status: string;
  items: ChecklistItem[];
}

interface AgentDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  projectId: string;
  idea: string;
  agentName: string;
  agentStatus?: string;
  checklist?: AgentChecklist;
  agentData?: any;
}

export function AgentDetailsModal({
  isOpen,
  onClose,
  projectId,
  idea,
  agentName,
  agentStatus = "COMPLETED",
  checklist,
  agentData
}: AgentDetailsModalProps) {
  if (!isOpen) return null;

  const cleanAgentTitle = agentName.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
  const compPct = checklist?.completion_percentage ?? 100;
  const statusLabel = checklist?.status || agentStatus || "COMPLETE";

  const handleExport = (fmt: "pdf" | "csv" | "html") => {
    if (projectId) {
      downloadAgentReportFile(projectId, agentName, fmt);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 font-sans selection:bg-black selection:text-white">
      <div className="bg-[#fefae0] border-4 border-black shadow-[12px_12px_0px_#000000] w-full max-w-2xl p-6 relative animate-in zoom-in-95 duration-150 max-h-[90vh] overflow-y-auto">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between border-b-4 border-black pb-4 mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-[#3b82f6] border-3 border-black shadow-[3px_3px_0px_#000000] flex items-center justify-center font-black text-white">
              <Cpu className="w-6 h-6 stroke-[2.5]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-xl font-black uppercase text-black tracking-tight">
                  {cleanAgentTitle}
                </h3>
                <span className={`px-2.5 py-0.5 border-2 border-black text-[10px] font-black uppercase tracking-wider ${
                  statusLabel === "COMPLETE" ? "bg-[#10b981] text-black" : "bg-[#f59e0b] text-black"
                }`}>
                  {statusLabel}
                </span>
              </div>
              <p className="text-xs font-bold text-gray-700">
                Project: {idea} | ID: {projectId.slice(0, 8)}
              </p>
            </div>
          </div>

          <button 
            onClick={onClose}
            className="p-1.5 bg-white hover:bg-black hover:text-white border-2 border-black text-black transition-colors font-black"
            title="Close modal"
          >
            <X className="w-5 h-5 stroke-[2.5]" />
          </button>
        </div>

        {/* Progress Bar & Summary Stats */}
        <div className="bg-white border-3 border-black p-4 shadow-[4px_4px_0px_#000000] mb-5">
          <div className="flex items-center justify-between text-xs font-black uppercase mb-1.5">
            <span>SOURCE CHECKLIST VERIFICATION</span>
            <span className="text-[#3b82f6]">{compPct}% COMPLETE</span>
          </div>
          <div className="w-full bg-gray-200 h-3 border-2 border-black overflow-hidden">
            <div 
              className="bg-[#10b981] h-full transition-all duration-300"
              style={{ width: `${compPct}%` }}
            />
          </div>
          <p className="text-[11px] font-bold text-gray-600 mt-2">
            Verified {checklist?.completed_items || 0} of {checklist?.total_items || 5} required inputs & market evidence fields.
          </p>
        </div>

        {/* 1. Source Checklist Section */}
        <div className="mb-6">
          <h4 className="text-sm font-black uppercase text-black tracking-wider border-b-2 border-black pb-1.5 mb-3 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-[#3b82f6]" />
            ROLE-SPECIFIC SOURCE CHECKLIST
          </h4>
          
          <div className="space-y-2">
            {checklist?.items?.map((item, i) => (
              <div 
                key={i}
                className={`p-3 border-2 border-black flex items-center justify-between text-xs font-bold ${
                  item.completed 
                    ? "bg-[#10b981]/15 text-black border-black" 
                    : "bg-amber-100 text-amber-900 border-black"
                }`}
              >
                <div className="flex items-center gap-2.5">
                  {item.completed ? (
                    <CheckCircle className="w-4 h-4 text-[#059669] shrink-0 stroke-[2.5]" />
                  ) : (
                    <AlertTriangle className="w-4 h-4 text-[#d97706] shrink-0 stroke-[2.5]" />
                  )}
                  <span>{item.name}</span>
                </div>

                <div className="flex items-center gap-2">
                  {item.is_evidence && (
                    <span className="px-1.5 py-0.5 bg-black text-white text-[9px] font-black uppercase border border-black">
                      EVIDENCE
                    </span>
                  )}
                  <span className={`px-2 py-0.5 border border-black text-[10px] font-black uppercase ${
                    item.completed ? "bg-[#10b981] text-black" : "bg-[#f59e0b] text-black"
                  }`}>
                    {item.completed ? "VERIFIED" : "MISSING"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 2. Agent Output & Findings */}
        <div className="mb-6">
          <h4 className="text-sm font-black uppercase text-black tracking-wider border-b-2 border-black pb-1.5 mb-3 flex items-center gap-2">
            <FileText className="w-4 h-4 text-[#3b82f6]" />
            AGENT DELIVERABLES & FINDINGS
          </h4>

          <div className="bg-white border-3 border-black p-4 font-mono text-xs max-h-60 overflow-y-auto space-y-3 shadow-[4px_4px_0px_#000000]">
            {agentData ? (
              typeof agentData === "object" ? (
                Object.entries(agentData).map(([key, val]) => (
                  <div key={key} className="border-b border-dashed border-gray-300 pb-2">
                    <span className="font-bold uppercase text-[#3b82f6] block mb-1">
                      {key.replace(/_/g, " ")}:
                    </span>
                    <p className="text-gray-900 whitespace-pre-wrap font-sans leading-relaxed">
                      {typeof val === "object" ? JSON.stringify(val, null, 2) : String(val)}
                    </p>
                  </div>
                ))
              ) : (
                <p className="text-gray-900 font-sans">{String(agentData)}</p>
              )
            ) : (
              <p className="text-gray-500 italic">Agent execution output payload ready.</p>
            )}
          </div>
        </div>

        {/* Export Buttons Bar */}
        <div className="border-t-4 border-black pt-4 flex flex-wrap items-center justify-between gap-3">
          <span className="text-xs font-black uppercase text-black flex items-center gap-1">
            <Activity className="w-4 h-4 text-[#10b981]" /> EXPORT SPECIFIC REPORT:
          </span>

          <div className="flex items-center gap-2">
            <button
              onClick={() => handleExport("pdf")}
              className="px-3.5 py-2 bg-black text-white hover:bg-zinc-800 border-2 border-black text-xs font-black uppercase shadow-[3px_3px_0px_#000000] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all flex items-center gap-1.5"
            >
              <Download className="w-3.5 h-3.5" /> EXPORT PDF
            </button>

            <button
              onClick={() => handleExport("csv")}
              className="px-3 py-2 bg-white text-black hover:bg-gray-100 border-2 border-black text-xs font-black uppercase shadow-[3px_3px_0px_#000000] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all flex items-center gap-1.5"
            >
              <FileSpreadsheet className="w-3.5 h-3.5 text-[#059669]" /> CSV
            </button>

            <button
              onClick={() => handleExport("html")}
              className="px-3 py-2 bg-white text-black hover:bg-gray-100 border-2 border-black text-xs font-black uppercase shadow-[3px_3px_0px_#000000] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all flex items-center gap-1.5"
            >
              <Code className="w-3.5 h-3.5 text-[#3b82f6]" /> HTML
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
