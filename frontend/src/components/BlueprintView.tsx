"use client";

import React, { useState } from "react";
import { getProjectPdfUrl, Project } from "@/lib/api";
import { 
  Download, Sparkles, Search, Users, Layout, Server, Calendar, 
  Presentation, CheckCircle2, FileText, ArrowUpRight, ShieldCheck, 
  Zap, Code2, ChevronRight, Layers, Target
} from "lucide-react";

interface BlueprintViewProps {
  project: Project;
}

export function BlueprintView({ project }: BlueprintViewProps) {
  const [activeTab, setActiveTab] = useState<"summary" | "research" | "competitor" | "product" | "architect" | "roadmap" | "pitch">("summary");

  const blueprint = project.blueprint || {};
  const research = blueprint.research || {};
  const competitor = blueprint.competitor || {};
  const product = blueprint.product || {};
  const architect = blueprint.architect || {};
  const roadmap = blueprint.roadmap || {};
  const pitch = blueprint.pitch || {};

  const handleDownloadPdf = () => {
    const pdfUrl = getProjectPdfUrl(project.id);
    window.open(pdfUrl, "_blank");
  };

  // Helper to format tech stack layers whether string or object
  const getTechDetails = (data: any, defaultTech: string, defaultRationale: string) => {
    if (typeof data === "string" && data.trim()) {
      return { technology: data, rationale: defaultRationale };
    }
    if (typeof data === "object" && data !== null) {
      return {
        technology: data.technology || defaultTech,
        rationale: data.rationale || defaultRationale
      };
    }
    return { technology: defaultTech, rationale: defaultRationale };
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header Banner */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl mb-8 border border-indigo-500/20 glow-purple flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold uppercase tracking-wider mb-3">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Startup Blueprint Generated</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white leading-tight mb-2">
            {project.idea}
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 max-w-2xl">
            Synthesized by 7 specialized AI agents on {new Date(project.created_at).toLocaleDateString(undefined, { dateStyle: "medium" })}.
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={handleDownloadPdf}
            className="flex items-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs sm:text-sm shadow-xl shadow-indigo-600/30 transition-all hover:scale-[1.02] active:scale-[0.98]"
          >
            <Download className="w-4 h-4" />
            <span>Download Investor PDF</span>
          </button>
        </div>
      </div>

      {/* Tabs Navigation Header */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-3 mb-6 scrollbar-none border-b border-slate-800">
        {[
          { id: "summary", label: "Executive Summary", icon: FileText },
          { id: "research", label: "Market Analysis", icon: Search },
          { id: "competitor", label: "Competitors & Gaps", icon: Users },
          { id: "product", label: "MVP Product Spec", icon: Layout },
          { id: "architect", label: "System Architecture", icon: Server },
          { id: "roadmap", label: "4-Week Roadmap", icon: Calendar },
          { id: "pitch", label: "Pitch & Monetization", icon: Presentation },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs whitespace-nowrap transition-all ${
                isActive
                  ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/25 border border-indigo-400/30"
                  : "bg-slate-900/60 text-slate-400 border border-slate-800/60 hover:bg-slate-800/80 hover:text-slate-200"
              }`}
            >
              <Icon className="w-4 h-4" />
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
                <p className="text-lg font-bold text-indigo-300">{research.market_size?.tam || "N/A"}</p>
              </div>

              <div className="glass-card p-5 rounded-2xl">
                <span className="text-xs text-slate-400 font-semibold block mb-1">Primary Tech Stack</span>
                <p className="text-sm font-bold text-purple-300">
                  {getTechDetails(architect.frontend, "React Native & Next.js", "").technology}
                </p>
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
                <p className="text-sm text-slate-200 font-medium">{pitch.usp}</p>
              </div>
            )}
          </div>
        )}

        {/* 2. Market Analysis Tab */}
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
                  <p className="text-xs text-slate-300">{research.market_size?.tam}</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <span className="text-xs font-bold text-purple-400 block mb-1">SAM (Serviceable Market)</span>
                  <p className="text-xs text-slate-300">{research.market_size?.sam}</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <span className="text-xs font-bold text-cyan-400 block mb-1">SOM (Year 1-2 Reachable)</span>
                  <p className="text-xs text-slate-300">{research.market_size?.som}</p>
                </div>
              </div>

              {/* Customer Pain Points */}
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">Customer Pain Points</h4>
              <div className="space-y-2 mb-6">
                {(research.customer_pain_points || []).map((pain: string, i: number) => (
                  <div key={i} className="flex items-start gap-2.5 text-xs text-slate-300 p-3 rounded-lg bg-slate-900/40 border border-slate-800/60">
                    <span className="w-5 h-5 rounded-full bg-rose-500/10 text-rose-400 flex items-center justify-center shrink-0 text-[10px] font-bold">
                      {i + 1}
                    </span>
                    <span>{pain}</span>
                  </div>
                ))}
              </div>

              {/* Target User Personas */}
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">Target User Personas</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {(research.target_users || []).map((user: any, i: number) => (
                  <div key={i} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
                    <h5 className="font-bold text-sm text-indigo-300 mb-1">{user.persona}</h5>
                    <p className="text-xs text-slate-400 mb-3">{user.description}</p>
                    <div className="space-y-1">
                      {(user.pain_points || []).map((p: string, j: number) => (
                        <span key={j} className="inline-block text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 mr-1.5 mb-1">
                          • {p}
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
                {(competitor.competitors || []).map((comp: any, i: number) => (
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
                          {(comp.strengths || []).map((s: string, idx: number) => (
                            <li key={idx}>{s}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <span className="text-rose-400 font-semibold block mb-1">Weaknesses & Gaps:</span>
                        <ul className="list-disc list-inside text-slate-300 space-y-0.5">
                          {(comp.weaknesses || []).map((w: string, idx: number) => (
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
                  <p className="text-xs text-slate-300">{competitor.defensability_strategy}</p>
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
                    {(product.mvp_features || []).map((feat: any, i: number) => (
                      <div key={i} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="font-bold text-sm text-slate-200">{feat.name}</h5>
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                            Impact: {feat.impact || "High"}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400">{feat.description}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider mb-3">User Journey Workflow</h4>
                  <div className="space-y-2">
                    {(product.user_journey || []).map((step: string, i: number) => (
                      <div key={i} className="flex items-start gap-3 p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                        <span className="w-6 h-6 rounded-full bg-purple-500/20 text-purple-300 font-bold flex items-center justify-center shrink-0 text-xs">
                          {i + 1}
                        </span>
                        <p className="text-xs text-slate-300 pt-0.5">{step}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 5. System Architecture Tab */}
        {activeTab === "architect" && (
          <div className="space-y-6">
            <div className="glass-card p-6 rounded-2xl">
              <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                <Server className="w-5 h-5 text-indigo-400" />
                <span>Technical Architecture & Tech Stack</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                {[
                  { label: "Frontend", key: "frontend", defaultT: "React Native & Next.js 15", defaultR: "Cross-platform client application interface" },
                  { label: "Backend API", key: "backend", defaultT: "FastAPI (Python 3.12)", defaultR: "High-performance asynchronous microservice engine" },
                  { label: "Database", key: "database", defaultT: "PostgreSQL & Redis Cache", defaultR: "ACID database compliance paired with sub-millisecond cache" },
                  { label: "Authentication", key: "authentication", defaultT: "OAuth 2.0 & Mobile OTP", defaultR: "Secure identity provider & access tokens" },
                  { label: "AI Infrastructure", key: "ai_apis", defaultT: "Domain AI & Speech Engine", defaultR: "Intelligent automated inference & vision pipeline" },
                  { label: "Deployment Host", key: "deployment", defaultT: "Vercel Edge & AWS Cloud", defaultR: "Global CDN storefront paired with cloud microservices" },
                ].map((item, i) => {
                  const rawData = architect[item.key];
                  const details = getTechDetails(rawData, item.defaultT, item.defaultR);
                  return (
                    <div key={i} className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                      <span className="text-[11px] font-bold text-indigo-400 uppercase tracking-wider block mb-1">
                        {item.label}
                      </span>
                      <p className="font-bold text-sm text-white mb-1.5 leading-snug">
                        {details.technology}
                      </p>
                      <p className="text-xs text-slate-400 leading-relaxed">
                        {details.rationale}
                      </p>
                    </div>
                  );
                })}
              </div>

              {/* Folder Structure Diagram */}
              {architect.folder_structure && (
                <div>
                  <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">Project Folder Architecture</h4>
                  <pre className="p-4 rounded-xl bg-slate-950 text-indigo-300 font-mono text-xs overflow-x-auto border border-slate-800">
                    {architect.folder_structure}
                  </pre>
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
                {(roadmap.schedule || []).map((wk: any, i: number) => (
                  <div key={i} className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 flex flex-col md:flex-row md:items-start justify-between gap-4">
                    <div className="shrink-0">
                      <span className="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-extrabold uppercase border border-indigo-500/30 inline-block mb-1">
                        Week {wk.week || i + 1}
                      </span>
                      <h4 className="font-bold text-base text-white">{wk.title}</h4>
                      <p className="text-xs text-slate-400 italic mt-0.5">Focus: {wk.goals}</p>
                    </div>

                    <div className="flex-1 md:max-w-md">
                      <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Deliverables:</span>
                      <ul className="space-y-1">
                        {(wk.deliverables || []).map((deliv: string, idx: number) => (
                          <li key={idx} className="flex items-center gap-2 text-xs text-slate-300">
                            <ChevronRight className="w-3 h-3 text-indigo-400" />
                            <span>{deliv}</span>
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
                  <p className="text-xs text-slate-300 leading-relaxed">{pitch.problem}</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2">The 10x Solution</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">{pitch.solution}</p>
                </div>
              </div>

              {/* Monetization */}
              <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 mb-6">
                <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2">Business Model & Revenue Streams</h4>
                <p className="text-xs text-slate-300 mb-4">{pitch.business_model}</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {(pitch.revenue_streams || []).map((rev: any, i: number) => {
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
      </div>
    </div>
  );
}
