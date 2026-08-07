"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { 
  Sparkles, Terminal, Play, Layers, Bot, ShieldCheck 
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
    <div className="max-w-5xl mx-auto px-4 py-8 md:py-12 relative z-10">
      {/* Studio Header & Tagline */}
      <motion.div 
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="text-center space-y-4 mb-8"
      >
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#d97706]/15 border border-[#f59e0b]/35 shadow-lg shadow-amber-950/20">
          <Sparkles className="w-4 h-4 text-[#f59e0b] animate-pulse" />
          <span className="text-xs font-extrabold text-[#fefae0] uppercase tracking-widest">
            Autonomous Multi-Agent Studio
          </span>
        </div>

        <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-[#fffdfa] leading-tight">
          Describe Any Startup Idea. <br />
          <span className="text-gradient-gemini">Synthesize An Investor-Ready Strategy.</span>
        </h1>

        <p className="text-sm sm:text-base text-[#d4c4b5] max-w-2xl mx-auto font-medium leading-relaxed">
          Powered by an autonomous 8-agent AI swarm. Automatically classifies business type, enforces domain anti-pattern rules, and generates custom operational blueprints.
        </p>
      </motion.div>

      {/* Main Studio Prompt Box */}
      <motion.div 
        initial={{ opacity: 0, scale: 0.96, y: 10 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="studio-panel rounded-3xl p-6 sm:p-8 max-w-4xl mx-auto mb-10 relative overflow-hidden shadow-2xl border border-[#e8ded2]/20"
      >
        {/* Studio Workspace Bar Header */}
        <div className="flex flex-wrap items-center justify-between gap-3 pb-4 mb-4 border-b border-[#e8ded2]/15 text-xs font-semibold text-[#d4c4b5]">
          <div className="flex items-center gap-2">
            <Terminal className="w-4 h-4 text-[#f59e0b]" />
            <span className="text-[#fffdfa] font-bold uppercase tracking-wider">Prompt Editor</span>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <span className="px-2.5 py-1 rounded-lg bg-[#1f1613] border border-[#e8ded2]/15 text-[11px] text-[#fefae0] font-mono">
              Swarm: 8 Agents
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-[#d97706]/20 border border-[#f59e0b]/30 text-[11px] text-[#fef3c7] font-mono">
              Mode: Auto-Classification
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-[11px] text-emerald-300 font-mono">
              QC: Active
            </span>
          </div>
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-[#fefae0] uppercase tracking-wider mb-2">
              Startup Vision & Core Idea
            </label>
            <textarea
              rows={4}
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="Enter any business vision... (e.g. A fruit transport company connecting regional orchards to wholesale markets with temperature monitoring...)"
              className="w-full px-4.5 py-4 rounded-2xl studio-input text-[#fffdfa] placeholder-[#a39284] text-sm focus:outline-none transition-all resize-none shadow-inner font-sans"
              required
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 pt-1">
            <div className="sm:col-span-2">
              <label className="block text-[11px] font-bold text-[#d4c4b5] uppercase tracking-wider mb-1.5">
                Target Market / Region Focus (Optional)
              </label>
              <input
                type="text"
                value={targetMarket}
                onChange={(e) => setTargetMarket(e.target.value)}
                placeholder="e.g. India & Global / Tier-1 Cities / B2B Commercial"
                className="w-full px-4 py-2.5 rounded-xl studio-input text-[#fffdfa] text-xs placeholder-[#a39284] focus:outline-none"
              />
            </div>

            <div className="flex items-end">
              <button
                type="submit"
                disabled={isSubmitting || !idea.trim()}
                className="w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-amber-600 via-amber-700 to-rose-700 hover:from-amber-500 hover:to-rose-600 text-white font-black text-xs sm:text-sm shadow-xl shadow-amber-950/40 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {isSubmitting ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                    <span>Executing Swarm...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 text-[#fefae0] fill-[#fefae0]" />
                    <span>Run Studio Pipeline</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </form>

        {/* Quick Sample Presets */}
        <div className="mt-5 pt-4 border-t border-[#e8ded2]/15">
          <span className="text-[11px] font-bold text-[#d4c4b5] uppercase tracking-wider block mb-2">
            Try a domain preset:
          </span>
          <div className="flex flex-wrap gap-2">
            {SAMPLE_IDEAS.map((preset, idx) => (
              <button
                key={idx}
                onClick={() => setIdea(preset.idea)}
                className="chip-pill text-xs px-3.5 py-1.5 rounded-xl text-[#fefae0] hover:text-white font-medium cursor-pointer"
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
          <div className="w-10 h-10 rounded-xl bg-[#d97706]/20 border border-[#f59e0b]/30 flex items-center justify-center mb-3">
            <Layers className="w-5 h-5 text-[#f59e0b]" />
          </div>
          <h3 className="font-extrabold text-xs text-[#fffdfa] uppercase tracking-wider mb-1">1. Idea Classifier Agent</h3>
          <p className="text-xs text-[#d4c4b5] leading-relaxed">
            Classifies into 19 categories (Transportation, Food, Hardware, Healthcare, Marketplace) to prevent SaaS template bias.
          </p>
        </div>

        <div className="studio-card p-5 rounded-2xl">
          <div className="w-10 h-10 rounded-xl bg-purple-500/20 border border-purple-500/30 flex items-center justify-center mb-3">
            <Bot className="w-5 h-5 text-purple-300" />
          </div>
          <h3 className="font-extrabold text-xs text-[#fffdfa] uppercase tracking-wider mb-1">2. Domain-Specific Swarm</h3>
          <p className="text-xs text-[#d4c4b5] leading-relaxed">
            Research, Competitors, MVP specs, Roadmaps & Monetization models adapt strictly to physical or digital requirements.
          </p>
        </div>

        <div className="studio-card p-5 rounded-2xl">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center mb-3">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
          </div>
          <h3 className="font-extrabold text-xs text-[#fffdfa] uppercase tracking-wider mb-1">3. Quality Control Audit</h3>
          <p className="text-xs text-[#d4c4b5] leading-relaxed">
            Final QC verification gate removes unneeded SaaS subscriptions or React dashboards before generating reports.
          </p>
        </div>
      </motion.div>
    </div>
  );
}
