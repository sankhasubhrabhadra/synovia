"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";

interface Props {
  children: ReactNode;
  fallbackMessage?: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught React component error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="max-w-2xl mx-auto my-12 p-8 glass-card rounded-3xl border border-rose-500/30 text-center">
          <div className="w-12 h-12 rounded-2xl bg-rose-500/10 text-rose-400 flex items-center justify-center mx-auto mb-4 border border-rose-500/20">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-black text-white mb-2">Display Error Prevented</h3>
          <p className="text-xs text-slate-400 mb-6">
            {this.props.fallbackMessage || "A minor display issue occurred while rendering this section."}
          </p>
          {this.state.error && (
            <div className="p-3 rounded-xl bg-slate-950 text-left font-mono text-[11px] text-rose-300 border border-slate-900 mb-6 max-h-32 overflow-y-auto">
              {this.state.error.message}
            </div>
          )}
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg transition-all"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Try Reloading Component</span>
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
