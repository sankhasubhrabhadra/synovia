"use client";

import React, { useEffect, useState } from "react";
import { Sparkles, Cpu, Layers, ShieldCheck, ArrowRight } from "lucide-react";

interface IntroSplashProps {
  onComplete: () => void;
}

export function IntroSplash({ onComplete }: IntroSplashProps) {
  const [progress, setProgress] = useState(0);
  const [stageText, setStageText] = useState("Initializing Autonomous Swarm Core...");
  const [isFading, setIsFading] = useState(false);

  useEffect(() => {
    const stageMessages = [
      "Initializing Autonomous Swarm Core...",
      "Loading 8 Specialized Agent Models...",
      "Activating Anti-Pattern Anti-Bias Engine...",
      "Synovia Studio Engine Ready."
    ];

    let currentProgress = 0;
    const interval = setInterval(() => {
      currentProgress += 4;
      if (currentProgress >= 100) {
        currentProgress = 100;
        clearInterval(interval);
        setStageText("Synovia Studio Engine Ready.");
        setTimeout(() => {
          setIsFading(true);
          setTimeout(() => {
            onComplete();
          }, 600);
        }, 400);
      } else {
        const msgIdx = Math.min(
          Math.floor((currentProgress / 100) * stageMessages.length),
          stageMessages.length - 1
        );
        setStageText(stageMessages[msgIdx]);
      }
      setProgress(currentProgress);
    }, 45);

    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <div 
      className={`fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#181210] text-[#fffdfa] transition-opacity duration-600 ${
        isFading ? "opacity-0 pointer-events-none" : "opacity-100"
      }`}
    >
      {/* Animated Colorful Mesh Canvas Background */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-[450px] h-[450px] rounded-full bg-gradient-to-tr from-amber-500/25 via-rose-500/20 to-purple-600/25 blur-3xl animate-pulse" style={{ animationDuration: '6s' }} />
        <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] rounded-full bg-gradient-to-bl from-cyan-500/20 via-indigo-600/25 to-amber-600/20 blur-3xl animate-pulse" style={{ animationDuration: '8s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-gradient-to-r from-emerald-500/15 via-purple-600/20 to-amber-500/15 blur-3xl animate-spin" style={{ animationDuration: '25s' }} />
      </div>

      {/* Main Logo & Intro Content */}
      <div className="relative z-10 flex flex-col items-center max-w-md px-6 text-center">
        {/* Glowing Logo Circle with Concentric Rings */}
        <div className="relative mb-8 group cursor-pointer">
          {/* Concentric Pulsing Rings */}
          <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-amber-500 via-rose-500 to-indigo-500 animate-ping opacity-25 blur-sm" />
          <div className="absolute -inset-3 rounded-3xl bg-gradient-to-tr from-amber-600 via-purple-600 to-cyan-500 opacity-40 blur-md animate-pulse" />
          
          <div className="relative w-24 h-24 rounded-3xl bg-gradient-to-tr from-[#2d2019] via-[#3d2b22] to-[#4a362c] p-[2px] shadow-2xl shadow-amber-900/50">
            <div className="w-full h-full bg-[#1e1512] rounded-[22px] flex items-center justify-center border border-[#e8ded2]/20">
              <Sparkles className="w-12 h-12 text-[#fefae0] animate-bounce" />
            </div>
          </div>
        </div>

        {/* Brand Name & Tagline */}
        <h1 className="text-3xl font-black tracking-tight text-[#fffdfa] mb-2 flex items-center gap-2">
          <span>SYNOVIA</span>
          <span className="text-xs px-2.5 py-1 rounded-md bg-[#d97706]/20 border border-[#f59e0b]/40 text-[#fef3c7] font-extrabold uppercase tracking-widest">
            AI STUDIO v2.0
          </span>
        </h1>
        
        <p className="text-xs font-semibold text-[#d4c4b5] tracking-wide uppercase mb-8">
          Autonomous 8-Agent Swarm • Startup Intelligence
        </p>

        {/* Progress Bar Container */}
        <div className="w-full bg-[#2a1d17] p-1 rounded-full border border-[#e8ded2]/20 shadow-inner mb-4">
          <div 
            className="h-2.5 bg-gradient-to-r from-amber-500 via-purple-500 to-cyan-400 rounded-full transition-all duration-150 shadow-md shadow-amber-500/50"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Loading Stage Status Text */}
        <div className="flex items-center gap-2 text-xs font-medium text-[#eae0d5]">
          <Cpu className="w-3.5 h-3.5 text-[#f59e0b] animate-spin" />
          <span>{stageText}</span>
          <span className="font-mono font-bold text-[#fefae0] ml-auto">{progress}%</span>
        </div>
      </div>
    </div>
  );
}
