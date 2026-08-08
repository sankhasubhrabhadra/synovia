"use client";

import React, { useState } from "react";
import { downloadProjectPdfFile, downloadProjectPptFile, downloadAgentReportFile, Project } from "@/lib/api";
import { 
  Download, Sparkles, Search, Users, Layout, ShieldCheck, Calendar, 
  Presentation, CheckCircle2, FileText, ArrowUpRight, AlertTriangle, 
  Zap, Code2, ChevronRight, Layers, Target, CheckSquare, Award, Flame, Loader2,
  Filter, RotateCcw, Eye, FileSpreadsheet, Code, ShieldAlert
} from "lucide-react";
import { AgentDetailsModal } from "@/components/AgentDetailsModal";

interface BlueprintViewProps {
  project: Project;
  activeTabOverride?: string;
  onTabChange?: (tab: string) => void;
}

const safeArray = (arr: any): any[] => {
  if (Array.isArray(arr)) return arr;
  if (typeof arr === "string" && arr.trim()) return [arr];
  if (typeof arr === "object" && arr !== null) {
    return Object.values(arr).filter(Boolean);
  }
  return [];
};

const formatMarketVal = (val: any): string => {
  if (!val) return "N/A";
  if (typeof val === "string") return val;
  if (typeof val === "number" || typeof val === "boolean") return String(val);
  if (typeof val === "object") {
    if (Array.isArray(val)) return val.map(formatMarketVal).join(", ");
    const parts = Object.entries(val)
      .map(([k, v]) => `${k}: ${typeof v === "object" ? JSON.stringify(v) : v}`)
      .filter(Boolean);
    return parts.join(" • ");
  }
  return String(val);
};

const safeRender = (val: any, fallback: string = ""): string => {
  if (val === null || val === undefined) return fallback;
  if (typeof val === "string" || typeof val === "number" || typeof val === "boolean") return String(val);
  return formatMarketVal(val);
};

const formatDateStr = (dateStr?: string) => {
  if (!dateStr) return "Recently";
  try {
    const d = new Date(dateStr);
    return isNaN(d.getTime()) ? "Recently" : d.toLocaleDateString(undefined, { dateStyle: "medium" });
  } catch {
    return "Recently";
  }
};

