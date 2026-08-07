"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import { 
  Mic, MicOff, Volume2, VolumeX, HelpCircle, X, Sparkles, 
  Terminal, Shield, Play, FileText, Presentation, Activity, Command
} from "lucide-react";

interface IrrisAssistantProps {
  onStartProject: (idea: string, targetMarket?: string) => void;
  onNavigateTab: (tab: string) => void;
  onDownloadPdf: () => void;
  onDownloadPpt: () => void;
  onReadSummary: () => string | void;
  onReadValidation: () => string | void;
  onNewProject: () => void;
  onOpenHistory?: () => void;
  onCloseHistory?: () => void;
  onExitStudio?: () => void;
  activeTab?: string;
  isExecuting?: boolean;
  currentAgentStep?: string;
  projectIdea?: string;
}

export function IrrisAssistant({
  onStartProject,
  onNavigateTab,
  onDownloadPdf,
  onDownloadPpt,
  onReadSummary,
  onReadValidation,
  onNewProject,
  onOpenHistory,
  onCloseHistory,
  onExitStudio,
  activeTab,
  isExecuting,
  currentAgentStep,
  projectIdea
}: IrrisAssistantProps) {
  const [isListening, setIsListening] = useState<boolean>(false);
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);
  const [isThinking, setIsThinking] = useState<boolean>(false);
  const [isMuted, setIsMuted] = useState<boolean>(false);
  const [showHelp, setShowHelp] = useState<boolean>(false);
  const [transcript, setTranscript] = useState<string>("");
  const [lastResponse, setLastResponse] = useState<string>("IRRIS // Online. Awaiting operational command, Boss.");
  const [showCaption, setShowCaption] = useState<boolean>(true);

  // Multi-Step Conversational Onboarding Consultation State
  const [consultationStep, setConsultationStep] = useState<"idle" | "awaiting_idea" | "awaiting_region">("idle");
  const [pendingIdea, setPendingIdea] = useState<string>("");

  const recognitionRef = useRef<any>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);
  const prevStepRef = useRef<string | undefined>(currentAgentStep);

  // Initialize Speech Synthesis
  useEffect(() => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      synthRef.current = window.speechSynthesis;
    }
  }, []);

  // Speak response function
  const speak = useCallback((text: string, onEndCallback?: () => void) => {
    setLastResponse(text);
    setShowCaption(true);

    if (isMuted || !synthRef.current) {
      if (onEndCallback) onEndCallback();
      return;
    }

    // Cancel current speech
    synthRef.current.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.05;
    utterance.pitch = 0.95;

    // Pick crisp female/command voice if available
    const voices = synthRef.current.getVoices();
    const preferredVoice = voices.find(
      (v) => v.lang.startsWith("en") && (v.name.includes("Female") || v.name.includes("Samantha") || v.name.includes("Zira") || v.name.includes("Google"))
    ) || voices.find((v) => v.lang.startsWith("en")) || voices[0];

    if (preferredVoice) utterance.voice = preferredVoice;

    utterance.onstart = () => {
      setIsSpeaking(true);
      setIsThinking(false);
    };

    utterance.onend = () => {
      setIsSpeaking(false);
      if (onEndCallback) onEndCallback();
    };

    utterance.onerror = () => {
      setIsSpeaking(false);
      if (onEndCallback) onEndCallback();
    };

    synthRef.current.speak(utterance);
  }, [isMuted]);

  // Upgrade: Interactive Voice Consultation & Operational Speech Processor
  const processVoiceCommand = useCallback((cmdRaw: string) => {
    const cmd = cmdRaw.toLowerCase().trim();
    setTranscript(cmdRaw);
    setIsThinking(true);

    setTimeout(() => {
      // -------------------------------------------------------------
      // 0. ACTIVE CONVERSATIONAL CONSULTATION STEPS
      // -------------------------------------------------------------
      if (consultationStep === "awaiting_idea") {
        if (/(?:cancel|abort|stop|nevermind|exit)/i.test(cmd)) {
          setConsultationStep("idle");
          setPendingIdea("");
          speak("Consultation cancelled, Boss.");
          return;
        }

        const cleanIdea = cmd
          .replace(/^(my\s+idea\s+is|it\s+is|a|an|the|i\s+want\s+to\s+build|i\s+want\s+to\s+start)\s+/i, "")
          .trim();

        if (cleanIdea.length > 2) {
          const formattedIdea = cleanIdea
            .split(" ")
            .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
            .join(" ");

          setPendingIdea(formattedIdea);
          setConsultationStep("awaiting_region");
          speak(`Idea registered: ${formattedIdea}. Which target region should the agents analyze? Options: India, United States, Europe, Southeast Asia, or Global?`);
          return;
        }
      }

      if (consultationStep === "awaiting_region") {
        if (/(?:cancel|abort|stop|nevermind|exit)/i.test(cmd)) {
          setConsultationStep("idle");
          setPendingIdea("");
          speak("Consultation cancelled, Boss.");
          return;
        }

        const selectedRegion = cmd
          .replace(/^(target\s+market|region|in|for|the)\s+/i, "")
          .trim();

        const formattedRegion = selectedRegion
          .split(" ")
          .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
          .join(" ");

        const finalIdea = pendingIdea;
        setConsultationStep("idle");
        setPendingIdea("");

        speak(`Affirmative, Boss. Initiating 8-agent swarm for: ${finalIdea} in target market: ${formattedRegion}.`, () => {
          onStartProject(finalIdea, formattedRegion);
        });
        return;
      }

      // -------------------------------------------------------------
      // 1. FULL APPLICATION SYSTEM CONTROLS
      // -------------------------------------------------------------
      if (/(?:close|hide|exit).*(?:history|drawer)/i.test(cmd)) {
        if (onCloseHistory) onCloseHistory();
        speak("Closing history drawer, Boss.");
        return;
      }

      if (/(?:open|show|view|display)?.*history/i.test(cmd)) {
        if (onOpenHistory) onOpenHistory();
        speak("Opening project history drawer, Boss.");
        return;
      }

      if (/(?:open\s+new\s+blueprint|new\s+blueprint|start\s+new\s+project|new\s+project|create\s+new\s+blueprint|reset\s+workspace)/i.test(cmd)) {
        onNewProject();
        speak("Opening new blueprint workspace. Ready for your next concept, Boss.");
        return;
      }

      if (/(?:close\s+application|close\s+app|close\s+studio|exit\s+app|exit\s+studio|go\s+home|cinematic)/i.test(cmd)) {
        if (onExitStudio) onExitStudio();
        speak("Closing studio application. Returning to main landing module.");
        return;
      }

      if (/(?:mute\s+voice|mute\s+audio|silence|unmute)/i.test(cmd)) {
        setIsMuted((prev) => !prev);
        speak("Audio status toggled.");
        return;
      }

      if (/(?:close\s+caption|hide\s+caption|dismiss\s+text)/i.test(cmd)) {
        setShowCaption(false);
        return;
      }

      if (/(?:help|commands?|shortcuts?|what\s*can\s*you\s*do|guide|manifest)/i.test(cmd)) {
        setShowHelp(true);
        speak("Displaying IRRIS Voice Operations command manifest.");
        return;
      }

      // -------------------------------------------------------------
      // 2. TAB NAVIGATION
      // -------------------------------------------------------------
      if (/(?:executive\s*summary|overview|summary\s*tab)/i.test(cmd)) {
        speak("Loading Executive Summary.");
        onNavigateTab("summary");
        return;
      }

      if (/(?:business\s*category|category|classification|type|anti-pattern)/i.test(cmd)) {
        speak("Opening Business Category & Anti-Patterns breakdown.");
        onNavigateTab("classification");
        return;
      }

      if (/(?:market\s*analysis|market\s*research|tam|sam|som|personas?|customer\s*pain)/i.test(cmd)) {
        speak("Displaying Market Research, TAM, SAM, and SOM metrics.");
        onNavigateTab("market");
        return;
      }

      if (/(?:competitor|competition|rival|market\s*gap|moat)/i.test(cmd)) {
        speak("Loading Competitor Intelligence matrix and defensibility gaps.");
        onNavigateTab("competitors");
        return;
      }

      if (/(?:product\s*spec|mvp|feature|priority\s*matrix)/i.test(cmd)) {
        speak("Displaying MVP Feature Specification & Priority Matrix.");
        onNavigateTab("product");
        return;
      }

      if (/(?:roadmap|schedule|timeline|weeks?|execution\s*plan)/i.test(cmd)) {
        speak("Opening 4-Week Agile Execution Roadmap.");
        onNavigateTab("roadmap");
        return;
      }

      if (/(?:pitch\s*deck|revenue|monetization|business\ model|pitch\s*tab)/i.test(cmd)) {
        speak("Opening VC Pitch Deck & Revenue Streams.");
        onNavigateTab("pitch");
        return;
      }

      if (/(?:validation|scores?|risks?|verdict|mentor|yc)/i.test(cmd)) {
        speak("Loading Validation Assessment & VC Mentor Verdict.");
        onNavigateTab("validation");
        return;
      }

      // -------------------------------------------------------------
      // 3. EXPORT REPORTS & AUDIO NARRATION
      // -------------------------------------------------------------
      if (/(?:download|export|get|save).*(?:pdf|document|report)/i.test(cmd) || cmd === "pdf") {
        speak("Compiling PDF Executive Report for instant download, Boss.");
        onDownloadPdf();
        return;
      }

      if (/(?:download|export|get|save).*(?:ppt|pptx|powerpoint|slide|presentation)/i.test(cmd) || cmd === "ppt") {
        speak("Generating 10-slide PowerPoint Pitch Deck for download.");
        onDownloadPpt();
        return;
      }

      if (/(?:read|speak|narrate|tell\s*me).*(?:summary|executive|overview)/i.test(cmd)) {
        onNavigateTab("summary");
        const text = onReadSummary();
        if (text) speak(`Reading Executive Summary: ${text.slice(0, 300)}...`);
        else speak("Executive Summary loaded, Boss.");
        return;
      }

      if (/(?:read|speak|narrate|tell\s*me).*(?:verdict|validation|mentor)/i.test(cmd)) {
        onNavigateTab("validation");
        const text = onReadValidation();
        if (text) speak(`VC Mentor Verdict: ${text}`);
        else speak("Validation & Mentor report loaded, Boss.");
        return;
      }

      // -------------------------------------------------------------
      // 4. EXPLICIT STARTUP SEARCH & CONSULTATION TRIGGER
      // -------------------------------------------------------------
      const hasCreationKeyword = /(?:search|create|generate|build|make|start\s+(?:a|an)?\s*(?:startup|company|business|project|app))/i.test(cmd);

      if (hasCreationKeyword) {
        let extractedIdea = cmd
          .replace(/^(please|can\s+you|could\s+you|help\s+me|irris|friday|hey|hi)\s+/i, "")
          .replace(/(?:search|create|generate|build|make|start)\s+(?:a|an|the)?\s*(?:startup|company|business|project|app|blueprint)?\s*(?:for|about|called|on)?\s*/i, "")
          .trim();

        // Case A: User said "search" or "create a startup" without specifying an idea
        if (!extractedIdea || extractedIdea.length <= 2) {
          setConsultationStep("awaiting_idea");
          speak("Understood, Boss. Initiating startup consultation. What is the core startup idea or business concept you'd like to analyze?");
          return;
        }

        // Case B: User specified BOTH idea and region in one sentence (e.g. "...in India")
        const regionMatch = extractedIdea.match(/(.*?)\s+(?:in|for|focused\s+on)\s+(india|united\s+states|us|usa|europe|asia|global|southeast\s+asia|uk|canada|latam)$/i);
        if (regionMatch) {
          const mainIdea = regionMatch[1].trim();
          const regionName = regionMatch[2].trim();
          const formattedIdea = mainIdea.split(" ").map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
          const formattedRegion = regionName.toUpperCase();

          speak(`Affirmative, Boss. Initiating 8-agent swarm for: ${formattedIdea} in target market: ${formattedRegion}.`, () => {
            onStartProject(formattedIdea, formattedRegion);
          });
          return;
        }

        // Case C: Idea is specified, ask for Region!
        const formattedIdea = extractedIdea
          .split(" ")
          .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
          .join(" ");

        setPendingIdea(formattedIdea);
        setConsultationStep("awaiting_region");
        speak(`Idea registered: ${formattedIdea}. Which target region or market should we focus on? Options: India, United States, Europe, Southeast Asia, or Global?`);
        return;
      }

      // Default Fallback
      speak("Command not recognized, Boss. To generate a startup, say 'Search [your idea]' or 'Create a startup for [your idea]'. Say 'Help' for controls.");
    }, 400);
  }, [speak, onStartProject, onNavigateTab, onDownloadPdf, onDownloadPpt, onReadSummary, onReadValidation, onNewProject, onOpenHistory, onCloseHistory, onExitStudio, consultationStep, pendingIdea]);




  // Speech Recognition Setup
  const toggleListening = () => {
    if (isListening) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsListening(false);
      setIsThinking(false);
      return;
    }

    if (typeof window === "undefined") return;

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      speak("Speech recognition is not supported in this browser. Please use Chrome or Edge, Boss.");
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = "en-US";

      recognition.onstart = () => {
        setIsListening(true);
        setIsThinking(false);
        setTranscript("Listening...");
      };

      recognition.onresult = (event: any) => {
        const current = event.resultIndex;
        const resultTranscript = event.results[current][0].transcript;
        setTranscript(resultTranscript);

        if (event.results[current].isFinal) {
          setIsListening(false);
          processVoiceCommand(resultTranscript);
        }
      };

      recognition.onerror = (event: any) => {
        console.warn("Speech recognition error:", event.error);
        setIsListening(false);
        setIsThinking(false);
        if (event.error !== "no-speech") {
          speak("Voice input error. Please try clicking the microphone again, Boss.");
        }
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch (err) {
      console.error("Failed to start speech recognition:", err);
      setIsListening(false);
    }
  };

  // Announce live agent step completions
  useEffect(() => {
    if (isExecuting && currentAgentStep && currentAgentStep !== prevStepRef.current) {
      prevStepRef.current = currentAgentStep;
      const stepNames: Record<string, string> = {
        classification: "Idea classification finalized.",
        research: "Market research & TAM metrics complete.",
        competitor: "Competitor intelligence & defensibility gaps identified.",
        product: "MVP feature specification ready.",
        roadmap: "4-Week agile execution roadmap generated.",
        pitch: "VC pitch deck & monetization model compiled.",
        validation: "Validation assessment & mentor verdict ready.",
        quality_control: "Quality control audit complete. Blueprint loaded, Boss."
      };
      if (stepNames[currentAgentStep]) {
        speak(stepNames[currentAgentStep]);
      }
    }
  }, [isExecuting, currentAgentStep, speak]);

  return (
    <>
      {/* Neo-Brutalist HUD Assistant Widget (Fixed Bottom Right) */}
      <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3 font-sans selection:bg-black selection:text-white">
        
        {/* Caption Dialogue Box */}
        {showCaption && (
          <div className="w-72 sm:w-80 p-4 bg-[#fefae0] border-4 border-black shadow-[6px_6px_0px_#000000] relative animate-in fade-in slide-in-from-bottom-3 duration-200">
            <div className="flex items-center justify-between border-b-2 border-black pb-2 mb-2">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 bg-[#f59e0b] border border-black animate-pulse" />
                <span className="text-[11px] font-black uppercase tracking-wider text-black">
                  IRRIS // COMMANDER
                </span>
              </div>
              <button 
                onClick={() => setShowCaption(false)}
                className="p-0.5 hover:bg-black hover:text-white border border-black text-black transition-colors"
                title="Dismiss caption"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Dynamic Status Badges */}
            <div className="flex flex-wrap items-center gap-1.5 mb-2">
              {consultationStep === "awaiting_idea" && (
                <span className="px-2 py-0.5 bg-[#f59e0b] text-black border-2 border-black text-[10px] font-black uppercase tracking-wider animate-pulse">
                  ⚡ STEP 1: TELL ME YOUR IDEA
                </span>
              )}
              {consultationStep === "awaiting_region" && (
                <span className="px-2 py-0.5 bg-[#3b82f6] text-white border-2 border-black text-[10px] font-black uppercase tracking-wider animate-pulse">
                  ⚡ STEP 2: CHOOSE TARGET REGION
                </span>
              )}
              {isListening && (
                <span className="px-2 py-0.5 bg-[#ec4899] text-white border-2 border-black text-[10px] font-black uppercase tracking-wider animate-bounce">
                  ● LISTENING
                </span>
              )}
              {isThinking && (
                <span className="px-2 py-0.5 bg-[#f59e0b] text-black border-2 border-black text-[10px] font-black uppercase tracking-wider animate-pulse">
                  ⚡ PROCESSING COMMAND
                </span>
              )}
              {isSpeaking && (
                <span className="px-2 py-0.5 bg-[#10b981] text-black border-2 border-black text-[10px] font-black uppercase tracking-wider">
                  🔊 TRANSMITTING VOICE
                </span>
              )}
            </div>


            {/* Dialogue / Transcript Content */}
            <p className="text-xs font-black text-black leading-snug">
              {lastResponse}
            </p>

            {transcript && (
              <div className="mt-2 pt-2 border-t-2 border-dashed border-black/40 text-[11px] font-bold text-gray-800 flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5 text-black shrink-0" />
                <span className="italic">"{transcript}"</span>
              </div>
            )}
          </div>
        )}

        {/* Action Controls & Avatar Orb Row */}
        <div className="flex items-center gap-2">
          
          {/* Quick Help Button */}
          <button
            onClick={() => setShowHelp(!showHelp)}
            className="p-3 bg-white text-black border-3 border-black shadow-[4px_4px_0px_#000000] hover:bg-[#fefae0] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0px_#000000] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none transition-all font-black"
            title="Voice Commands Guide"
          >
            <HelpCircle className="w-5 h-5 stroke-[2.5]" />
          </button>

          {/* Mute Audio Toggle Button */}
          <button
            onClick={() => {
              setIsMuted(!isMuted);
              if (synthRef.current) synthRef.current.cancel();
            }}
            className={`p-3 border-3 border-black shadow-[4px_4px_0px_#000000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0px_#000000] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none transition-all font-black ${
              isMuted ? "bg-rose-500 text-white" : "bg-white text-black hover:bg-[#fefae0]"
            }`}
            title={isMuted ? "Unmute IRRIS Voice" : "Mute IRRIS Voice"}
          >
            {isMuted ? <VolumeX className="w-5 h-5 stroke-[2.5]" /> : <Volume2 className="w-5 h-5 stroke-[2.5]" />}
          </button>

          {/* Main Floating Neo-Brutalist IRRIS Avatar & Microphone Button */}
          <button
            onClick={toggleListening}
            className={`relative group p-4 border-4 border-black shadow-[6px_6px_0px_#000000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[3px_3px_0px_#000000] active:translate-x-[6px] active:translate-y-[6px] active:shadow-none transition-all flex items-center justify-center ${
              isListening
                ? "bg-[#ec4899] text-white animate-pulse"
                : isSpeaking
                ? "bg-[#10b981] text-black"
                : isThinking
                ? "bg-[#f59e0b] text-black"
                : "bg-[#000000] text-white hover:bg-[#18181b]"
            }`}
            title={isListening ? "Listening... Click to stop" : "Click to give voice command to IRRIS"}
          >
            {/* Equalizer Wave / Mic Core */}
            <div className="flex items-center gap-1.5 h-6 px-1">
              <span className={`w-1.5 bg-current border border-black transition-all duration-150 ${isSpeaking || isListening ? "h-6 animate-pulse" : "h-3"}`} />
              <span className={`w-1.5 bg-current border border-black transition-all duration-150 ${isSpeaking || isListening ? "h-4 animate-bounce" : "h-5"}`} />
              
              <div className="mx-1">
                <Mic className={`w-6 h-6 stroke-[3] ${isListening ? "scale-110 text-white" : ""}`} />
              </div>

              <span className={`w-1.5 bg-current border border-black transition-all duration-150 ${isSpeaking || isListening ? "h-5 animate-bounce" : "h-4"}`} />
              <span className={`w-1.5 bg-current border border-black transition-all duration-150 ${isSpeaking || isListening ? "h-6 animate-pulse" : "h-3"}`} />
            </div>

            {/* Glowing Status Ring */}
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-[#f59e0b] border-2 border-black flex items-center justify-center text-[8px] font-black text-black">
              ★
            </span>
          </button>
        </div>
      </div>

      {/* Neo-Brutalist Voice Commands Help Drawer / Modal */}
      {showHelp && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white border-4 border-black shadow-[10px_10px_0px_#000000] w-full max-w-xl p-6 sm:p-8 relative animate-in zoom-in-95 duration-150 max-h-[90vh] overflow-y-auto">
            
            {/* Modal Header */}
            <div className="flex items-center justify-between border-b-4 border-black pb-4 mb-6">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-[#f59e0b] border-3 border-black shadow-[3px_3px_0px_#000000] flex items-center justify-center font-black text-black">
                  <Command className="w-6 h-6 stroke-[3]" />
                </div>
                <div>
                  <h3 className="text-lg font-black uppercase text-black">
                    IRRIS // COMMAND MANIFEST
                  </h3>
                  <p className="text-xs font-bold text-gray-700">
                    AI Operations Commander Voice Shortcuts
                  </p>
                </div>
              </div>
              <button
                onClick={() => setShowHelp(false)}
                className="p-2 bg-rose-500 text-white border-3 border-black shadow-[3px_3px_0px_#000000] hover:bg-rose-600 active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all font-black"
              >
                <X className="w-5 h-5 stroke-[3]" />
              </button>
            </div>

            {/* Supported Commands Grid */}
            <div className="space-y-4 text-xs font-bold text-black">
              
              {/* Category 1: Generation */}
              <div className="p-4 bg-[#fefae0] border-3 border-black shadow-[4px_4px_0px_#000000]">
                <h4 className="font-black text-black uppercase tracking-wider mb-2 flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-black stroke-[3]" />
                  <span>Blueprint Generation</span>
                </h4>
                <div className="space-y-1.5">
                  <div className="p-2 bg-white border-2 border-black flex items-center justify-between">
                    <span className="font-black text-black">"Create a startup for [your idea]"</span>
                    <span className="text-[10px] bg-black text-white px-2 py-0.5 font-black">AUTO EXECUTE</span>
                  </div>
                  <div className="p-2 bg-white border-2 border-black flex items-center justify-between">
                    <span className="font-black text-black">"Generate blueprint"</span>
                    <span className="text-[10px] bg-black text-white px-2 py-0.5 font-black">LAUNCH SWARM</span>
                  </div>
                </div>
              </div>

              {/* Category 2: Navigation */}
              <div className="p-4 bg-white border-3 border-black shadow-[4px_4px_0px_#000000]">
                <h4 className="font-black text-black uppercase tracking-wider mb-2 flex items-center gap-2">
                  <Activity className="w-4 h-4 text-black stroke-[3]" />
                  <span>Tab Navigation Shortcuts</span>
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {["Show executive summary", "Show business category", "Show market analysis", "Show competitors", "Open product spec", "Open roadmap", "Open pitch deck", "Open validation"].map((cmd, i) => (
                    <div key={i} className="p-2 bg-[#f3f4f6] border-2 border-black text-[11px] font-black">
                      "{cmd}"
                    </div>
                  ))}
                </div>
              </div>

              {/* Category 3: Downloads & Audio */}
              <div className="p-4 bg-[#10b981]/20 border-3 border-black shadow-[4px_4px_0px_#000000]">
                <h4 className="font-black text-black uppercase tracking-wider mb-2 flex items-center gap-2">
                  <FileText className="w-4 h-4 text-black stroke-[3]" />
                  <span>Reports & Audio Narration</span>
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  <div className="p-2 bg-white border-2 border-black">
                    <span className="font-black">"Download PDF"</span> / <span className="font-black">"Download PPT"</span>
                  </div>
                  <div className="p-2 bg-white border-2 border-black">
                    <span className="font-black">"Read executive summary"</span>
                  </div>
                  <div className="p-2 bg-white border-2 border-black">
                    <span className="font-black">"Read validation verdict"</span>
                  </div>
                  <div className="p-2 bg-white border-2 border-black">
                    <span className="font-black">"Start new project"</span>
                  </div>
                </div>
              </div>

            </div>

            {/* Footer */}
            <div className="mt-6 pt-4 border-t-3 border-black flex justify-end">
              <button
                onClick={() => setShowHelp(false)}
                className="px-6 py-2.5 bg-[#f59e0b] text-black border-3 border-black shadow-[4px_4px_0px_#000000] hover:bg-[#d97706] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all font-black uppercase text-xs tracking-wider"
              >
                Acknowledge // Close
              </button>
            </div>

          </div>
        </div>
      )}
    </>
  );
}
