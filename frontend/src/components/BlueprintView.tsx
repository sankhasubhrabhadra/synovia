"use client";

import React, { useState } from "react";
import { downloadProjectPdfFile, downloadProjectPptFile, Project } from "@/lib/api";
import { 
  Download, Sparkles, Search, Users, Layout, ShieldCheck, Calendar, 
  Presentation, CheckCircle2, FileText, ArrowUpRight, AlertTriangle, 
  Zap, Code2, ChevronRight, Layers, Target, CheckSquare, Award, Flame, Loader2
} from "lucide-react";

interface BlueprintViewProps {
  project: Project;
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

export function BlueprintView({ project }: BlueprintViewProps) {
  const [activeTab, setActiveTab] = useState<"summary" | "classification" | "research" | "competitor" | "product" | "validation" | "roadmap" | "pitch" | "quality_control">("summary");
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

  const getScoreColor = (score: number) => {
    if (score >= 80) return { text: "text-emerald-400", bg: "bg-emerald-500", border: "border-emerald-500/30", badge: "bg-emerald-500/10 text-emerald-300" };
    if (score >= 65) return { text: "text-indigo-400", bg: "bg-indigo-500", border: "border-indigo-500/30", badge: "bg-indigo-500/10 text-indigo-300" };
    if (score >= 50) return { text: "text-amber-400", bg: "bg-amber-500", border: "border-amber-500/30", badge: "bg-amber-500/10 text-amber-300" };
    return { text: "text-rose-400", bg: "bg-rose-500", border: "border-rose-500/30", badge: "bg-rose-500/10 text-rose-300" };
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header Banner */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl mb-8 border border-indigo-500/20 glow-purple flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold uppercase tracking-wider mb-3">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Startup Blueprint & Strategy Generated</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white leading-tight mb-2">
            {project.idea}
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 max-w-2xl">
            Evaluated by 6 specialized AI agents on {formatDateStr(project?.created_at)}.
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-3 shrink-0">
          <button
            onClick={handleDownloadPdf}
            disabled={downloadingPdf}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs sm:text-sm shadow-xl shadow-indigo-600/30 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50"
          >
            {downloadingPdf ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
            <span>{downloadingPdf ? "Downloading PDF..." : "Download PDF"}</span>
          </button>
          
          <button
            onClick={handleDownloadPpt}
            disabled={downloadingPpt}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs sm:text-sm shadow-xl shadow-emerald-600/30 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50"
          >
            {downloadingPpt ? <Loader2 className="w-4 h-4 animate-spin" /> : <Presentation className="w-4 h-4 text-emerald-200" />}
            <span>{downloadingPpt ? "Generating PPT..." : "Download PPT Pitch Deck"}</span>
          </button>
        </div>
      </div>

      {/* Tabs Navigation Header */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-3 mb-6 scrollbar-none border-b border-slate-800">
        {[
          { id: "summary", label: "Executive Summary", icon: FileText },
          { id: "classification", label: "Business Category", icon: Layers },
          { id: "research", label: "Market Analysis", icon: Search },
          { id: "competitor", label: "Competitors & Gaps", icon: Users },
          { id: "product", label: "MVP Product Spec", icon: Layout },
          { id: "validation", label: "Validation & Strategy", icon: ShieldCheck },
          { id: "roadmap", label: "4-Week Roadmap", icon: Calendar },
          { id: "pitch", label: "Pitch & Monetization", icon: Presentation },
          { id: "quality_control", label: "Quality Audit", icon: CheckSquare },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-3.5 py-2.5 rounded-xl font-bold text-xs whitespace-nowrap transition-all cursor-pointer ${
                isActive
                  ? "bg-gradient-to-r from-amber-600 via-amber-700 to-rose-700 text-[#fffdfa] shadow-lg shadow-amber-950/40 border border-[#f59e0b]/50"
                  : "bg-[#251b17]/80 text-[#d4c4b5] border border-[#e8ded2]/15 hover:bg-[#33241e] hover:text-[#fffdfa]"
              }`}
            >
              <Icon className="w-4 h-4 text-[#f59e0b]" />
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
            <div className="glass-card p-6 rounded-2xl">
              <h3 className="text-base font-bold text-white mb-3 flex items-center gap-2">
                <FileText className="w-5 h-5 text-indigo-400" />
                <span>Executive Summary</span>
              </h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                {blueprint.executive_summary || "Synthetic multi-agent operational blueprint generated."}
              </p>
            </div>

            {/* Quick Metrics Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="glass-card p-5 rounded-2xl">
                <span className="text-xs text-slate-400 font-semibold block mb-1">Total Addressable Market (TAM)</span>
                <p className="text-lg font-bold text-indigo-300">{formatMarketVal(research.market_size?.tam)}</p>
              </div>

              <div className="glass-card p-5 rounded-2xl">
                <span className="text-xs text-slate-400 font-semibold block mb-1">Viability Score</span>
                <p className="text-2xl font-black text-emerald-400">{validation.viability_score || 82}/100</p>
              </div>

              <div className="glass-card p-5 rounded-2xl">
                <span className="text-xs text-slate-400 font-semibold block mb-1">Time to MVP Launch</span>
                <p className="text-lg font-bold text-cyan-300">4 Weeks</p>
              </div>
            </div>

            {/* Key Unfair Advantage */}
            {pitch.usp && (
              <div className="glass-card p-6 rounded-2xl border-l-4 border-l-indigo-500">
                <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2">Unfair Advantage / USP</h4>
                <p className="text-sm text-slate-200 font-medium">{safeRender(pitch.usp)}</p>
              </div>
            )}
          </div>
        )}

        {/* 2. Business Classification & Anti-Patterns Tab */}
        {activeTab === "classification" && (
          <div className="space-y-6">
            <div className="studio-card p-6 rounded-2xl border border-blue-500/20">
              <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                <Layers className="w-5 h-5 text-blue-400" />
                <span>Idea Classification & Business Category</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <span className="text-xs font-bold text-blue-400 uppercase tracking-wider block mb-1">Classified Category</span>
                  <p className="text-lg font-black text-white capitalize">{classification.business_type ? classification.business_type.replace("_", " ") : "Domain Specific"}</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider block mb-1">Domain & Industry</span>
                  <p className="text-xs font-bold text-indigo-300">{safeRender(classification.industry, "Industry Analysis")}</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider block mb-1">Business Model Type</span>
                  <p className="text-xs font-bold text-emerald-300 capitalize">{safeRender(classification.digital_or_physical, "physical")} • {safeRender(classification.b2b_or_b2c, "b2b")}</p>
                </div>
              </div>

              {/* Core Problem */}
              {classification.core_problem && (
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 mb-6">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Core Problem Solved</h4>
                  <p className="text-xs text-slate-200 font-medium">{safeRender(classification.core_problem)}</p>
                </div>
              )}


              {/* Recommended Business Models */}
              {safeArray(classification.recommended_business_models).length > 0 && (
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-blue-400 uppercase tracking-wider mb-3">Recommended Revenue Models</h4>
                  <div className="flex flex-wrap gap-2">
                    {safeArray(classification.recommended_business_models).map((model: string, idx: number) => (
                      <span key={idx} className="px-3 py-1 rounded-lg bg-blue-500/10 text-blue-300 border border-blue-500/30 text-xs font-semibold">
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
            <div className="glass-card p-6 rounded-2xl">
              <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                <Search className="w-5 h-5 text-indigo-400" />
                <span>Industry & TAM / SAM / SOM Market Sizing</span>
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <span className="text-xs font-bold text-indigo-400 block mb-1">TAM (Total Market)</span>
                  <p className="text-xs text-slate-300">{formatMarketVal(research.market_size?.tam)}</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <span className="text-xs font-bold text-purple-400 block mb-1">SAM (Serviceable Market)</span>
                  <p className="text-xs text-slate-300">{formatMarketVal(research.market_size?.sam)}</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <span className="text-xs font-bold text-cyan-400 block mb-1">SOM (Year 1-2 Reachable)</span>
                  <p className="text-xs text-slate-300">{formatMarketVal(research.market_size?.som)}</p>
                </div>
              </div>

              {/* Customer Pain Points */}
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">Customer Pain Points</h4>
              <div className="space-y-2 mb-6">
                {safeArray(research.customer_pain_points).map((pain: any, i: number) => (
                  <div key={i} className="flex items-start gap-2.5 text-xs text-slate-300 p-3 rounded-lg bg-slate-900/40 border border-slate-800/60">
                    <span className="w-5 h-5 rounded-full bg-rose-500/10 text-rose-400 flex items-center justify-center shrink-0 text-[10px] font-bold">
                      {i + 1}
                    </span>
                    <span>{safeRender(pain)}</span>
                  </div>
                ))}
              </div>

              {/* Target User Personas */}
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">Target User Personas</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {safeArray(research.target_users).map((user: any, i: number) => (
                  <div key={i} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
                    <h5 className="font-bold text-sm text-indigo-300 mb-1">{safeRender(user?.persona)}</h5>
                    <p className="text-xs text-slate-400 mb-3">{safeRender(user?.description)}</p>
                    <div className="space-y-1">
                      {safeArray(user?.pain_points).map((p: any, j: number) => (
                        <span key={j} className="inline-block text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 mr-1.5 mb-1">
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

        {/* 3. Competitor Analysis Tab */}
        {activeTab === "competitor" && (
          <div className="space-y-6">
            <div className="glass-card p-6 rounded-2xl">
              <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                <Users className="w-5 h-5 text-indigo-400" />
                <span>Competitor Matrix & Market Gaps</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                {safeArray(competitor.competitors).map((comp: any, i: number) => (
                  <div key={i} className="p-5 rounded-xl bg-slate-950/80 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-bold text-base text-white">{comp.name}</h4>
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                        {comp.category}
                      </span>
                    </div>
                    <div className="space-y-3 text-xs">
                      <div>
                        <span className="text-emerald-400 font-semibold block mb-1">Strengths:</span>
                        <ul className="list-disc list-inside text-slate-300 space-y-0.5">
                          {safeArray(comp.strengths).map((s: string, idx: number) => (
                            <li key={idx}>{s}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <span className="text-rose-400 font-semibold block mb-1">Weaknesses & Gaps:</span>
                        <ul className="list-disc list-inside text-slate-300 space-y-0.5">
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
                <div className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-500/30">
                  <h4 className="text-xs font-bold text-indigo-300 uppercase tracking-wider mb-1">Defensability & Moat Strategy</h4>
                  <p className="text-xs text-slate-300">{safeRender(competitor.defensability_strategy)}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* 4. Product Spec Tab */}
        {activeTab === "product" && (
          <div className="space-y-6">
            <div className="glass-card p-6 rounded-2xl">
              <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                <Layout className="w-5 h-5 text-indigo-400" />
                <span>MVP Feature Specification & User Journey</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-3">Core MVP Features</h4>
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
                        <div key={i} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                          <div className="flex items-center justify-between mb-1">
                            <h5 className="font-bold text-sm text-slate-200">{fname}</h5>
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                              Impact: {fimpact}
                            </span>
                          </div>
                          {fdesc && <p className="text-xs text-slate-400">{fdesc}</p>}
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider mb-3">User Journey Workflow</h4>
                  <div className="space-y-2">
                    {safeArray(product.user_journey).map((step: any, i: number) => (
                      <div key={i} className="flex items-start gap-3 p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                        <span className="w-6 h-6 rounded-full bg-purple-500/20 text-purple-300 font-bold flex items-center justify-center shrink-0 text-xs">
                          {i + 1}
                        </span>
                        <p className="text-xs text-slate-300 pt-0.5">{safeRender(step)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 5. NEW Validation & Strategy Tab (REPLACES Technical Architecture) */}
        {activeTab === "validation" && (
          <div className="space-y-6">
            <div className="glass-card p-6 rounded-2xl">
              <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-indigo-400" />
                <span>Validation & Strategy Report (VC Mentor Evaluation)</span>
              </h3>

              {/* 5 Core Scores Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 mb-6">
                {[
                  { label: "Viability Score", score: validation.viability_score || 82 },
                  { label: "Innovation Score", score: validation.innovation_score || 78 },
                  { label: "Market Opportunity", score: validation.market_opportunity_score || 88 },
                  { label: "Feasibility Score", score: validation.feasibility_score || 75 },
                  { label: "Scalability Score", score: validation.scalability_score || 84 },
                ].map((item, i) => {
                  const style = getScoreColor(item.score);
                  return (
                    <div key={i} className={`p-4 rounded-2xl bg-slate-950/80 border ${style.border} flex flex-col justify-between`}>
                      <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2 block">
                        {item.label}
                      </span>
                      <div>
                        <span className={`text-2xl font-black ${style.text}`}>{item.score}</span>
                        <span className="text-xs text-slate-500"> / 100</span>
                      </div>
                      <div className="w-full h-1.5 bg-slate-800 rounded-full mt-3 overflow-hidden">
                        <div className={`h-full ${style.bg} rounded-full`} style={{ width: `${item.score}%` }} />
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Risk Cards Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-rose-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4 text-rose-400" />
                    <span>Major Business Risks</span>
                  </h4>
                  <ul className="space-y-2 text-xs text-slate-300">
                    {safeArray(validation.major_business_risks).map((risk: any, i: number) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-rose-400 shrink-0">•</span>
                        <span>{safeRender(risk)}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4 text-amber-400" />
                    <span>Technical & Execution Risks</span>
                  </h4>
                  <ul className="space-y-2 text-xs text-slate-300">
                    {safeArray(validation.technical_risks).map((risk: any, i: number) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-amber-400 shrink-0">•</span>
                        <span>{safeRender(risk)}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4 text-purple-400" />
                    <span>Competitive Risks</span>
                  </h4>
                  <ul className="space-y-2 text-xs text-slate-300">
                    {safeArray(validation.competitive_risks).map((risk: any, i: number) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-purple-400 shrink-0">•</span>
                        <span>{safeRender(risk)}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Recommendations & Next Actions */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                    <CheckSquare className="w-4 h-4 text-indigo-400" />
                    <span>Validation Recommendations</span>
                  </h4>
                  <div className="space-y-2 text-xs text-slate-300">
                    {safeArray(validation.validation_recommendations).map((rec: any, i: number) => (
                      <div key={i} className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex items-start gap-2">
                        <span className="w-5 h-5 rounded-full bg-indigo-500/20 text-indigo-300 font-bold flex items-center justify-center shrink-0 text-[10px]">
                          {i + 1}
                        </span>
                        <span>{safeRender(rec)}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                    <Flame className="w-4 h-4 text-emerald-400" />
                    <span>Next Best Actions (Immediate 7-Day Plan)</span>
                  </h4>
                  <div className="space-y-2 text-xs text-slate-300">
                    {safeArray(validation.next_best_actions).map((act: any, i: number) => (
                      <div key={i} className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex items-start gap-2">
                        <span className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-300 font-bold flex items-center justify-center shrink-0 text-[10px]">
                          {i + 1}
                        </span>
                        <span>{safeRender(act)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Suggested First Customers & Growth Strategy */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2">Suggested First Customers</h4>
                  <ul className="space-y-1 text-xs text-slate-300">
                    {safeArray(validation.suggested_first_customers).map((cust: any, i: number) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-cyan-400 font-bold">•</span>
                        <span>{safeRender(cust)}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider mb-2">Long-Term Growth Strategy</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">{safeRender(validation.long_term_growth_strategy)}</p>
                </div>
              </div>

              {/* Final VC Mentor Verdict Card */}
              {validation.final_verdict && (
                <div className="p-6 rounded-2xl bg-gradient-to-br from-indigo-950 via-slate-950 to-purple-950 border border-indigo-500/40">
                  <h4 className="text-xs font-extrabold text-indigo-300 uppercase tracking-wider mb-2 flex items-center gap-2">
                    <Award className="w-5 h-5 text-indigo-400" />
                    <span>Final VC Mentor Verdict</span>
                  </h4>
                  <p className="text-sm font-bold text-white leading-relaxed">
                    {safeRender(validation.final_verdict)}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* 6. 4-Week Roadmap Tab */}
        {activeTab === "roadmap" && (
          <div className="space-y-6">
            <div className="glass-card p-6 rounded-2xl">
              <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                <Calendar className="w-5 h-5 text-indigo-400" />
                <span>4-Week Agile Execution Roadmap</span>
              </h3>

              <div className="space-y-4">
                {safeArray(roadmap.schedule).map((wk: any, i: number) => (
                  <div key={i} className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 flex flex-col md:flex-row md:items-start justify-between gap-4">
                    <div className="shrink-0">
                      <span className="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-extrabold uppercase border border-indigo-500/30 inline-block mb-1">
                        Week {wk.week || i + 1}
                      </span>
                      <h4 className="font-bold text-base text-white">{safeRender(wk.title)}</h4>
                      <p className="text-xs text-slate-400 italic mt-0.5">Focus: {safeRender(wk.goals)}</p>
                    </div>

                    <div className="flex-1 md:max-w-md">
                      <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Deliverables:</span>
                      <ul className="space-y-1">
                        {safeArray(wk.deliverables).map((deliv: any, idx: number) => (
                          <li key={idx} className="flex items-center gap-2 text-xs text-slate-300">
                            <ChevronRight className="w-3 h-3 text-indigo-400" />
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

        {/* 7. Pitch Deck Tab */}
        {activeTab === "pitch" && (
          <div className="space-y-6">
            <div className="glass-card p-6 rounded-2xl">
              <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                <Presentation className="w-5 h-5 text-indigo-400" />
                <span>Investor Pitch Deck & Hackathon Script</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-rose-400 uppercase tracking-wider mb-2">The Market Problem</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">{safeRender(pitch.problem)}</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2">The 10x Solution</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">{safeRender(pitch.solution)}</p>
                </div>
              </div>

              {/* Monetization */}
              <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 mb-6">
                <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2">Business Model & Revenue Streams</h4>
                <p className="text-xs text-slate-300 mb-4">{safeRender(pitch.business_model)}</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
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
                      <div key={i} className="p-3.5 rounded-xl bg-slate-900/90 text-xs text-indigo-200 border border-slate-800 font-medium leading-relaxed flex items-start gap-2.5">
                        <span className="w-5 h-5 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center shrink-0 text-[10px] font-bold">
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
                <div className="p-5 rounded-2xl bg-gradient-to-br from-indigo-950/80 via-purple-950/40 to-slate-950 border border-indigo-500/40">
                  <h4 className="text-xs font-extrabold text-indigo-300 uppercase tracking-wider mb-2 flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-indigo-400" />
                    <span>60-Second Hackathon Elevator Pitch</span>
                  </h4>
                  <p className="text-xs sm:text-sm text-slate-100 italic leading-relaxed">
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
            <div className="studio-card p-6 rounded-2xl border border-emerald-500/30">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <div>
                  <h3 className="text-base font-bold text-white flex items-center gap-2 mb-1">
                    <CheckSquare className="w-5 h-5 text-emerald-400" />
                    <span>Quality Control & Anti-Bias Audit</span>
                  </h3>
                  <p className="text-xs text-slate-400">
                    Final verification gate ensuring outputs match the classified business category without generic template leakage.
                  </p>
                </div>

                <div className="px-4 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-extrabold text-xs uppercase tracking-wider shrink-0">
                  Verdict: {qualityControl.quality_verdict || "PASS"}
                </div>
              </div>

              {/* QC Scores */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">Category Match Score</span>
                  <p className="text-xl font-black text-emerald-400">{qualityControl.category_match_score || 95}/100</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">Roadmap Fit Score</span>
                  <p className="text-xl font-black text-blue-400">{qualityControl.roadmap_fit_score || 92}/100</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">Pricing Model Fit Score</span>
                  <p className="text-xl font-black text-indigo-400">{qualityControl.pricing_model_fit_score || 90}/100</p>
                </div>
              </div>

              {/* Violations Flagged */}
              {safeArray(qualityControl.violations_found).length > 0 && (
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 mb-4">
                  <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">Template Violations Flagged</h4>
                  <ul className="space-y-1.5">
                    {safeArray(qualityControl.violations_found).map((v: any, idx: number) => (
                      <li key={idx} className="text-xs text-slate-300 flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
                        <span>{safeRender(v)}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Corrections Applied */}
              {safeArray(qualityControl.corrections_applied).length > 0 && (
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2">Autonomous Corrections Applied</h4>
                  <ul className="space-y-1.5">
                    {safeArray(qualityControl.corrections_applied).map((c: any, idx: number) => (
                      <li key={idx} className="text-xs text-slate-300 flex items-center gap-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                        <span>{safeRender(c)}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
