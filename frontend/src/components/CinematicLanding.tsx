"use client";

import React from "react";
import { motion } from "framer-motion";
import { 
  Sparkles, ArrowRight, Play, Terminal, Layers, Search, Users, Layout, 
  Calendar, Presentation, ShieldCheck, ShieldAlert, Cpu, CheckCircle2, History, Zap, Award
} from "lucide-react";

interface CinematicLandingProps {
  onEnterStudio: () => void;
  onSelectPreset: (idea: string, market?: string) => void;
  onOpenHistory: () => void;
  historyCount: number;
}

const AGENTS = [
  { id: 1, name: "Idea Classifier", role: "19 Domain Classifications & Anti-Pattern Detection", icon: Layers, bg: "bg-[#f59e0b]", tag: "DOMAIN-AWARE" },
  { id: 2, name: "Market Research", icon: Search, role: "TAM / SAM / SOM & Customer Personas", bg: "bg-[#3b82f6]", tag: "VENTURE INTEL" },
  { id: 3, name: "Competitors & Moats", icon: Users, role: "Incumbent Gaps & Defensability Strategy", bg: "bg-[#8b5cf6]", tag: "REAL BRAND DATA" },
  { id: 4, name: "MVP Spec Manager", icon: Layout, role: "Category-Specific Feature Matrix", bg: "bg-[#ec4899]", tag: "ZERO SAAS BIAS" },
  { id: 5, name: "Agile Roadmap", icon: Calendar, role: "4-Week Physical or Software Sprints", bg: "bg-[#10b981]", tag: "OPERATIONAL" },
  { id: 6, name: "VC Pitch & Monetization", icon: Presentation, role: "Revenue Streams & Unit Economics", bg: "bg-[#f97316]", tag: "INVESTOR READY" },
  { id: 7, name: "Validation & Mentor", icon: ShieldCheck, role: "YC/VC Score & Strategic Risk Verdict", bg: "bg-[#06b6d4]", tag: "VIABILITY SCORE" },
  { id: 8, name: "Quality Control Audit", icon: ShieldAlert, role: "Strict Anti-Pattern Rule Enforcement", bg: "bg-[#e11d48]", tag: "FINAL AUDIT" },
];

const PRESETS = [
  {
    title: "🚚 Fruit Transport Logistics",
    category: "LOGISTICS & TRANSPORTATION",
    desc: "Cold-chain refrigerated fleet connecting orchards directly to wholesale markets with IoT temperature sensors.",
    idea: "Fruit Transport & Cold-Chain Logistics Company connecting regional orchards to wholesale markets with temperature monitoring"
  },
  {
    title: "🎒 Smart Biometric Backpack",
    category: "CONSUMER HARDWARE",
    desc: "Ergonomic anti-theft smart backpack with embedded solar panels, GPS tracking, and TSA biometric locks.",
    idea: "Smart Ergonomic Anti-Theft Backpack with integrated TSA biometric locks and solar charging"
  },
  {
    title: "🐟 Dockside Fresh Fish Market",
    category: "FOOD & MARKETPLACE",
    desc: "Direct dockside seafood marketplace delivering 100% formalin-free fresh ocean catch within 90 minutes.",
    idea: "Direct Dockside Seafood Marketplace delivering 100% formalin-free fresh catch in 90 minutes"
  },
  {
    title: "🩺 Ambient AI Medical Scribe",
    category: "HEALTHCARE TECH",
    desc: "HIPAA-compliant ambient audio scribe translating doctor consultations into structured EMR clinical notes.",
    idea: "Ambient AI Medical Scribe converting doctor-patient audio consultations into structured clinical notes"
  }
];

