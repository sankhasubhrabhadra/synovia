"use client";

import React, { useState, useEffect } from "react";
import { Sparkles, Plus, Settings, Check, X, Server } from "lucide-react";
import { getApiBaseUrl, setApiBaseUrl } from "@/lib/api";

interface NavbarProps {
  onNewProject: () => void;
  activeProjectIdea?: string;
  isExecuting?: boolean;
}

export function Navbar({ onNewProject, activeProjectIdea, isExecuting }: NavbarProps) {
  const [showSettings, setShowSettings] = useState(false);
  const [serverUrl, setServerUrl] = useState("");
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    setServerUrl(getApiBaseUrl());
  }, [showSettings]);

  const handleSaveSettings = (e: React.FormEvent) => {
    e.preventDefault();
    setApiBaseUrl(serverUrl.trim());
    setSavedSuccess(true);
    setTimeout(() => {
      setSavedSuccess(false);
      setShowSettings(false);
      window.location.reload();
    }, 1000);
  };

  return (
    <header className="h-16 border-b border-slate-800/80 glass-panel sticky top-0 z-40 px-4 md:px-8 flex items-center justify-between">
      {/* Brand Logo */}
      <div className="flex items-center gap-3 cursor-pointer" onClick={onNewProject}>
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-cyan-400 p-[1px] flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <div className="w-full h-full bg-slate-950 rounded-[11px] flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-indigo-400" />
          </div>
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-lg tracking-tight text-white">SYNOVIA</span>
            <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase tracking-widest">
              AI Co-Founder
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-medium hidden sm:block">Autonomous Multi-Agent Startup Synthesizer</p>
        </div>
      </div>

      {/* Center status banner if actively generating */}
      {isExecuting && (
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-950/60 border border-indigo-500/30 animate-pulse">
          <div className="w-2 h-2 rounded-full bg-indigo-400 animate-ping" />
          <span className="text-xs font-semibold text-indigo-300">
            Agents Operating: {activeProjectIdea ? `"${activeProjectIdea.slice(0, 25)}..."` : "Processing..."}
          </span>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-2 sm:gap-3">
        {/* Settings button */}
        <button
          onClick={() => setShowSettings(true)}
          title="Server Connection Settings"
          className="p-2 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition-all cursor-pointer"
        >
          <Settings className="w-4 h-4" />
        </button>

        <button
          onClick={onNewProject}
          className="flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white shadow-md shadow-indigo-600/20 transition-all hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span className="hidden sm:inline">New Blueprint</span>
        </button>
      </div>

      {/* Server Connection Modal */}
      {showSettings && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-panel p-6 rounded-2xl max-w-md w-full border border-indigo-500/30 shadow-2xl relative">
            <button
              onClick={() => setShowSettings(false)}
              className="absolute right-4 top-4 text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2 mb-3">
              <Server className="w-5 h-5 text-indigo-400" />
              <h3 className="font-bold text-base text-white">Backend Server Settings</h3>
            </div>

            <p className="text-xs text-slate-400 mb-4 leading-relaxed">
              Connect to your laptop backend tunnel (e.g. <code className="text-indigo-300 bg-slate-900 px-1 py-0.5 rounded">https://smart-files-rush.loca.lt</code>) or local server.
            </p>

            <form onSubmit={handleSaveSettings} className="space-y-4">
              <div>
                <label className="block text-[11px] font-bold text-slate-300 uppercase tracking-wider mb-1.5">
                  Backend API Base URL
                </label>
                <input
                  type="text"
                  value={serverUrl}
                  onChange={(e) => setServerUrl(e.target.value)}
                  placeholder="https://smart-files-rush.loca.lt"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/90 border border-slate-800 text-white text-xs placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => {
                    setServerUrl("http://localhost:8000");
                  }}
                  className="px-3 py-1.5 text-xs text-slate-400 hover:text-white"
                >
                  Reset to Localhost
                </button>

                <button
                  type="submit"
                  className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-all shadow-md shadow-indigo-600/30"
                >
                  {savedSuccess ? (
                    <>
                      <Check className="w-4 h-4 text-emerald-400" />
                      <span>Connected!</span>
                    </>
                  ) : (
                    <span>Save & Connect</span>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </header>
  );
}
