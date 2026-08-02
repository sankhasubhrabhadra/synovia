"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, Rocket, ArrowRight, Bot, Target, Cpu, TrendingUp, ShieldCheck, Zap } from "lucide-react";

interface LandingHeroProps {
  onSubmitIdea: (idea: string, market?: string) => void;
  isSubmitting: boolean;
}

const SAMPLE_IDEAS = [
  "AI-powered medical billing audit software for independent clinics",
  "Autonomous devops agent that auto-remediates Kubernetes cluster errors",
  "B2B SaaS for automated climate compliance and carbon offset tracking",
  "Voice-activated AI copilot for real estate agents during property tours"
];

export function LandingHero({ onSubmitIdea, isSubmitting }: LandingHeroProps) {
  const [idea, setIdea] = useState("");
  const [targetMarket, setTargetMarket] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!idea.trim()) return;
    onSubmitIdea(idea.trim(), targetMarket.trim() || undefined);
  };

  const handleSelectSample = (sample: string) => {
    setIdea(sample);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-10 md:py-16">
      {/* Hero Header */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center space-y-6 mb-12"
      >
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-gradient-to-r from-indigo-500/10 via-purple-500/10 to-cyan-500/10 border border-indigo-500/20 shadow-lg shadow-indigo-500/5">
          <Sparkles className="w-4 h-4 text-indigo-400 animate-pulse" />
          <span className="text-xs font-semibold text-indigo-300 uppercase tracking-wider">
            Autonomous Multi-Agent AI Swarm
          </span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white leading-[1.15]">
          Turn Any Startup Idea Into An <br />
          <span className="text-gradient">Investor-Ready Blueprint</span>
        </h1>

        <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto font-normal leading-relaxed">
          <strong className="text-slate-200">Your Autonomous AI Co-Founder.</strong> Synovia deploys specialized AI agents to research markets, benchmark competitors, spec product MVPs, design technical architectures, and draft pitch decks in seconds.
        </p>
      </motion.div>

      {/* Main Idea Input Form */}
      <motion.div 
        initial={{ opacity: 0, scale: 0.96 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.15 }}
        className="glass-panel p-6 sm:p-8 rounded-3xl glow-purple max-w-3xl mx-auto mb-12 border border-indigo-500/20 relative overflow-hidden"
      >
        {/* Subtle ambient lighting background */}
        <div className="absolute -top-24 -left-24 w-60 h-60 bg-indigo-600/15 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -right-24 w-60 h-60 bg-purple-600/15 rounded-full blur-3xl pointer-events-none" />

        <form onSubmit={handleSubmit} className="space-y-4 relative z-10">
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider">
                What is your startup idea?
              </label>
              <span className="text-[11px] text-slate-500 font-medium">Describe your vision or domain</span>
            </div>
            <textarea
              rows={3}
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="e.g. An AI-powered medical billing audit software for independent clinics that auto-detects coding discrepancies..."
              className="w-full px-4 py-3.5 rounded-xl bg-slate-950/90 border border-slate-800 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all resize-none shadow-inner"
              required
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                Target Market (Optional)
              </label>
              <input
                type="text"
                value={targetMarket}
                onChange={(e) => setTargetMarket(e.target.value)}
                placeholder="e.g. North America Healthcare SMBs"
                className="w-full px-3.5 py-2.5 rounded-lg bg-slate-950/90 border border-slate-800 text-slate-200 text-xs placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div className="flex items-end">
              <button
                type="submit"
                disabled={isSubmitting || !idea.trim()}
                className="w-full flex items-center justify-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm shadow-xl shadow-indigo-600/30 transition-all hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {isSubmitting ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                    <span>Deploying Swarm...</span>
                  </>
                ) : (
                  <>
                    <Rocket className="w-4 h-4 text-indigo-200" />
                    <span>Generate Startup Blueprint</span>
                    <ArrowRight className="w-4 h-4 ml-1 text-indigo-200" />
                  </>
                )}
              </button>
            </div>
          </div>
        </form>

        {/* Sample Prompt Chips */}
        <div className="mt-6 pt-5 border-t border-slate-800/80 relative z-10">
          <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-2.5">
            Or try one of these sample startup ideas:
          </span>
          <div className="flex flex-wrap gap-2">
            {SAMPLE_IDEAS.map((sample, idx) => (
              <button
                key={idx}
                onClick={() => handleSelectSample(sample)}
                className="text-left text-xs px-3 py-1.5 rounded-lg bg-slate-900/60 border border-slate-800 text-slate-300 hover:text-white hover:border-indigo-500/40 hover:bg-slate-900 transition-all cursor-pointer"
              >
                "{sample}"
              </button>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Feature Grid */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto"
      >
        <div className="glass-card p-5 rounded-2xl">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center mb-3">
            <Bot className="w-5 h-5 text-purple-400" />
          </div>
          <h3 className="font-bold text-sm text-white mb-1">7 Autonomous AI Agents</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Manager, Research, Competitor, Product, Technical Architect, Roadmap, and Pitch agents work together seamlessly.
          </p>
        </div>

        <div className="glass-card p-5 rounded-2xl">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mb-3">
            <Cpu className="w-5 h-5 text-indigo-400" />
          </div>
          <h3 className="font-bold text-sm text-white mb-1">Full Technical Stack Spec</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Generates production architecture, DB schemas, API layer breakdowns, and folder structures.
          </p>
        </div>

        <div className="glass-card p-5 rounded-2xl">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mb-3">
            <TrendingUp className="w-5 h-5 text-cyan-400" />
          </div>
          <h3 className="font-bold text-sm text-white mb-1">Investor Blueprint PDF</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            One-click download of a clean executive summary, competitor matrix, TAM sizing, and elevator pitch.
          </p>
        </div>
      </motion.div>
    </div>
  );
}
