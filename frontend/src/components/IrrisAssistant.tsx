import React, { useState, useEffect, useRef, useCallback } from "react";
import { 
  Mic, MicOff, Volume2, VolumeX, HelpCircle, X, Sparkles, 
  Terminal, Shield, Play, FileText, Presentation, Activity, Command,
  MessageSquare, Send, Radio, ChevronDown, ChevronUp
} from "lucide-react";
import { chatWithIrris } from "@/lib/api";

export interface ChatMessage {
  id: string;
  sender: "user" | "irris";
  text: string;
  timestamp: string;
  action?: string;
}

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
  
  // Chatbot Intelligence Feed Box & Auto-Listen State
  const [showChatFeed, setShowChatFeed] = useState<boolean>(true);
  const [textInput, setTextInput] = useState<string>("");
  const [autoListen, setAutoListen] = useState<boolean>(true);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome-1",
      sender: "irris",
      text: "IRRIS AI Operations Commander online. Ask for startup ideas, market analysis, or give operational commands naturally.",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const chatScrollRef = useRef<HTMLDivElement | null>(null);

  // Multi-Step Conversational Onboarding Consultation State
  const [consultationStep, setConsultationStep] = useState<"idle" | "awaiting_idea" | "awaiting_region">("idle");
  const [pendingIdea, setPendingIdea] = useState<string>("");

  const recognitionRef = useRef<any>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);
  const prevStepRef = useRef<string | undefined>(currentAgentStep);


  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);

  // Asynchronously load and store available browser/OS voices
  useEffect(() => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      synthRef.current = window.speechSynthesis;

      const updateVoices = () => {
        if (synthRef.current) {
          const loaded = synthRef.current.getVoices();
          setVoices(loaded);
        }
      };

      updateVoices();
      if (synthRef.current.onvoiceschanged !== undefined) {
        synthRef.current.onvoiceschanged = updateVoices;
      }
    }
  }, []);

  // Helper to append message to Chatbot Intelligence Feed Box
  const addMessage = useCallback((sender: "user" | "irris", text: string, action?: string) => {
    const newMsg: ChatMessage = {
      id: Date.now().toString() + Math.random().toString().slice(2, 6),
      sender,
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      action
    };
    setMessages((prev) => [...prev, newMsg]);
    setTimeout(() => {
      if (chatScrollRef.current) {
        chatScrollRef.current.scrollTop = chatScrollRef.current.scrollHeight;
      }
    }, 50);
  }, []);

  // Speak response function with Alexa/Siri-like Neural Voice Selection & Chat Logging
  const speak = useCallback((text: string, onEndCallback?: () => void, isWarm?: boolean) => {
    setLastResponse(text);
    setShowCaption(true);
    addMessage("irris", text);

    if (isMuted || !synthRef.current) {
      if (onEndCallback) onEndCallback();
      return;
    }

    // Cancel current speech
    synthRef.current.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    if (isWarm) {
      utterance.rate = 0.95;
      utterance.pitch = 1.02;
    } else {
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
    }

    // Pick top Alexa/Siri-like Neural Voice
    const available = voices.length > 0 ? voices : (synthRef.current ? synthRef.current.getVoices() : []);
    
    const preferredVoice = available.find(
      (v) => v.lang.startsWith("en") && (
        v.name.includes("Natural") || 
        v.name.includes("Neural") || 
        v.name.includes("Jenny") || 
        v.name.includes("Aria") || 
        v.name.includes("Samantha") || 
        v.name.includes("Siri") || 
        v.name.includes("Google US English") || 
        v.name.includes("Google UK English Female")
      )
    ) || available.find(
      (v) => v.lang.startsWith("en") && (v.name.includes("Female") || v.name.includes("Google") || v.name.includes("Zira"))
    ) || available.find((v) => v.lang.startsWith("en")) || available[0];

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
  }, [isMuted, voices, addMessage]);

  // Upgrade: Hybrid Instant Direct Controller + Conversational AI LLM Engine
  const processVoiceCommand = useCallback(async (cmdRaw: string) => {
    const rawTrimmed = cmdRaw.trim();
    if (!rawTrimmed) return;

    // Strip wake-word "irris" or "hey irris" if spoken at the beginning
    let cleanSpeech = rawTrimmed.replace(/^(hey\s+)?irris[\s,.:!]*/i, "").trim();
    if (!cleanSpeech) cleanSpeech = rawTrimmed;

    setTranscript(cleanSpeech);
    addMessage("user", cleanSpeech);
    setIsThinking(true);

    const cleanCmd = cleanSpeech.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").trim();


    // -------------------------------------------------------------
    // 0. ACTIVE CONSULTATION STEPS
    // -------------------------------------------------------------
    if (consultationStep === "awaiting_idea") {
      if (/(?:cancel|abort|stop|nevermind|exit)/i.test(cleanCmd)) {
        setConsultationStep("idle");
        setPendingIdea("");
        speak("Consultation cancelled, Boss.");
        setIsThinking(false);
        return;
      }

      const cleanIdea = cleanCmd
        .replace(/^(my\s+idea\s+is|it\s+is|a|an|the|i\s+want\s+to\s+build|i\s+want\s+to\s+start|i\s+was\s+thinking\s+of|how\s+about)\s+/i, "")
        .trim();

      if (cleanIdea.length > 2) {
        const formattedIdea = cleanIdea
          .split(" ")
          .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
          .join(" ");

        setPendingIdea(formattedIdea);
        setConsultationStep("awaiting_region");
        speak(`Idea registered: ${formattedIdea}. Which target region should the agents analyze? Options: India, United States, Europe, Southeast Asia, or Global?`);
        setIsThinking(false);
        return;
      }
    }

    if (consultationStep === "awaiting_region") {
      if (/(?:cancel|abort|stop|nevermind|exit)/i.test(cleanCmd)) {
        setConsultationStep("idle");
        setPendingIdea("");
        speak("Consultation cancelled, Boss.");
        setIsThinking(false);
        return;
      }

      const selectedRegion = cleanCmd
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
      setIsThinking(false);
      return;
    }

    // -------------------------------------------------------------
    // 1. INSTANT DIRECT APP CONTROLS (Zero Latency, 100% Reliable)
    // -------------------------------------------------------------
    if (/(?:close|hide|exit|dismiss).*(?:history|drawer|sidebar)/i.test(cleanCmd)) {
      if (onCloseHistory) onCloseHistory();
      speak("Closing history drawer, Boss.");
      setIsThinking(false);
      return;
    }

    if (/(?:open|show|view|display|check|my).*(?:history|past\s+projects|saved|blueprints|projects)/i.test(cleanCmd) || cleanCmd === "history") {
      if (onOpenHistory) onOpenHistory();
      speak("Opening project history drawer, Boss.");
      setIsThinking(false);
      return;
    }

    if (/(?:open\s+new\s+blueprint|new\s+blueprint|start\s+new\s+project|new\s+project|create\s+new\s+blueprint|reset\s+workspace|clear|fresh\s+start)/i.test(cleanCmd)) {
      setConsultationStep("idle");
      setPendingIdea("");
      onNewProject();
      speak("Opening new blueprint workspace. Ready for your next concept, Boss.");
      setIsThinking(false);
      return;
    }

    if (/(?:close\s+application|close\s+app|close\s+studio|exit\s+app|exit\s+studio|go\s+home|cinematic|landing\s+page)/i.test(cleanCmd)) {
      if (onExitStudio) onExitStudio();
      speak("Closing studio application. Returning to main landing module.");
      setIsThinking(false);
      return;
    }

    if (/(?:mute|unmute|silence|quiet|audio\s+off|audio\s+on)/i.test(cleanCmd)) {
      setIsMuted((prev) => !prev);
      speak("Audio status toggled.");
      setIsThinking(false);
      return;
    }

    if (/(?:close\s+caption|hide\s+caption|dismiss\s+text|hide\s+box)/i.test(cleanCmd)) {
      setShowCaption(false);
      setIsThinking(false);
      return;
    }

    if (/(?:help|commands?|shortcuts?|what\s*can\s*you\s*do|guide|manifest|capabilities|instructions)/i.test(cleanCmd)) {
      setShowHelp(true);
      speak("Displaying IRRIS Voice Operations command manifest. You can control navigation, trigger blueprints, and export reports.");
      setIsThinking(false);
      return;
    }

    // -------------------------------------------------------------
    // 2. INSTANT TAB NAVIGATION CONTROLS
    // -------------------------------------------------------------
    if (/(?:executive\s*summary|overview|summary|front\s*page|home\s*tab|main\s*page)/i.test(cleanCmd)) {
      speak("Loading Executive Summary.");
      onNavigateTab("summary");
      setIsThinking(false);
      return;
    }

    if (/(?:business\s*category|category|classification|type|anti-patterns?|business\s*model\s*type)/i.test(cleanCmd)) {
      speak("Opening Business Category & Anti-Patterns breakdown.");
      onNavigateTab("classification");
      setIsThinking(false);
      return;
    }

    if (/(?:market\s*analysis|market\s*research|tam|sam|som|market\s*size|personas?|user\s*pain|customers?|target\s*audience)/i.test(cleanCmd)) {
      speak("Displaying Market Research, TAM, SAM, and SOM metrics.");
      onNavigateTab("market");
      setIsThinking(false);
      return;
    }

    if (/(?:competitor|competition|rivals?|market\s*gap|moat|defensibility|who\s+are\s+the\s+competitors)/i.test(cleanCmd)) {
      speak("Loading Competitor Intelligence matrix and defensibility gaps.");
      onNavigateTab("competitors");
      setIsThinking(false);
      return;
    }

    if (/(?:product\s*spec|mvp|features?|priority\s*matrix|what\s+to\s+build|specification)/i.test(cleanCmd)) {
      speak("Displaying MVP Feature Specification & Priority Matrix.");
      onNavigateTab("product");
      setIsThinking(false);
      return;
    }

    if (/(?:roadmap|schedule|timeline|weeks?|execution\s*plan|action\s*items?)/i.test(cleanCmd)) {
      speak("Opening 4-Week Agile Execution Roadmap.");
      onNavigateTab("roadmap");
      setIsThinking(false);
      return;
    }

    if (/(?:pitch\s*deck|slides?|presentation|revenue|monetization|business\s*model|how\s+will\s+we\s+make\s+money|pitch\s*tab)/i.test(cleanCmd)) {
      speak("Opening VC Pitch Deck & Revenue Streams.");
      onNavigateTab("pitch");
      setIsThinking(false);
      return;
    }

    if (/(?:validation|scores?|risks?|verdict|mentor|yc|is\s+this\s+a\s+good\s+idea|viability)/i.test(cleanCmd)) {
      speak("Loading Validation Assessment & VC Mentor Verdict.");
      onNavigateTab("validation");
      setIsThinking(false);
      return;
    }

    // -------------------------------------------------------------
    // 3. INSTANT REPORT EXPORTS
    // -------------------------------------------------------------
    if (/(?:download|export|get|save).*(?:pdf|document|report)/i.test(cleanCmd) || cleanCmd === "pdf") {
      speak("Compiling PDF Executive Report for instant download, Boss.");
      onDownloadPdf();
      setIsThinking(false);
      return;
    }

    if (/(?:download|export|get|save).*(?:ppt|pptx|powerpoint|slide|presentation)/i.test(cleanCmd) || cleanCmd === "ppt") {
      speak("Generating 10-slide PowerPoint Pitch Deck for download.");
      onDownloadPpt();
      setIsThinking(false);
      return;
    }

    // -------------------------------------------------------------
    // 4. CONVERSATIONAL AI LLM BRAIN (For Smalltalk, Founder Empathy, Ideas & Q&A)
    // -------------------------------------------------------------
    try {
      const res = await chatWithIrris(
        cmdRaw, 
        projectIdea, 
        activeTab, 
        consultationStep, 
        pendingIdea
      );

      const reply = res.reply || "I am online and ready for your operational commands, Boss.";
      const action = res.action;
      const payload = res.payload || {};

      speak(reply, () => {
        if (action === "START_PROJECT" && payload.idea) {
          setConsultationStep("idle");
          setPendingIdea("");
          onStartProject(payload.idea, payload.target_market || "Global");
        } else if (action === "ASK_REGION" && payload.idea) {
          setPendingIdea(payload.idea);
          setConsultationStep("awaiting_region");
        }
      }, true);

    } catch (err) {
      console.warn("Conversational AI backend fallback:", err);
      speak("Command acknowledged, Boss. Tell me your startup idea or say 'Help' for system controls.", undefined, true);
    } finally {
      setIsThinking(false);
    }
  }, [speak, onStartProject, onNavigateTab, onDownloadPdf, onDownloadPpt, onReadSummary, onReadValidation, onNewProject, onOpenHistory, onCloseHistory, onExitStudio, consultationStep, pendingIdea, projectIdea, activeTab]);



  // Speech Recognition & Auto-Listen Setup
  const toggleListening = () => {
    if (isListening) {
      setAutoListen(false);
      if (recognitionRef.current) {
        try { recognitionRef.current.stop(); } catch {}
      }
      setIsListening(false);
      setIsThinking(false);
      return;
    }

    setAutoListen(true);
    startRecognition();
  };

  const startRecognition = () => {
    if (typeof window === "undefined") return;

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      speak("Speech recognition is not supported in this browser. Please use Chrome or Edge, Boss.");
      return;
    }

    try {
      if (recognitionRef.current) {
        try { recognitionRef.current.stop(); } catch {}
      }

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
        setIsListening(false);
        setIsThinking(false);
      };

      recognition.onend = () => {
        setIsListening(false);
        // Auto-restart recognition if autoListen mode is active
        if (autoListen && !isSpeaking && !isThinking) {
          setTimeout(() => {
            try { recognition.start(); } catch {}
          }, 300);
        }
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch (err) {
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
        
        {/* Chatbot Intelligence Feed Box (Scrollable Log + Text Input) */}
        {showCaption && (
          <div className="w-80 sm:w-96 p-4 bg-[#fefae0] border-4 border-black shadow-[6px_6px_0px_#000000] relative animate-in fade-in slide-in-from-bottom-3 duration-200">
            <div className="flex items-center justify-between border-b-2 border-black pb-2 mb-2">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 bg-[#f59e0b] border border-black animate-pulse" />
                <span className="text-[11px] font-black uppercase tracking-wider text-black">
                  IRRIS // CHAT & INTELLIGENCE FEED
                </span>
              </div>
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setShowChatFeed(!showChatFeed)}
                  className="p-1 hover:bg-black hover:text-white border border-black text-black transition-colors"
                  title={showChatFeed ? "Collapse Feed" : "Expand Feed"}
                >
                  {showChatFeed ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                </button>
                <button 
                  onClick={() => setShowCaption(false)}
                  className="p-1 hover:bg-black hover:text-white border border-black text-black transition-colors"
                  title="Dismiss HUD"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            {/* Dynamic Status Badges */}
            <div className="flex flex-wrap items-center gap-1.5 mb-2">
              <button 
                onClick={() => setAutoListen(!autoListen)}
                className={`px-2 py-0.5 border-2 border-black text-[10px] font-black uppercase tracking-wider flex items-center gap-1 transition-all ${
                  autoListen ? "bg-black text-white" : "bg-gray-200 text-gray-700"
                }`}
                title="Toggle Auto-Listen / Wake-Word mode"
              >
                <Radio className={`w-2.5 h-2.5 ${autoListen ? "text-[#10b981] animate-pulse" : "text-gray-400"}`} />
                WAKE-WORD: "IRRIS"
              </button>
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

            {/* Expandable Chat Log Feed */}
            {showChatFeed && (
              <div 
                ref={chatScrollRef}
                className="max-h-64 overflow-y-auto space-y-2 bg-[#fffdf0] border-2 border-black p-2.5 mb-3 font-mono"
              >
                {messages.map((m) => (
                  <div 
                    key={m.id}
                    className={`p-2 border-2 border-black text-xs font-bold ${
                      m.sender === "user"
                        ? "bg-[#10b981]/20 text-black border-black text-right ml-6"
                        : "bg-black text-white border-black text-left mr-2"
                    }`}
                  >
                    <div className="flex items-center justify-between text-[9px] opacity-70 mb-1 font-sans">
                      <span>{m.sender === "user" ? "YOU" : "IRRIS COMMANDER"}</span>
                      <span>{m.timestamp}</span>
                    </div>
                    <p className="whitespace-pre-wrap leading-relaxed font-sans">{m.text}</p>
                  </div>
                ))}
              </div>
            )}

            {/* Text & Voice Command Bar */}
            <div className="flex items-center gap-1.5 border-2 border-black bg-white p-1">
              <input
                type="text"
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && textInput.trim()) {
                    const val = textInput.trim();
                    setTextInput("");
                    processVoiceCommand(val);
                  }
                }}
                placeholder="Type command or say 'IRRIS'..."
                className="flex-1 px-2 py-1 text-xs font-bold text-black outline-none placeholder:text-gray-500"
              />
              <button
                onClick={() => {
                  if (textInput.trim()) {
                    const val = textInput.trim();
                    setTextInput("");
                    processVoiceCommand(val);
                  }
                }}
                className="px-2.5 py-1 bg-black text-white hover:bg-zinc-800 border border-black text-xs font-black uppercase transition-colors"
                title="Send command"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}

        {/* Action Controls & Avatar Orb Row */}
        <div className="flex items-center gap-2">
          
          {/* Quick Chat Feed Toggle Button */}
          <button
            onClick={() => {
              setShowCaption(true);
              setShowChatFeed(!showChatFeed);
            }}
            className="p-3 bg-white text-black border-3 border-black shadow-[4px_4px_0px_#000000] hover:bg-[#fefae0] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0px_#000000] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none transition-all font-black relative"
            title="Toggle IRRIS Chat & Feed"
          >
            <MessageSquare className="w-5 h-5 stroke-[2.5]" />
            {messages.length > 0 && (
              <span className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-[#ec4899] text-white border border-black rounded-full text-[9px] font-black flex items-center justify-center">
                {messages.length}
              </span>
            )}
          </button>

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
            title={isListening ? "Listening... Click to pause auto-listen" : "Click to wake up IRRIS voice assistant"}
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
