"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { 
  Sparkles, Rocket, ArrowRight, Bot, Cpu, TrendingUp, ShieldCheck, 
  Terminal, Sliders, Play, Layers, Code, CheckCircle2 
} from "lucide-react";

interface LandingHeroProps {
  onSubmitIdea: (idea: string, market?: string) => void;
  isSubmitting: boolean;
}

const SAMPLE_IDEAS = [
  { label: "🚚 Fruit Transport Company", idea: "Fruit Transport & Cold-Chain Logistics Company connecting regional orchards to wholesale markets" },
  { label: "🎒 Smart Anti-Theft Backpack", idea: "Smart Ergonomic Anti-Theft Backpack with integrated TSA biometric locks and solar charging" },
  { label: "🐟 Dockside Fresh Fish Market", idea: "Direct Dockside Seafood Marketplace delivering 100% formalin-free fresh catch in 90 minutes" },
  { label: "🩺 Ambient AI Medical Scribe", idea: "Ambient AI Medical Scribe converting doctor-patient audio consultations into structured clinical notes" },
  { label: "⚡ EV Battery Swapping Fleet", idea: "1-Minute EV Battery Swapping Network for commercial 2-wheeler and 3-wheeler delivery fleets" }
];

export function LandingHero({ onSubmitIdea, isSubmitting }: LandingHeroProps) {
  const [idea, setIdea] = useState("");
  const [targetMarket, setTargetMarket] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!idea.trim()) return;
    onSubmitIdea(idea.trim(), targetMarket.trim() || undefined);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 md:py-12">
      {/* Studio Header & Tagline */}
      <motion.div 
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="text-center space-y-4 mb-8"
      >
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 shadow-lg shadow-blue-500/5">
          <Sparkles className="w-4 h-4 text-blue-400 animate-pulse" />
          <span className="text-xs font-extrabold text-blue-300 uppercase tracking-widest">
            Synovia AI Studio Workspace
          </span>
        </div>

        <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-white leading-tight">
          Describe Any Startup Idea. <br />
          <span className="text-gradient-gemini">Synthesize An Investor-Ready Strategy.</span>
        </h1>

        <p className="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto font-normal leading-relaxed">
          Powered by an autonomous 8-agent AI swarm. Automatically classifies business type, enforces anti-pattern rules, and generates custom operational blueprints.
        </p>
      </motion.div>

      {/* Main Studio Prompt Box (Google AI Studio Styled) */}
      <motion.div 
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="studio-panel rounded-3xl p-5 sm:p-7 glow-gemini max-w-4xl mx-auto mb-10 relative overflow-hidden"
      >
        {/* Studio Workspace Bar Header */}
        <div className="flex flex-wrap items-center justify-between gap-3 pb-4 mb-4 border-b border-slate-800/80 text-xs font-semibold text-slate-400">
          <div className="flex items-center gap-2">
            <Terminal className="w-4 h-4 text-blue-400" />
            <span className="text-white font-bold uppercase tracking-wider">Prompt Editor</span>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-[11px] text-slate-300 font-mono">
              Swarm: 8 Agents
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-blue-500/10 border border-blue-500/30 text-[11px] text-blue-400 font-mono">
              Mode: Auto-Classification
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-[11px] text-emerald-400 font-mono">
              QC: Active
            </span>
          </div>
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
              Startup Vision & Core Idea
            </label>
            <textarea
              rows={4}
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="Enter any business vision... (e.g. A fruit transport company connecting regional orchards to wholesale markets with temperature monitoring...)"
              className="w-full px-4 py-3.5 rounded-2xl studio-input text-white placeholder-slate-500 text-sm focus:outline-none transition-all resize-none shadow-inner font-sans"
              required
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
            <div className="sm:col-span-2">
              <label className="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">
                Target Market / Region Focus (Optional)
              </label>
              <input
                type="text"
                value={targetMarket}
                onChange={(e) => setTargetMarket(e.target.value)}
                placeholder="e.g. India & Global / Tier-1 Cities / B2B Commercial"
                className="w-full px-3.5 py-2.5 rounded-xl studio-input text-slate-200 text-xs placeholder-slate-500 focus:outline-none"
              />
            </div>

            <div className="flex items-end">
              <button
                type="submit"
                disabled={isSubmitting || !idea.trim()}
                className="w-full flex items-center justify-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-black text-xs sm:text-sm shadow-xl shadow-blue-500/25 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {isSubmitting ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                    <span>Executing Swarm...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 text-blue-200 fill-blue-200" />
                    <span>Run Studio Pipeline</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </form>

        {/* Quick Sample Presets */}
        <div className="mt-5 pt-4 border-t border-slate-800/80">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
            Try a domain preset:
          </span>
          <div className="flex flex-wrap gap-2">
            {SAMPLE_IDEAS.map((preset, idx) => (
              <button
                key={idx}
                onClick={() => setIdea(preset.idea)}
                className="chip-pill text-xs px-3 py-1.5 rounded-xl text-slate-300 hover:text-white font-medium cursor-pointer"
              >
                {preset.label}
              </button>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Feature Highlights Grid */}
      <motion.div 
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-5 max-w-4xl mx-auto"
      >
        <div className="studio-card p-5 rounded-2xl">
          <div className="w-9 h-9 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mb-3">
            <Layers className="w-4 h-4 text-blue-400" />
          </div>
          <h3 className="font-bold text-xs text-white uppercase tracking-wider mb-1">1. Idea Classifier Agent</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Classifies into 19 categories (Transportation, Food, Hardware, Healthcare, Marketplace) to prevent SaaS template bias.
          </p>
        </div>

        <div className="studio-card p-5 rounded-2xl">
          <div className="w-9 h-9 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center mb-3">
            <Bot className="w-4 h-4 text-purple-400" />
          </div>
          <h3 className="font-bold text-xs text-white uppercase tracking-wider mb-1">2. Domain-Specific Swarm</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Research, Competitors, MVP specs, Roadmaps & Monetization models adapt strictly to physical or digital requirements.
          </p>
        </div>

        <div className="studio-card p-5 rounded-2xl">
          <div className="w-9 h-9 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mb-3">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <h3 className="font-bold text-xs text-white uppercase tracking-wider mb-1">3. Quality Control Audit</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Final QC verification gate removes unneeded SaaS subscriptions or React dashboards before generating reports.
          </p>
        </div>
      </motion.div>
    </div>
  );
}