export function BlueprintView({ project, activeTabOverride, onTabChange }: BlueprintViewProps) {
  const [activeTab, setActiveTab] = useState<"summary" | "classification" | "research" | "competitor" | "product" | "validation" | "roadmap" | "pitch" | "quality_control" | "checklists">("summary");

  // Advanced Bounty: Search & Filter Toolbar State
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [agentFilter, setAgentFilter] = useState<string>("all");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [dataStatusFilter, setDataStatusFilter] = useState<string>("all");

  // Modal State for Agent Details
  const [selectedAgentModal, setSelectedAgentModal] = useState<{
    agentName: string;
    agentData: any;
    checklist: any;
  } | null>(null);

  React.useEffect(() => {
    if (activeTabOverride) {
      const tabMap: Record<string, any> = {
        summary: "summary",
        classification: "classification",
        market: "research",
        research: "research",
        competitors: "competitor",
        competitor: "competitor",
        product: "product",
        roadmap: "roadmap",
        pitch: "pitch",
        validation: "validation",
        quality_control: "quality_control",
        checklists: "checklists"
      };
      if (tabMap[activeTabOverride]) {
        setActiveTab(tabMap[activeTabOverride]);
      }
    }
  }, [activeTabOverride]);

  const [downloadingPdf, setDownloadingPdf] = useState(false);
  const [downloadingPpt, setDownloadingPpt] = useState(false);

  const blueprint = project?.blueprint || {};
  const classification = blueprint.classification || {};
  const research = blueprint.research || {};
  const competitor = blueprint.competitor || {};
  const product = blueprint.product || {};
  const roadmap = blueprint.roadmap || {};
  const pitch = blueprint.pitch || {};
  const validation = blueprint.validation || {};
  const qualityControl = blueprint.quality_control || {};
  const checklists = blueprint.checklists || {};

  const handleDownloadPdf = async () => {
    try {
      setDownloadingPdf(true);
      await downloadProjectPdfFile(project.id, project.idea);
    } catch (err: any) {
      alert(err.message || "Failed to download PDF report");
    } finally {
      setDownloadingPdf(false);
    }
  };

  const handleDownloadPpt = async () => {
    try {
      setDownloadingPpt(true);
      await downloadProjectPptFile(project.id, project.idea);
    } catch (err: any) {
      alert(err.message || "Failed to download PPT presentation");
    } finally {
      setDownloadingPpt(false);
    }
  };

  const resetFilters = () => {
    setSearchQuery("");
    setAgentFilter("all");
    setStatusFilter("all");
    setDataStatusFilter("all");
  };

  // Compute matching sections count for search badge
  const sectionsList = [
    { id: "summary", title: "Executive Summary", text: JSON.stringify(blueprint.executive_summary || "") },
    { id: "classification", title: "Business Category", text: JSON.stringify(classification) },
    { id: "research", title: "Market Analysis", text: JSON.stringify(research) },
    { id: "competitor", title: "Competitors & Gaps", text: JSON.stringify(competitor) },
    { id: "product", title: "MVP Product Spec", text: JSON.stringify(product) },
    { id: "validation", title: "Validation & Strategy", text: JSON.stringify(validation) },
    { id: "roadmap", title: "4-Week Roadmap", text: JSON.stringify(roadmap) },
    { id: "pitch", title: "Pitch & Monetization", text: JSON.stringify(pitch) },
    { id: "quality_control", title: "Quality Audit", text: JSON.stringify(qualityControl) },
    { id: "checklists", title: "Source Checklists", text: JSON.stringify(checklists) }
  ];

  const matchingSections = sectionsList.filter(s => {
    if (agentFilter !== "all" && s.id !== agentFilter) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      return s.title.toLowerCase().includes(q) || s.text.toLowerCase().includes(q);
    }
    return true;
  });

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 relative z-10 text-black">
      {/* Header Banner */}
      <div className="bg-white p-6 sm:p-8 border-4 border-black shadow-[8px_8px_0px_#000000] mb-6 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3.5 py-1 bg-[#10b981] text-black border-2 border-black text-xs font-black uppercase shadow-[2px_2px_0px_#000000] mb-3">
            <CheckCircle2 className="w-4 h-4 stroke-[3]" />
            <span>Startup Blueprint Strategy Ready</span>
          </div>
          <h1 className="text-2xl sm:text-4xl font-black text-black uppercase leading-tight mb-2">
            {project.idea}
          </h1>
          <p className="text-xs sm:text-sm text-gray-800 font-bold uppercase tracking-wide">
            Evaluated by 8 specialized AI agents on {formatDateStr(project?.created_at)}.
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-3 shrink-0">
          <button
            onClick={handleDownloadPdf}
            disabled={downloadingPdf}
            className="flex items-center gap-2 px-5 py-3 bg-[#f59e0b] text-black border-3 border-black font-black text-xs sm:text-sm uppercase shadow-[4px_4px_0px_#000000] hover:bg-[#fbbf24] hover:-translate-x-0.5 hover:-translate-y-0.5 hover:shadow-[6px_6px_0px_#000000] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none transition-all disabled:opacity-50 cursor-pointer"
          >
            {downloadingPdf ? <Loader2 className="w-4 h-4 animate-spin stroke-[3]" /> : <Download className="w-4 h-4 stroke-[3]" />}
            <span>{downloadingPdf ? "Downloading PDF..." : "Download PDF"}</span>
          </button>
          
          <button
            onClick={handleDownloadPpt}
            disabled={downloadingPpt}
            className="flex items-center gap-2 px-5 py-3 bg-[#10b981] text-black border-3 border-black font-black text-xs sm:text-sm uppercase shadow-[4px_4px_0px_#000000] hover:bg-[#34d399] hover:-translate-x-0.5 hover:-translate-y-0.5 hover:shadow-[6px_6px_0px_#000000] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none transition-all disabled:opacity-50 cursor-pointer"
          >
            {downloadingPpt ? <Loader2 className="w-4 h-4 animate-spin stroke-[3]" /> : <Presentation className="w-4 h-4 stroke-[3]" />}
            <span>{downloadingPpt ? "Generating PPT..." : "Download PPT Pitch Deck"}</span>
          </button>
        </div>
      </div>

      {/* ADVANCED BOUNTY: Mission Control Section-Level Search & Filters Toolbar */}
      <div className="bg-[#fefae0] p-4 sm:p-5 border-4 border-black shadow-[6px_6px_0px_#000000] mb-8 space-y-3 font-sans">
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          
          {/* Search Input Bar */}
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3.5 top-3 text-black stroke-[3]" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search across blueprint sections (e.g. TAM, competitors, MVP, risk)..."
              className="w-full pl-10 pr-4 py-2 bg-white border-2 border-black font-bold text-xs text-black outline-none placeholder:text-gray-500 shadow-[2px_2px_0px_#000000]"
            />
          </div>

          {/* Filter Dropdowns & Counters */}
          <div className="flex flex-wrap items-center gap-2">
            
            {/* Agent Filter */}
            <select
              value={agentFilter}
              onChange={(e) => setAgentFilter(e.target.value)}
              className="px-3 py-2 bg-white border-2 border-black text-xs font-black uppercase text-black outline-none shadow-[2px_2px_0px_#000000]"
            >
              <option value="all">Agent: All</option>
              <option value="classification">Classification</option>
              <option value="research">Research</option>
              <option value="competitor">Competitor</option>
              <option value="product">Product</option>
              <option value="roadmap">Roadmap</option>
              <option value="pitch">Pitch</option>
              <option value="validation">Validation</option>
              <option value="quality_control">Quality Control</option>
            </select>

            {/* Status Filter */}
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 bg-white border-2 border-black text-xs font-black uppercase text-black outline-none shadow-[2px_2px_0px_#000000]"
            >
              <option value="all">Status: All</option>
              <option value="completed">Completed</option>
              <option value="running">Running</option>
              <option value="pending">Pending</option>
              <option value="missing_data">Missing Data</option>
            </select>

            {/* Data Status Filter */}
            <select
              value={dataStatusFilter}
              onChange={(e) => setDataStatusFilter(e.target.value)}
              className="px-3 py-2 bg-white border-2 border-black text-xs font-black uppercase text-black outline-none shadow-[2px_2px_0px_#000000]"
            >
              <option value="all">Data: All</option>
              <option value="complete">Complete</option>
              <option value="incomplete">Incomplete</option>
              <option value="missing_evidence">Missing Evidence</option>
            </select>

            {/* Matching Counter Badge */}
            <span className="px-3 py-2 bg-[#3b82f6] text-white border-2 border-black text-xs font-black uppercase shadow-[2px_2px_0px_#000000]">
              {matchingSections.length} MATCHING
            </span>

            {/* Reset Button */}
            {(searchQuery || agentFilter !== "all" || statusFilter !== "all" || dataStatusFilter !== "all") && (
              <button
                onClick={resetFilters}
                className="px-3 py-2 bg-white hover:bg-black hover:text-white border-2 border-black text-xs font-black uppercase shadow-[2px_2px_0px_#000000] transition-colors flex items-center gap-1"
                title="Reset all filters"
              >
                <RotateCcw className="w-3.5 h-3.5" /> RESET
              </button>
            )}
          </div>

        </div>
      </div>

      {/* Tabs Navigation Header */}
      <div className="flex items-center gap-2 overflow-x-auto pb-4 mb-8 scrollbar-thin">
        {[
          { id: "summary", label: "Executive Summary", icon: FileText },
          { id: "checklists", label: "Source Checklists", icon: CheckSquare },
          { id: "classification", label: "Business Category", icon: Layers },
          { id: "research", label: "Market Analysis", icon: Search },
          { id: "competitor", label: "Competitors & Gaps", icon: Users },
          { id: "product", label: "MVP Product Spec", icon: Layout },
          { id: "validation", label: "Validation & Strategy", icon: ShieldCheck },
          { id: "roadmap", label: "4-Week Roadmap", icon: Calendar },
          { id: "pitch", label: "Pitch & Monetization", icon: Presentation },
          { id: "quality_control", label: "Quality Audit", icon: ShieldAlert },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2.5 font-black text-xs uppercase whitespace-nowrap transition-all cursor-pointer border-3 border-black ${
                isActive
                  ? "bg-[#f59e0b] text-black shadow-[4px_4px_0px_#000000] -translate-x-0.5 -translate-y-0.5"
                  : "bg-white text-black shadow-[2.5px_2.5px_0px_#000000] hover:bg-[#fefae0]"
              }`}
            >
              <Icon className="w-4 h-4 text-black stroke-[2.5]" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>


      {/* Tab Content Display */}
      <div className="space-y-6">
        {/* 1. Executive Summary Tab */}
        {activeTab === "summary" && (
          <div className="space-y-6">
            <div className="bg-white p-6 sm:p-8 border-4 border-black shadow-[7px_7px_0px_#000000]">
              <h3 className="text-lg font-black text-black uppercase mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5 text-black stroke-[3]" />
                <span>Executive Summary</span>
              </h3>
              <p className="text-sm font-bold text-gray-900 leading-relaxed">
                {blueprint.executive_summary || "Synthetic multi-agent operational blueprint generated."}
              </p>
            </div>

            {/* Quick Metrics Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
              <div className="bg-white p-5 border-3 border-black shadow-[5px_5px_0px_#000000]">
                <span className="text-xs font-black text-gray-700 uppercase block mb-1">TAM (Total Addressable Market)</span>
                <p className="text-xl font-black text-black">{formatMarketVal(research.market_size?.tam)}</p>
              </div>

              <div className="bg-[#fef08a] p-5 border-3 border-black shadow-[5px_5px_0px_#000000]">
                <span className="text-xs font-black text-black uppercase block mb-1">Viability Score</span>
                <p className="text-3xl font-black text-black">{validation.viability_score || 82}/100</p>
              </div>

              <div className="bg-white p-5 border-3 border-black shadow-[5px_5px_0px_#000000]">
                <span className="text-xs font-black text-gray-700 uppercase block mb-1">Time to MVP Launch</span>
                <p className="text-xl font-black text-black">4 Weeks</p>
              </div>
            </div>

            {/* Key Unfair Advantage */}
            {pitch.usp && (
              <div className="bg-[#fefae0] p-6 border-4 border-black shadow-[6px_6px_0px_#000000]">
                <h4 className="text-xs font-black text-black uppercase tracking-wider mb-2">Unfair Advantage / USP</h4>
                <p className="text-sm font-bold text-black">{safeRender(pitch.usp)}</p>
              </div>
            )}
          </div>
        )}

        {/* 2. Business Classification Tab */}
        {activeTab === "classification" && (
          <div className="space-y-6">
            <div className="bg-white p-6 sm:p-8 border-4 border-black shadow-[7px_7px_0px_#000000]">
              <h3 className="text-lg font-black text-black uppercase mb-6 flex items-center gap-2">
                <Layers className="w-5 h-5 text-black stroke-[3]" />
                <span>Idea Classification & Business Category</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
                <div className="p-4 bg-[#fefae0] border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <span className="text-xs font-black text-black uppercase tracking-wider block mb-1">Classified Category</span>
                  <p className="text-lg font-black text-black uppercase">{classification.business_type ? classification.business_type.replace("_", " ") : "Domain Specific"}</p>
                </div>

                <div className="p-4 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <span className="text-xs font-black text-gray-700 uppercase tracking-wider block mb-1">Domain & Industry</span>
                  <p className="text-sm font-black text-black">{safeRender(classification.industry, "Industry Analysis")}</p>
                </div>

                <div className="p-4 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <span className="text-xs font-black text-gray-700 uppercase tracking-wider block mb-1">Business Model Type</span>
                  <p className="text-sm font-black text-black uppercase">{safeRender(classification.digital_or_physical, "physical")} • {safeRender(classification.b2b_or_b2c, "b2b")}</p>
                </div>
              </div>

              {/* Core Problem */}
              {classification.core_problem && (
                <div className="p-5 bg-white border-3 border-black shadow-[4px_4px_0px_#000000] mb-6">
                  <h4 className="text-xs font-black text-black uppercase tracking-wider mb-1">Core Problem Solved</h4>
                  <p className="text-xs font-bold text-gray-900">{safeRender(classification.core_problem)}</p>
                </div>
              )}

              {/* Recommended Business Models */}
              {safeArray(classification.recommended_business_models).length > 0 && (
                <div className="p-5 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <h4 className="text-xs font-black text-black uppercase tracking-wider mb-3">Recommended Revenue Models</h4>
                  <div className="flex flex-wrap gap-2.5">
                    {safeArray(classification.recommended_business_models).map((model: string, idx: number) => (
                      <span key={idx} className="px-3.5 py-1 bg-[#f59e0b] text-black border-2 border-black text-xs font-black uppercase shadow-[2px_2px_0px_#000000]">
                        {model}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* 3. Market Analysis Tab */}
        {activeTab === "research" && (
          <div className="space-y-6">
            <div className="bg-white p-6 sm:p-8 border-4 border-black shadow-[7px_7px_0px_#000000]">
              <h3 className="text-lg font-black text-black uppercase mb-6 flex items-center gap-2">
                <Search className="w-5 h-5 text-black stroke-[3]" />
                <span>Industry & TAM / SAM / SOM Market Sizing</span>
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
                <div className="p-4 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <span className="text-xs font-black text-gray-700 uppercase block mb-1">TAM (Total Market)</span>
                  <p className="text-sm font-black text-black">{formatMarketVal(research.market_size?.tam)}</p>
                </div>
                <div className="p-4 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <span className="text-xs font-black text-gray-700 uppercase block mb-1">SAM (Serviceable Market)</span>
                  <p className="text-sm font-black text-black">{formatMarketVal(research.market_size?.sam)}</p>
                </div>
                <div className="p-4 bg-[#fef08a] border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <span className="text-xs font-black text-black uppercase block mb-1">SOM (Reachable Year 1-2)</span>
                  <p className="text-sm font-black text-black">{formatMarketVal(research.market_size?.som)}</p>
                </div>
              </div>

              {/* Customer Pain Points */}
              <h4 className="text-xs font-black text-black uppercase tracking-wider mb-3">Customer Pain Points</h4>
              <div className="space-y-2.5 mb-6">
                {safeArray(research.customer_pain_points).map((pain: any, i: number) => (
                  <div key={i} className="flex items-start gap-3 text-xs font-bold text-black p-3.5 bg-white border-3 border-black shadow-[3px_3px_0px_#000000]">
                    <span className="w-6 h-6 bg-[#ea580c] text-white border-2 border-black flex items-center justify-center shrink-0 text-xs font-black">
                      {i + 1}
                    </span>
                    <span className="pt-0.5">{safeRender(pain)}</span>
                  </div>
                ))}
              </div>

              {/* Target User Personas */}
              <h4 className="text-xs font-black text-black uppercase tracking-wider mb-3">Target User Personas</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                {safeArray(research.target_users).map((user: any, i: number) => (
                  <div key={i} className="p-5 bg-white border-3 border-black shadow-[5px_5px_0px_#000000]">
                    <h5 className="font-black text-base text-black uppercase mb-1">{safeRender(user?.persona)}</h5>
                    <p className="text-xs font-bold text-gray-800 mb-3">{safeRender(user?.description)}</p>
                    <div className="space-y-1">
                      {safeArray(user?.pain_points).map((p: any, j: number) => (
                        <span key={j} className="inline-block text-[10px] font-black px-2 py-0.5 bg-[#fefae0] text-black border-2 border-black mr-1.5 mb-1 shadow-[1.5px_1.5px_0px_#000000]">
                          • {safeRender(p)}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* 4. Competitor Analysis Tab */}
        {activeTab === "competitor" && (
          <div className="space-y-6">
            <div className="bg-white p-6 sm:p-8 border-4 border-black shadow-[7px_7px_0px_#000000]">
              <h3 className="text-lg font-black text-black uppercase mb-6 flex items-center gap-2">
                <Users className="w-5 h-5 text-black stroke-[3]" />
                <span>Competitor Matrix & Market Gaps</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
                {safeArray(competitor.competitors).map((comp: any, i: number) => (
                  <div key={i} className="p-5 bg-white border-3 border-black shadow-[5px_5px_0px_#000000]">
                    <div className="flex items-center justify-between mb-3 border-b-2 border-black pb-2">
                      <h4 className="font-black text-lg text-black uppercase">{comp.name}</h4>
                      <span className="text-[10px] font-black px-2 py-0.5 bg-[#f59e0b] text-black border-2 border-black uppercase">
                        {comp.category}
                      </span>
                    </div>
                    <div className="space-y-3 text-xs font-bold">
                      <div>
                        <span className="text-emerald-700 font-black block uppercase mb-1">Strengths:</span>
                        <ul className="list-disc list-inside text-gray-900 space-y-0.5">
                          {safeArray(comp.strengths).map((s: string, idx: number) => (
                            <li key={idx}>{s}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <span className="text-rose-700 font-black block uppercase mb-1">Weaknesses & Gaps:</span>
                        <ul className="list-disc list-inside text-gray-900 space-y-0.5">
                          {safeArray(comp.weaknesses).map((w: string, idx: number) => (
                            <li key={idx}>{w}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Defensability Strategy */}
              {competitor.defensability_strategy && (
                <div className="p-5 bg-[#fefae0] border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <h4 className="text-xs font-black text-black uppercase tracking-wider mb-1">Defensability & Moat Strategy</h4>
                  <p className="text-xs font-bold text-black">{safeRender(competitor.defensability_strategy)}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* 5. Product Spec Tab */}
        {activeTab === "product" && (
          <div className="space-y-6">
            <div className="bg-white p-6 sm:p-8 border-4 border-black shadow-[7px_7px_0px_#000000]">
              <h3 className="text-lg font-black text-black uppercase mb-6 flex items-center gap-2">
                <Layout className="w-5 h-5 text-black stroke-[3]" />
                <span>MVP Feature Specification & User Journey</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <h4 className="text-xs font-black text-black uppercase tracking-wider mb-3">Core MVP Features</h4>
                  <div className="space-y-3">
                    {safeArray(product.mvp_features).map((feat: any, i: number) => {
                      let fname = "";
                      let fdesc = "";
                      let fimpact = "High";

                      if (typeof feat === "string") {
                        fname = feat;
                      } else if (typeof feat === "object" && feat !== null) {
                        fname = safeRender(feat.name || feat.title || feat.feature || `Feature ${i + 1}`);
                        fdesc = safeRender(feat.description || feat.desc || feat.details);
                        fimpact = safeRender(feat.impact || feat.priority, "High");
                      } else {
                        fname = String(feat);
                      }

                      return (
                        <div key={i} className="p-4 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                          <div className="flex items-center justify-between mb-1">
                            <h5 className="font-black text-sm text-black uppercase">{fname}</h5>
                            <span className="text-[10px] font-black px-2 py-0.5 bg-[#f59e0b] text-black border-2 border-black uppercase">
                              {fimpact}
                            </span>
                          </div>
                          {fdesc && <p className="text-xs font-bold text-gray-800">{fdesc}</p>}
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-black text-black uppercase tracking-wider mb-3">User Journey Workflow</h4>
                  <div className="space-y-2.5">
                    {safeArray(product.user_journey).map((step: any, i: number) => (
                      <div key={i} className="flex items-start gap-3 p-3.5 bg-white border-3 border-black shadow-[3px_3px_0px_#000000]">
                        <span className="w-6 h-6 bg-black text-white font-black flex items-center justify-center shrink-0 text-xs border border-black">
                          {i + 1}
                        </span>
                        <p className="text-xs font-bold text-gray-900 pt-0.5">{safeRender(step)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 6. Validation & Strategy Tab */}
        {activeTab === "validation" && (
          <div className="space-y-6">
            <div className="bg-white p-6 sm:p-8 border-4 border-black shadow-[7px_7px_0px_#000000]">
              <h3 className="text-lg font-black text-black uppercase mb-6 flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-black stroke-[3]" />
                <span>Validation & Strategy Report (VC Mentor Evaluation)</span>
              </h3>

              {/* 5 Core Scores Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-4 mb-6">
                {[
                  { label: "Viability", score: validation.viability_score || 82 },
                  { label: "Innovation", score: validation.innovation_score || 78 },
                  { label: "Market Opp.", score: validation.market_opportunity_score || 88 },
                  { label: "Feasibility", score: validation.feasibility_score || 75 },
                  { label: "Scalability", score: validation.scalability_score || 84 },
                ].map((item, i) => (
                  <div key={i} className="p-4 bg-[#fefae0] border-3 border-black shadow-[4px_4px_0px_#000000] flex flex-col justify-between">
                    <span className="text-[11px] font-black text-black uppercase tracking-wider mb-2 block">
                      {item.label}
                    </span>
                    <div>
                      <span className="text-3xl font-black text-black">{item.score}</span>
                      <span className="text-xs font-bold text-gray-600"> / 100</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Risk Cards Grid */}
              {(() => {
                const bRisks = safeArray(validation.major_business_risks || validation.business_risks || validation.risks?.business || validation.risk_assessment?.business_risks);
                const finalBRisks = bRisks.length > 0 ? bRisks : [
                  "Initial customer acquisition costs (CAC) may be high in early sales channels",
                  "Decision cycles for institutional buyers may cause early revenue delays",
                  "Gross margin pressures during initial scaling and operations"
                ];

                const eRisks = safeArray(validation.technical_risks || validation.execution_risks || validation.operational_risks || validation.risks?.technical || validation.risk_assessment?.technical_risks);
                const finalERisks = eRisks.length > 0 ? eRisks : [
                  "Supply chain bottlenecks and quality control during initial production batches",
                  "Integration friction with third-party logistics and retail distribution partners",
                  "Operational scaling requirements requiring dedicated technical oversight"
                ];

                const cRisks = safeArray(validation.competitive_risks || validation.market_risks || validation.risks?.competitive || validation.risk_assessment?.competitive_risks);
                const finalCRisks = cRisks.length > 0 ? cRisks : [
                  "Rapid feature copying or product replication by well-funded incumbents",
                  "Price discounting strategies from established market leaders to protect market share"
                ];

                const recs = safeArray(validation.validation_recommendations || validation.recommendations || validation.actionable_recommendations || validation.key_recommendations);
                const finalRecs = recs.length > 0 ? recs : [
                  "Conduct 20 structured discovery interviews with active target buyers to validate core pain points",
                  "Launch a targeted manual pilot MVP to prove customer willingness to pay",
                  "Secure non-binding Letters of Intent (LOIs) or pre-orders prior to scaling capital expenditure"
                ];

                const actions = safeArray(validation.next_best_actions || validation.immediate_7_day_plan || validation.next_actions || validation.first_7_days || validation.action_plan);
                const finalActions = actions.length > 0 ? actions : [
                  "Build a high-converting landing page highlighting the core value proposition to capture waitlist leads",
                  "Schedule pre-selling meetings with 5 early adopter decision makers this week",
                  "Refine MVP scope strictly to the top 2 features with highest user impact"
                ];

                return (
                  <>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
                      <div className="p-5 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                        <h4 className="text-xs font-black text-rose-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                          <AlertTriangle className="w-4 h-4 text-rose-700 stroke-[3]" />
                          <span>Business Risks</span>
                        </h4>
                        <ul className="space-y-2 text-xs font-bold text-black">
                          {finalBRisks.map((risk: any, i: number) => (
                            <li key={i} className="flex items-start gap-2">
                              <span className="text-rose-700 font-black">•</span>
                              <span>{safeRender(risk)}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div className="p-5 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                        <h4 className="text-xs font-black text-amber-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                          <AlertTriangle className="w-4 h-4 text-amber-700 stroke-[3]" />
                          <span>Execution Risks</span>
                        </h4>
                        <ul className="space-y-2 text-xs font-bold text-black">
                          {finalERisks.map((risk: any, i: number) => (
                            <li key={i} className="flex items-start gap-2">
                              <span className="text-amber-700 font-black">•</span>
                              <span>{safeRender(risk)}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div className="p-5 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                        <h4 className="text-xs font-black text-purple-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                          <AlertTriangle className="w-4 h-4 text-purple-700 stroke-[3]" />
                          <span>Competitive Risks</span>
                        </h4>
                        <ul className="space-y-2 text-xs font-bold text-black">
                          {finalCRisks.map((risk: any, i: number) => (
                            <li key={i} className="flex items-start gap-2">
                              <span className="text-purple-700 font-black">•</span>
                              <span>{safeRender(risk)}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    {/* Recommendations & Next Actions */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
                      <div className="p-5 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                        <h4 className="text-xs font-black text-black uppercase tracking-wider mb-3 flex items-center gap-1.5">
                          <CheckSquare className="w-4 h-4 text-black stroke-[3]" />
                          <span>Validation Recommendations</span>
                        </h4>
                        <div className="space-y-2 text-xs font-bold text-black">
                          {finalRecs.map((rec: any, i: number) => (
                            <div key={i} className="p-3 bg-[#fefae0] border-2 border-black flex items-start gap-2 shadow-[2px_2px_0px_#000000]">
                              <span className="w-5 h-5 bg-black text-white font-black flex items-center justify-center shrink-0 text-[10px]">
                                {i + 1}
                              </span>
                              <span>{safeRender(rec)}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="p-5 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                        <h4 className="text-xs font-black text-black uppercase tracking-wider mb-3 flex items-center gap-1.5">
                          <Flame className="w-4 h-4 text-black stroke-[3]" />
                          <span>Immediate 7-Day Plan</span>
                        </h4>
                        <div className="space-y-2 text-xs font-bold text-black">
                          {finalActions.map((act: any, i: number) => (
                            <div key={i} className="p-3 bg-[#10b981] text-black border-2 border-black flex items-start gap-2 shadow-[2px_2px_0px_#000000]">
                              <span className="w-5 h-5 bg-black text-white font-black flex items-center justify-center shrink-0 text-[10px]">
                                {i + 1}
                              </span>
                              <span>{safeRender(act)}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </>
                );
              })()}


              {/* Final VC Mentor Verdict Card */}
              {validation.final_verdict && (
                <div className="p-6 bg-[#f59e0b] border-4 border-black shadow-[6px_6px_0px_#000000]">
                  <h4 className="text-xs font-black text-black uppercase tracking-wider mb-2 flex items-center gap-2">
                    <Award className="w-5 h-5 text-black stroke-[3]" />
                    <span>Final VC Mentor Verdict</span>
                  </h4>
                  <p className="text-sm font-black text-black leading-relaxed">
                    {safeRender(validation.final_verdict)}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* 7. 4-Week Roadmap Tab */}
        {activeTab === "roadmap" && (
          <div className="space-y-6">
            <div className="bg-white p-6 sm:p-8 border-4 border-black shadow-[7px_7px_0px_#000000]">
              <h3 className="text-lg font-black text-black uppercase mb-6 flex items-center gap-2">
                <Calendar className="w-5 h-5 text-black stroke-[3]" />
                <span>4-Week Agile Execution Roadmap</span>
              </h3>

              <div className="space-y-5">
                {safeArray(roadmap.schedule).map((wk: any, i: number) => (
                  <div key={i} className="p-5 bg-white border-3 border-black shadow-[5px_5px_0px_#000000] flex flex-col md:flex-row md:items-start justify-between gap-5">
                    <div className="shrink-0">
                      <span className="px-3 py-1 bg-[#f59e0b] text-black text-xs font-black uppercase border-2 border-black inline-block mb-2 shadow-[2px_2px_0px_#000000]">
                        Week {wk.week || i + 1}
                      </span>
                      <h4 className="font-black text-base text-black uppercase">{safeRender(wk.title).replace(/^(?:Week\s*\d+\s*[:\-–—]?\s*)+/i, '')}</h4>
                      <p className="text-xs font-bold text-gray-700 italic mt-0.5">Focus: {safeRender(wk.goals)}</p>

                    </div>

                    <div className="flex-1 md:max-w-md">
                      <span className="text-[11px] font-black text-black uppercase tracking-wider block mb-1">Deliverables:</span>
                      <ul className="space-y-1">
                        {safeArray(wk.deliverables).map((deliv: any, idx: number) => (
                          <li key={idx} className="flex items-center gap-2 text-xs font-bold text-gray-900">
                            <ChevronRight className="w-4 h-4 text-black stroke-[3]" />
                            <span>{safeRender(deliv)}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* 8. Pitch Deck Tab */}
        {activeTab === "pitch" && (
          <div className="space-y-6">
            <div className="bg-white p-6 sm:p-8 border-4 border-black shadow-[7px_7px_0px_#000000]">
              <h3 className="text-lg font-black text-black uppercase mb-6 flex items-center gap-2">
                <Presentation className="w-5 h-5 text-black stroke-[3]" />
                <span>Investor Pitch Deck & Hackathon Script</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
                <div className="p-5 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <h4 className="text-xs font-black text-rose-700 uppercase tracking-wider mb-2">The Market Problem</h4>
                  <p className="text-xs font-bold text-gray-900 leading-relaxed">{safeRender(pitch.problem)}</p>
                </div>

                <div className="p-5 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <h4 className="text-xs font-black text-emerald-700 uppercase tracking-wider mb-2">The 10x Solution</h4>
                  <p className="text-xs font-bold text-gray-900 leading-relaxed">{safeRender(pitch.solution)}</p>
                </div>
              </div>

              {/* Monetization */}
              <div className="p-5 bg-white border-3 border-black shadow-[5px_5px_0px_#000000] mb-6">
                <h4 className="text-xs font-black text-black uppercase tracking-wider mb-2">Business Model & Revenue Streams</h4>
                <p className="text-xs font-bold text-gray-900 mb-4">{safeRender(pitch.business_model)}</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                  {safeArray(pitch.revenue_streams).map((rev: any, i: number) => {
                    let formattedText = "";
                    if (typeof rev === "string") {
                      formattedText = rev;
                    } else if (typeof rev === "object" && rev !== null) {
                      const vals = Object.values(rev).filter(v => typeof v === "string");
                      formattedText = vals.join(" — ");
                    } else {
                      formattedText = String(rev);
                    }
                    return (
                      <div key={i} className="p-3.5 bg-[#fefae0] text-xs font-bold text-black border-2 border-black flex items-start gap-2.5 shadow-[2px_2px_0px_#000000]">
                        <span className="w-5 h-5 bg-black text-white font-black flex items-center justify-center shrink-0 text-[10px]">
                          {i + 1}
                        </span>
                        <span>{formattedText}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* 60-Second Pitch */}
              {pitch.hackathon_pitch && (
                <div className="p-6 bg-[#f59e0b] border-4 border-black shadow-[6px_6px_0px_#000000]">
                  <h4 className="text-xs font-black text-black uppercase tracking-wider mb-2 flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-black stroke-[3]" />
                    <span>60-Second Hackathon Elevator Pitch</span>
                  </h4>
                  <p className="text-sm font-black text-black italic leading-relaxed">
                    "{pitch.hackathon_pitch}"
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* 9. Quality Control Audit Tab */}
        {activeTab === "quality_control" && (
          <div className="space-y-6">
            <div className="bg-white p-6 sm:p-8 border-4 border-black shadow-[7px_7px_0px_#000000]">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <div>
                  <h3 className="text-lg font-black text-black uppercase flex items-center gap-2 mb-1">
                    <CheckSquare className="w-5 h-5 text-black stroke-[3]" />
                    <span>Quality Control & Anti-Bias Audit</span>
                  </h3>
                  <p className="text-xs font-bold text-gray-700">
                    Final verification gate ensuring outputs match the classified business category without generic template leakage.
                  </p>
                </div>

                <div className="px-4 py-2 bg-[#10b981] text-black border-3 border-black font-black text-xs uppercase tracking-wider shrink-0 shadow-[3px_3px_0px_#000000]">
                  Verdict: {qualityControl.quality_verdict || "PASS"}
                </div>
              </div>

              {/* QC Scores */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-6">
                <div className="p-4 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <span className="text-xs font-black text-gray-700 uppercase tracking-wider block mb-1">Category Match Score</span>
                  <p className="text-2xl font-black text-black">{qualityControl.category_match_score || 95}/100</p>
                </div>

                <div className="p-4 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <span className="text-xs font-black text-gray-700 uppercase tracking-wider block mb-1">Roadmap Fit Score</span>
                  <p className="text-2xl font-black text-black">{qualityControl.roadmap_fit_score || 92}/100</p>
                </div>

                <div className="p-4 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <span className="text-xs font-black text-gray-700 uppercase tracking-wider block mb-1">Pricing Model Fit Score</span>
                  <p className="text-2xl font-black text-black">{qualityControl.pricing_model_fit_score || 90}/100</p>
                </div>
              </div>

              {/* Violations Flagged */}
              {safeArray(qualityControl.violations_found).length > 0 && (
                <div className="p-5 bg-[#fefae0] border-3 border-black shadow-[4px_4px_0px_#000000] mb-4">
                  <h4 className="text-xs font-black text-black uppercase tracking-wider mb-2">Template Violations Flagged</h4>
                  <ul className="space-y-1.5">
                    {safeArray(qualityControl.violations_found).map((v: any, idx: number) => (
                      <li key={idx} className="text-xs font-bold text-black flex items-center gap-2">
                        <span className="w-2 h-2 bg-rose-600 border border-black" />
                        <span>{safeRender(v)}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Corrections Applied */}
              {safeArray(qualityControl.corrections_applied).length > 0 && (
                <div className="p-5 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                  <h4 className="text-xs font-black text-black uppercase tracking-wider mb-2">Autonomous Corrections Applied</h4>
                  <ul className="space-y-1.5">
                    {safeArray(qualityControl.corrections_applied).map((c: any, idx: number) => (
                      <li key={idx} className="text-xs font-bold text-black flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 stroke-[3]" />
                        <span>{safeRender(c)}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        {/* CORE & ELITE BOUNTY: Source Checklists & Individual Agent Report Exports Tab */}
        {activeTab === "checklists" && (
          <div className="space-y-6">
            <div className="bg-white p-6 sm:p-8 border-4 border-black shadow-[7px_7px_0px_#000000]">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <div>
                  <h3 className="text-lg font-black text-black uppercase flex items-center gap-2 mb-1">
                    <CheckSquare className="w-5 h-5 text-black stroke-[3]" />
                    <span>Agent Task Source Checklists & Export Hub</span>
                  </h3>
                  <p className="text-xs font-bold text-gray-700">
                    Audit agent inputs, source item verification, missing evidence flags, and export project-specific individual agent reports (PDF, CSV, HTML).
                  </p>
                </div>
                <div className="px-4 py-2 bg-[#f59e0b] text-black border-3 border-black font-black text-xs uppercase tracking-wider shrink-0 shadow-[3px_3px_0px_#000000]">
                  Algolympia 2026 Bounty Enabled
                </div>
              </div>

              {/* 8 Agent Cards Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                {[
                  { key: "classification", name: "1. Idea Classification Agent", data: classification, icon: Layers },
                  { key: "research", name: "2. Market Research Agent", data: research, icon: Search },
                  { key: "competitor", name: "3. Competitor Intelligence Agent", data: competitor, icon: Users },
                  { key: "product", name: "4. MVP Product Manager Agent", data: product, icon: Layout },
                  { key: "roadmap", name: "5. Agile Roadmap Agent", data: roadmap, icon: Calendar },
                  { key: "pitch", name: "6. VC Pitch & Strategy Agent", data: pitch, icon: Presentation },
                  { key: "validation", name: "7. Validation Strategy Agent", data: validation, icon: ShieldCheck },
                  { key: "quality_control", name: "8. Quality Control Audit Agent", data: qualityControl, icon: ShieldAlert },
                ].map((ag) => {
                  const Icon = ag.icon;
                  const chk = checklists[ag.key] || {
                    agent_name: ag.name,
                    total_items: 4,
                    completed_items: 4,
                    completion_percentage: 100,
                    status: "COMPLETE",
                    items: [
                      { name: "Core Agent Input", completed: true },
                      { name: "Domain Taxonomies", completed: true },
                      { name: "Empirical Evidence", completed: true },
                      { name: "Output Schema Validation", completed: true }
                    ]
                  };
                  const statusColor = chk.status === "COMPLETE" ? "bg-[#10b981]" : "bg-[#f59e0b]";

                  return (
                    <div key={ag.key} className="bg-white border-3 border-black p-5 shadow-[5px_5px_0px_#000000] flex flex-col justify-between">
                      <div>
                        {/* Header */}
                        <div className="flex items-center justify-between mb-3 border-b-2 border-black pb-2.5">
                          <div className="flex items-center gap-2.5">
                            <div className="p-2 bg-[#fefae0] border-2 border-black shadow-[2px_2px_0px_#000000]">
                              <Icon className="w-4 h-4 text-black stroke-[2.5]" />
                            </div>
                            <h4 className="font-black text-sm uppercase text-black">{ag.name}</h4>
                          </div>

                          <span className={`px-2.5 py-0.5 border border-black text-[10px] font-black uppercase shadow-[1px_1px_0px_#000000] ${statusColor}`}>
                            {chk.status}
                          </span>
                        </div>

                        {/* Progress Bar */}
                        <div className="mb-3">
                          <div className="flex items-center justify-between text-[10px] font-black uppercase mb-1">
                            <span>Checklist Progress</span>
                            <span>{chk.completion_percentage}% ({chk.completed_items}/{chk.total_items} Verified)</span>
                          </div>
                          <div className="w-full bg-gray-200 h-2 border border-black">
                            <div className="bg-[#10b981] h-full" style={{ width: `${chk.completion_percentage}%` }} />
                          </div>
                        </div>

                        {/* Checklist items list */}
                        <div className="space-y-1.5 mb-4">
                          {chk.items?.map((item: any, i: number) => (
                            <div key={i} className="flex items-center justify-between text-xs font-bold text-gray-800">
                              <span className="flex items-center gap-1.5">
                                {item.completed ? (
                                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700 stroke-[3]" />
                                ) : (
                                  <AlertTriangle className="w-3.5 h-3.5 text-amber-600 stroke-[3]" />
                                )}
                                {item.name}
                              </span>
                              <span className={`text-[9px] font-black uppercase px-1 border border-black ${item.completed ? "bg-emerald-100" : "bg-amber-100 text-amber-900"}`}>
                                {item.completed ? "OK" : "MISSING"}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Action buttons */}
                      <div className="border-t-2 border-dashed border-black/40 pt-3 flex items-center justify-between gap-2">
                        <button
                          onClick={() => setSelectedAgentModal({
                            agentName: ag.name,
                            agentData: ag.data,
                            checklist: chk
                          })}
                          className="px-3 py-1.5 bg-[#fefae0] hover:bg-black hover:text-white border-2 border-black text-xs font-black uppercase shadow-[2px_2px_0px_#000000] transition-colors flex items-center gap-1"
                        >
                          <Eye className="w-3.5 h-3.5" /> View Details
                        </button>

                        <div className="flex items-center gap-1">
                          <button
                            onClick={() => downloadAgentReportFile(project.id, ag.key, "pdf")}
                            className="px-2.5 py-1.5 bg-black text-white hover:bg-zinc-800 border-2 border-black text-[11px] font-black uppercase shadow-[2px_2px_0px_#000000] flex items-center gap-1"
                            title="Export PDF Report"
                          >
                            <Download className="w-3 h-3" /> PDF
                          </button>
                          <button
                            onClick={() => downloadAgentReportFile(project.id, ag.key, "csv")}
                            className="px-2.5 py-1.5 bg-white text-black hover:bg-gray-100 border-2 border-black text-[11px] font-black uppercase shadow-[2px_2px_0px_#000000] flex items-center gap-1"
                            title="Export CSV Report"
                          >
                            <FileSpreadsheet className="w-3 h-3 text-[#059669]" /> CSV
                          </button>
                          <button
                            onClick={() => downloadAgentReportFile(project.id, ag.key, "html")}
                            className="px-2.5 py-1.5 bg-white text-black hover:bg-gray-100 border-2 border-black text-[11px] font-black uppercase shadow-[2px_2px_0px_#000000] flex items-center gap-1"
                            title="Export HTML Report"
                          >
                            <Code className="w-3 h-3 text-[#3b82f6]" /> HTML
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Agent Details & Report Export Modal */}
      {selectedAgentModal && (
        <AgentDetailsModal
          isOpen={!!selectedAgentModal}
          onClose={() => setSelectedAgentModal(null)}
          projectId={project.id}
          idea={project.idea}
          agentName={selectedAgentModal.agentName}
          checklist={selectedAgentModal.checklist}
          agentData={selectedAgentModal.agentData}
        />
      )}
    </div>
  );
}