export function CinematicLanding({ 
  onEnterStudio, 
  onSelectPreset, 
  onOpenHistory,
  historyCount 
}: CinematicLandingProps) {
  return (
    <div className="min-h-screen bg-white text-black font-sans relative z-10 flex flex-col justify-between py-12 px-4 md:px-8">
      {/* Main Hero Container */}
      <div className="max-w-6xl mx-auto w-full space-y-12">
        {/* Top Announcement Badge */}
        <motion.div 
          initial={{ opacity: 0, y: -15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex flex-wrap items-center justify-between gap-4 border-b-4 border-black pb-6"
        >
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-[#f59e0b] border-4 border-black shadow-[4px_4px_0px_#000000] flex items-center justify-center">
              <Sparkles className="w-7 h-7 text-black fill-black" />
            </div>
            <div>
              <span className="font-black text-2xl tracking-tight uppercase block leading-none">SYNOVIA</span>
              <span className="text-xs font-black text-gray-700 uppercase tracking-widest">Autonomous Startup Intelligence Engine</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={onOpenHistory}
              className="flex items-center gap-2 px-4 py-2 bg-white text-black border-3 border-black font-black text-xs uppercase shadow-[3px_3px_0px_#000000] hover:bg-[#fefae0] hover:-translate-x-0.5 hover:-translate-y-0.5 hover:shadow-[5px_5px_0px_#000000] transition-all cursor-pointer"
            >
              <History className="w-4 h-4 stroke-[2.5]" />
              <span>Past Blueprints ({historyCount})</span>
            </button>
          </div>
        </motion.div>

        {/* Main Cinematic Hero Banner */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="text-center space-y-6 max-w-4xl mx-auto"
        >
          <div className="inline-flex items-center gap-2 px-5 py-2 bg-[#ea580c] text-white border-3 border-black shadow-[5px_5px_0px_#000000]">
            <Zap className="w-4 h-4 fill-white" />
            <span className="text-xs font-black uppercase tracking-widest">
              Anti-Pattern Engine • 19 Domain Classifications
            </span>
          </div>

          <h1 className="text-4xl sm:text-6xl md:text-7xl font-black text-black leading-none uppercase tracking-tight">
            Stop Generating Generic SaaS Templates. <br />
            <span className="bg-[#f59e0b] text-black px-3 py-1 border-4 border-black inline-block shadow-[8px_8px_0px_#000000] mt-2">
              Synthesize Investor-Ready Intelligence.
            </span>
          </h1>

          <p className="text-base sm:text-xl font-bold text-gray-800 max-w-3xl mx-auto leading-relaxed uppercase tracking-wide">
            An autonomous 8-agent swarm that evaluates physical products, logistics, food production, hardware, healthcare, and marketplaces with strict category anti-pattern rules.
          </p>

          {/* Primary Action Call To Actions */}
          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <button
              onClick={onEnterStudio}
              className="flex items-center gap-3 px-8 py-4 bg-[#f59e0b] text-black border-4 border-black font-black text-sm sm:text-base uppercase shadow-[6px_6px_0px_#000000] hover:bg-[#fbbf24] hover:-translate-x-1 hover:-translate-y-1 hover:shadow-[10px_10px_0px_#000000] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none transition-all cursor-pointer"
            >
              <Play className="w-5 h-5 fill-black stroke-[2.5]" />
              <span>Launch Studio Prompt Workspace</span>
              <ArrowRight className="w-5 h-5 stroke-[3]" />
            </button>
          </div>
        </motion.div>

        {/* 8-Agent Swarm Architecture Showcase */}
        <motion.div 
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="space-y-4 pt-6"
        >
          <div className="flex items-center justify-between border-b-3 border-black pb-2">
            <h2 className="text-lg font-black text-black uppercase tracking-wider flex items-center gap-2">
              <Cpu className="w-5 h-5 text-black" />
              <span>Autonomous 8-Agent Swarm Architecture</span>
            </h2>
            <span className="text-xs font-black bg-[#fefae0] px-2.5 py-1 border-2 border-black shadow-[2px_2px_0px_#000000]">
              Parallel Pipeline
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            {AGENTS.map((agent) => {
              const Icon = agent.icon;
              return (
                <div 
                  key={agent.id}
                  className="bg-white border-3 border-black p-4 shadow-[5px_5px_0px_#000000] hover:-translate-y-1 hover:shadow-[7px_7px_0px_#000000] transition-all flex flex-col justify-between space-y-3"
                >
                  <div className="flex items-center justify-between">
                    <div className={`w-9 h-9 ${agent.bg} border-2 border-black shadow-[2px_2px_0px_#000000] flex items-center justify-center`}>
                      <Icon className="w-5 h-5 text-black stroke-[2.5]" />
                    </div>
                    <span className="text-[9px] font-black bg-black text-white px-2 py-0.5 uppercase">
                      {agent.tag}
                    </span>
                  </div>

                  <div>
                    <h3 className="font-black text-sm text-black uppercase">{agent.name}</h3>
                    <p className="text-xs font-bold text-gray-700 mt-1">{agent.role}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>

        {/* Preset Domains Grid */}
        <motion.div 
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="space-y-4 pt-6"
        >
          <div className="flex items-center justify-between border-b-3 border-black pb-2">
            <h2 className="text-lg font-black text-black uppercase tracking-wider flex items-center gap-2">
              <Award className="w-5 h-5 text-black" />
              <span>Explore Domain Presets (Click to Execute)</span>
            </h2>
            <span className="text-xs font-black bg-[#f59e0b] text-black px-2.5 py-1 border-2 border-black shadow-[2px_2px_0px_#000000]">
              1-Click Demo
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {PRESETS.map((preset, idx) => (
              <div 
                key={idx}
                onClick={() => onSelectPreset(preset.idea)}
                className="bg-white border-4 border-black p-5 shadow-[6px_6px_0px_#000000] hover:bg-[#fefae0] hover:-translate-x-1 hover:-translate-y-1 hover:shadow-[9px_9px_0px_#000000] transition-all cursor-pointer flex flex-col justify-between space-y-3 group"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-black bg-[#ea580c] text-white px-2 py-0.5 border-2 border-black uppercase shadow-[2px_2px_0px_#000000]">
                      {preset.category}
                    </span>
                    <ArrowRight className="w-5 h-5 text-black stroke-[3] group-hover:translate-x-1 transition-transform" />
                  </div>
                  <h3 className="font-black text-lg text-black uppercase">{preset.title}</h3>
                  <p className="text-xs font-bold text-gray-800 mt-1">{preset.desc}</p>
                </div>

                <div className="pt-2 border-t-2 border-black flex items-center justify-between text-xs font-black text-black uppercase">
                  <span>Run Agent Swarm</span>
                  <span className="text-[#ea580c] group-hover:underline">Launch Idea →</span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Footer Branding */}
      <div className="max-w-6xl mx-auto w-full pt-12 border-t-4 border-black mt-12 flex flex-wrap items-center justify-between gap-4 text-xs font-black uppercase text-gray-800">
        <div>
          <span>SYNOVIA AI STUDIO © 2026</span> • <span>Multi-Agent Venture Intelligence</span>
        </div>
        <div className="flex items-center gap-4">
          <span>Qwen 2.5 1.5B</span>
          <span>•</span>
          <span>Gemini Intelligence</span>
          <span>•</span>
          <span className="text-[#ea580c]">19 Categories</span>
        </div>
      </div>
    </div>
  );
}
