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
      currentProgress += 5;
      if (currentProgress >= 100) {
        currentProgress = 100;
        clearInterval(interval);
        setStageText("Synovia Studio Engine Ready.");
        setTimeout(() => {
          setIsFading(true);
          setTimeout(() => {
            onComplete();
          }, 500);
        }, 300);
      } else {
        const msgIdx = Math.min(
          Math.floor((currentProgress / 100) * stageMessages.length),
          stageMessages.length - 1
        );
        setStageText(stageMessages[msgIdx]);
      }
      setProgress(currentProgress);
    }, 40);

    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <div 
      className={`fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#1a120e] text-[#fffdfa] transition-opacity duration-500 ${
        isFading ? "opacity-0 pointer-events-none" : "opacity-100"
      }`}
    >
      {/* Animated Colorful Mesh Canvas Background */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-[450px] h-[450px] rounded-full bg-gradient-to-tr from-amber-500/30 via-rose-500/25 to-purple-600/30 blur-3xl animate-pulse" style={{ animationDuration: '6s' }} />
        <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] rounded-full bg-gradient-to-bl from-cyan-500/25 via-indigo-600/30 to-amber-600/25 blur-3xl animate-pulse" style={{ animationDuration: '8s' }} />
      </div>

      {/* Neo-Brutalist Main Logo & Intro Container */}
      <div className="relative z-10 flex flex-col items-center max-w-md px-6 text-center bg-[#251b15] border-4 border-black p-8 shadow-[10px_10px_0px_#000000]">
        {/* Brutalist Logo Circle */}
        <div className="relative mb-6">
          <div className="w-24 h-24 bg-[#f59e0b] border-4 border-black shadow-[6px_6px_0px_#000000] flex items-center justify-center">
            <Sparkles className="w-12 h-12 text-black fill-black animate-bounce" />
          </div>
        </div>

        {/* Brand Name & Tagline */}
        <h1 className="text-4xl font-black tracking-tight text-[#fffdfa] uppercase mb-2 flex items-center gap-2">
          <span>SYNOVIA</span>
          <span className="text-xs px-2.5 py-1 bg-[#ea580c] text-white border-2 border-black font-black uppercase shadow-[2px_2px_0px_#000000]">
            AI v2.0
          </span>
        </h1>
        
        <p className="text-xs font-black text-[#d4c4b5] tracking-wider uppercase mb-6 bg-[#17100c] px-3 py-1 border-2 border-black shadow-[3px_3px_0px_#000000]">
          Autonomous 8-Agent Swarm Intelligence
        </p>

        {/* Progress Bar Container */}
        <div className="w-full bg-[#120c0a] p-1 border-3 border-black shadow-[4px_4px_0px_#000000] mb-4">
          <div 
            className="h-3 bg-[#f59e0b] border-r-2 border-black transition-all duration-150"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Loading Stage Status Text */}
        <div className="w-full flex items-center justify-between text-xs font-black text-[#fffdfa] bg-[#2b1f19] px-3 py-2 border-2 border-black shadow-[2px_2px_0px_#000000]">
          <div className="flex items-center gap-2">
            <Cpu className="w-4 h-4 text-[#f59e0b] animate-spin" />
            <span className="truncate">{stageText}</span>
          </div>
          <span className="font-mono text-[#f59e0b]">{progress}%</span>
        </div>
      </div>
    </div>
  );
}
