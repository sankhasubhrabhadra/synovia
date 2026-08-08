import React, { useState, useEffect, useRef, useCallback } from "react";
import { 
  Mic, MicOff, Volume2, VolumeX, HelpCircle, X, Sparkles, 
  Terminal, Shield, Play, FileText, Presentation, Activity, Command,
  MessageSquare, Send, Radio, ChevronDown, ChevronUp
} from "lucide-react";
import { chatWithIrris } from "@/lib/api";

export interface ChatMessage {
  id: string;
  sender: "user" | "blue";
  text: string;
  timestamp: string;
  action?: string;
}

export interface IrrisAssistantProps {
  onStartProject: (idea: string, targetMarket?: string) => void;
  onNavigateTab: (tab: string) => void;
  onDownloadPdf: () => void;
  onDownloadPpt: () => void;
  onReadSummary: () => string | void;
  onReadValidation: () => string | void;
  onNewProject: () => void;
  onOpenHistory?: () => void;
  onCloseHistory?: () => void;
  onOpenHistoryIndex?: (index: number) => void;
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
  onOpenHistoryIndex,
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
  const [lastResponse, setLastResponse] = useState<string>("BLUE // Online. Ready for operational commands, Boss.");
  const [showCaption, setShowCaption] = useState<boolean>(true);
  
  // Chatbot Intelligence Feed Box & Listening State (No Auto-Restart Chatter)
  const [showChatFeed, setShowChatFeed] = useState<boolean>(true);
  const [textInput, setTextInput] = useState<string>("");
  const [autoListen, setAutoListen] = useState<boolean>(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome-1",
      sender: "blue",
      text: "BLUE AI Commander online. Say 'Hey Blue', tap the mic, or type 'search this idea [your idea]' to generate startup blueprints.",
      timestamp: "10:00 AM"
    }
  ]);
  const chatScrollRef = useRef<HTMLDivElement | null>(null);

  // State Refs to prevent stale closures in Web Speech callbacks
  const autoListenRef = useRef(autoListen);
  const isSpeakingRef = useRef(isSpeaking);
  const isThinkingRef = useRef(isThinking);

  useEffect(() => { autoListenRef.current = autoListen; }, [autoListen]);
  useEffect(() => { isSpeakingRef.current = isSpeaking; }, [isSpeaking]);
  useEffect(() => { isThinkingRef.current = isThinking; }, [isThinking]);

  const recognitionRef = useRef<any>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);
  const prevStepRef = useRef<string | undefined>(currentAgentStep);
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);

  // Load available browser/OS voices
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
  const addMessage = useCallback((sender: "user" | "blue", text: string, action?: string) => {
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

  // Speak response function with MALE Neural Voice Selection
  const speak = useCallback((text: string, onEndCallback?: () => void) => {
    setLastResponse(text);
    setShowCaption(true);
    addMessage("blue", text);

    if (isMuted || !synthRef.current) {
      if (onEndCallback) onEndCallback();
      return;
    }

    // Cancel current speech
    synthRef.current.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 0.95; // Slightly deeper male tone

    // Pick top MALE Neural Voice
    const available = voices.length > 0 ? voices : (synthRef.current ? synthRef.current.getVoices() : []);
    
    const preferredVoice = available.find(
      (v) => v.lang.startsWith("en") && (
        v.name.includes("Male") || 
        v.name.includes("David") || 
        v.name.includes("Guy") || 
        v.name.includes("George") || 
        v.name.includes("Ryan") || 
        v.name.includes("Google US English Male") ||
        v.name.includes("Microsoft David") ||
        v.name.includes("Microsoft Guy") ||
        v.name.includes("Daniel") ||
        v.name.includes("James")
      )
    ) || available.find(
      (v) => v.lang.startsWith("en") && (!v.name.includes("Female") && !v.name.includes("Zira") && !v.name.includes("Jenny"))
    ) || available.find((v) => v.lang.startsWith("en")) || available[0];

    if (preferredVoice) utterance.voice = preferredVoice;

    utterance.onstart = () => {
      setIsSpeaking(true);
      setIsThinking(false);
      // Stop mic recognition while BLUE is speaking to avoid hearing himself
      if (recognitionRef.current) {
        try { recognitionRef.current.stop(); } catch {}
      }
    };

    utterance.onend = () => {
      setIsSpeaking(false);
      if (onEndCallback) onEndCallback();
      // Auto-turn on mic after BLUE finishes speaking so user can speak immediately
      setTimeout(() => {
        if (!isMuted) {
          startRecognition();
        }
      }, 400);
    };

    utterance.onerror = () => {
      setIsSpeaking(false);
      if (onEndCallback) onEndCallback();
    };

    synthRef.current.speak(utterance);
  }, [isMuted, voices, addMessage]);

  // Command Processor: Exact operational controls & search execution
  const processVoiceCommand = useCallback(async (cmdRaw: string) => {
    const rawTrimmed = cmdRaw.trim();
    if (!rawTrimmed) return;

    // Wake-Word Matching: "hey blue", "hi blue", "blue", "ok blue"
    const wakeWordRegex = /^(?:hey|hi|hello|ok|okay)?\s*(?:blue|bloo|bleu)[\s,.:!]*/i;
    let cleanSpeech = rawTrimmed.replace(wakeWordRegex, "").trim();
    const isWakeWordOnly = !cleanSpeech || cleanSpeech.toLowerCase() === "blue" || cleanSpeech.toLowerCase() === "hey blue";
    if (!cleanSpeech) cleanSpeech = rawTrimmed;

    setTranscript(cleanSpeech);
    addMessage("user", cleanSpeech);
    setIsThinking(true);

    const cleanCmd = cleanSpeech.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").trim();

    // If user just called "blue" or "hey blue", activate mic & acknowledge!
    if (isWakeWordOnly || cleanCmd === "blue" || cleanCmd === "hey blue" || cleanCmd === "hi blue") {
      speak("Yes Boss? BLUE online and listening.");
      setIsThinking(false);
      return;
    }


    // -------------------------------------------------------------
    // 1. SEARCH THIS IDEA / STARTUP RESULT COMMANDS
    // -------------------------------------------------------------
    const searchMatch = cleanCmd.match(/(?:search\s+(?:this\s+)?idea|search\s+for\s+(?:startup\s+result\s+for\s+)?|search\s+for|search|find\s+startup\s+for|analyze\s+idea|generate\s+blueprint\s+for)\s+(.+)/i);
    if (searchMatch && searchMatch[1]) {
      const targetIdea = searchMatch[1].trim();
      if (targetIdea.length > 1) {
        speak(`Searching startup results and initiating agent swarm for: ${targetIdea}, Boss.`);
        onStartProject(targetIdea, "Global");
        setIsThinking(false);
        return;
      }
    }

    // -------------------------------------------------------------
    // 2. OPEN SPECIFIC HISTORY ITEM BY INDEX NUMBER ("open number 1 result from history box")
    // -------------------------------------------------------------
    const historyIndexMatch = cleanCmd.match(/(?:open|show|load|view)\s+(?:this\s+|number\s+|num\s+)?(\d+)(?:st|nd|rd|th)?\s*(?:result|project|blueprint|item)?(?:\s*from\s*history\s*box|\s*from\s*history)?/i) ||
                              cleanCmd.match(/open\s+(\d+)(?:st|nd|rd|th)?\s+result/i);
    if (historyIndexMatch && historyIndexMatch[1] && onOpenHistoryIndex) {
      const idx = parseInt(historyIndexMatch[1], 10);
      if (idx > 0) {
        speak(`Loading result number ${idx} from history box, Boss.`);
        onOpenHistoryIndex(idx - 1); // 1-indexed to 0-indexed
        setIsThinking(false);
        return;
      }
    }

    // -------------------------------------------------------------
    // 3. NAVIGATE TO HISTORY BOX / OPEN HISTORY
    // -------------------------------------------------------------
    if (/(?:navigate\s+to\s+history\s+box|navigate\s+to\s+history|open\s+history\s+box|open\s+history|show\s+history|history\s+box|history)/i.test(cleanCmd)) {
      if (onOpenHistory) onOpenHistory();
      speak("Navigating to history box, Boss.");
      setIsThinking(false);
      return;
    }

    if (/(?:close|hide|exit|dismiss).*(?:history|drawer|sidebar)/i.test(cleanCmd)) {
      if (onCloseHistory) onCloseHistory();
      speak("Closing history box, Boss.");
      setIsThinking(false);
      return;
    }

    // -------------------------------------------------------------
    // 4. CLOSE STUDIO COMMAND
    // -------------------------------------------------------------
    if (/(?:close\s+studio|exit\s+studio|close\s+application|close\s+app|exit\s+app|go\s+home)/i.test(cleanCmd)) {
      if (onExitStudio) onExitStudio();
      speak("Closing studio application. Returning to home module, Boss.");
      setIsThinking(false);
      return;
    }

    if (/(?:open\s+new\s+blueprint|new\s+blueprint|start\s+new\s+project|new\s+project|reset\s+workspace|fresh\s+start)/i.test(cleanCmd)) {
      onNewProject();
      speak("Opening new blueprint workspace. Ready for your next concept, Boss.");
      setIsThinking(false);
      return;
    }

    // -------------------------------------------------------------
    // 5. TAB NAVIGATION CONTROLS
    // -------------------------------------------------------------
    if (/(?:executive\s*summary|overview|summary|front\s*page|main\s*page)/i.test(cleanCmd)) {
      speak("Loading Executive Summary.");
      onNavigateTab("summary");
      setIsThinking(false);
      return;
    }

    if (/(?:business\s*category|category|classification|type|anti-patterns?)/i.test(cleanCmd)) {
      speak("Opening Business Category breakdown.");
      onNavigateTab("classification");
      setIsThinking(false);
      return;
    }

    if (/(?:market\s*analysis|market\s*research|tam|sam|som|market\s*size)/i.test(cleanCmd)) {
      speak("Displaying Market Research, TAM, SAM, and SOM metrics.");
      onNavigateTab("market");
      setIsThinking(false);
      return;
    }

    if (/(?:competitor|competition|rivals?|market\s*gap|moat|defensibility)/i.test(cleanCmd)) {
      speak("Loading Competitor Intelligence matrix.");
      onNavigateTab("competitors");
      setIsThinking(false);
      return;
    }

    if (/(?:product\s*spec|mvp|features?|priority\s*matrix)/i.test(cleanCmd)) {
      speak("Displaying MVP Feature Specification.");
      onNavigateTab("product");
      setIsThinking(false);
      return;
    }

    if (/(?:roadmap|schedule|timeline|weeks?|execution\s*plan)/i.test(cleanCmd)) {
      speak("Opening 4-Week Execution Roadmap.");
      onNavigateTab("roadmap");
      setIsThinking(false);
      return;
    }

    if (/(?:pitch\s*deck|slides?|presentation|revenue|monetization)/i.test(cleanCmd)) {
      speak("Opening Pitch Deck & Revenue Streams.");
      onNavigateTab("pitch");
      setIsThinking(false);
      return;
    }

    if (/(?:validation|scores?|risks?|verdict|mentor|yc|viability)/i.test(cleanCmd)) {
      speak("Loading Validation Assessment & Verdict.");
      onNavigateTab("validation");
      setIsThinking(false);
      return;
    }

    // EXPORTS
    if (/(?:download|export).*(?:pdf|document|report)/i.test(cleanCmd) || cleanCmd === "pdf") {
      speak("Compiling PDF Executive Report for download, Boss.");
      onDownloadPdf();
      setIsThinking(false);
      return;
    }

    if (/(?:download|export).*(?:ppt|pptx|presentation)/i.test(cleanCmd) || cleanCmd === "ppt") {
      speak("Generating 10-slide PowerPoint Pitch Deck.");
      onDownloadPpt();
      setIsThinking(false);
      return;
    }

    // FALLBACK / BACKEND INTELLIGENCE CHAT
    try {
      const res = await chatWithIrris(cmdRaw, projectIdea, activeTab);
      const reply = res.reply || "Ready for your commands, Boss. Say 'search this idea [idea]' to analyze a project.";
      speak(reply);
    } catch (err) {
      speak("Command acknowledged, Boss. Say 'search this idea [idea]' or 'navigate to history box'.");
    } finally {
      setIsThinking(false);
    }
  }, [speak, onStartProject, onNavigateTab, onDownloadPdf, onDownloadPpt, onNewProject, onOpenHistory, onCloseHistory, onOpenHistoryIndex, onExitStudio, activeTab, projectIdea, addMessage]);

  // Clean Microphone Toggle (No Auto-Restart Chatter)
  const toggleListening = () => {
    if (isListening || autoListen) {
      setAutoListen(false);
      autoListenRef.current = false;
      if (recognitionRef.current) {
        try {
          recognitionRef.current.onstart = null;
          recognitionRef.current.onresult = null;
          recognitionRef.current.onerror = null;
          recognitionRef.current.onend = null;
          recognitionRef.current.abort();
        } catch {}
        recognitionRef.current = null;
      }
      setIsListening(false);
      setIsThinking(false);
      return;
    }

    setAutoListen(true);
    autoListenRef.current = true;
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
        try {
          recognitionRef.current.onstart = null;
          recognitionRef.current.onresult = null;
          recognitionRef.current.onerror = null;
          recognitionRef.current.onend = null;
          recognitionRef.current.abort();
        } catch {}
        recognitionRef.current = null;
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

      recognition.onerror = () => {
        setIsListening(false);
        setIsThinking(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
      try {
        recognition.start();
      } catch {}
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
        research: "Market research complete.",
        competitor: "Competitor intelligence identified.",
        product: "MVP feature specification ready.",
        roadmap: "4-Week execution roadmap generated.",
        pitch: "VC pitch deck compiled.",
        validation: "Validation assessment ready.",
        quality_control: "Quality control audit complete. Blueprint loaded, Boss."
      };
      if (stepNames[currentAgentStep]) {
        speak(stepNames[currentAgentStep]);
      }
    }
  }, [isExecuting, currentAgentStep, speak]);

  return (
    <>
      {/* Neo-Brutalist BLUE Assistant Widget (Fixed Bottom Right) */}
      <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3 font-sans selection:bg-black selection:text-white">
        
        {/* Chatbot Intelligence Feed Box (Scrollable Log + Text Input) */}
        {showCaption && (
          <div className="w-80 sm:w-96 p-4 bg-[#fefae0] border-4 border-black shadow-[6px_6px_0px_#000000] relative animate-in fade-in slide-in-from-bottom-3 duration-200">
            <div className="flex items-center justify-between border-b-2 border-black pb-2 mb-2">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 bg-[#3b82f6] border border-black animate-pulse" />
                <span className="text-[11px] font-black uppercase tracking-wider text-black">
                  BLUE // COMMANDER
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
                onClick={toggleListening}
                className={`px-2 py-0.5 border-2 border-black text-[10px] font-black uppercase tracking-wider flex items-center gap-1 transition-all ${
                  isListening ? "bg-[#ec4899] text-white animate-bounce" : "bg-black text-white"
                }`}
                title="Toggle Mic / Wake Word: BLUE"
              >
                <Radio className={`w-2.5 h-2.5 ${isListening ? "text-white animate-pulse" : "text-[#3b82f6]"}`} />
                {isListening ? "● LISTENING..." : 'WAKE-WORD: "BLUE"'}
              </button>
              {isThinking && (
                <span className="px-2 py-0.5 bg-[#f59e0b] text-black border-2 border-black text-[10px] font-black uppercase tracking-wider animate-pulse">
                  ⚡ PROCESSING COMMAND
                </span>
              )}
              {isSpeaking && (
                <span className="px-2 py-0.5 bg-[#10b981] text-black border-2 border-black text-[10px] font-black uppercase tracking-wider">
                  🔊 MALE VOICE TRANSMITTING
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
                        ? "bg-[#3b82f6]/20 text-black border-black text-right ml-6"
                        : "bg-black text-white border-black text-left mr-2"
                    }`}
                  >
                    <div className="flex items-center justify-between text-[9px] opacity-70 mb-1 font-sans">
                      <span>{m.sender === "user" ? "YOU" : "BLUE COMMANDER"}</span>
                      <span suppressHydrationWarning>{m.timestamp}</span>
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
                placeholder="Type 'search this idea [idea]'..."
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

        {/* Action Controls & Avatar Button Row */}
        <div className="flex items-center gap-2">
          
          {/* Quick Chat Feed Toggle Button */}
          <button
            onClick={() => {
              setShowCaption(true);
              setShowChatFeed(!showChatFeed);
            }}
            className="p-3 bg-white text-black border-3 border-black shadow-[4px_4px_0px_#000000] hover:bg-[#fefae0] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0px_#000000] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none transition-all font-black relative"
            title="Toggle BLUE Chat & Feed"
          >
            <MessageSquare className="w-5 h-5 stroke-[2.5]" />
            {messages.length > 0 && (
              <span className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-[#3b82f6] text-white border border-black rounded-full text-[9px] font-black flex items-center justify-center">
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
            title={isMuted ? "Unmute Male Voice" : "Mute Voice"}
          >
            {isMuted ? <VolumeX className="w-5 h-5 stroke-[2.5]" /> : <Volume2 className="w-5 h-5 stroke-[2.5]" />}
          </button>

          {/* Floating BLUE Avatar & Mic Button */}
          <button
            onClick={toggleListening}
            className={`relative group p-4 border-4 border-black shadow-[6px_6px_0px_#000000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[3px_3px_0px_#000000] active:translate-x-[6px] active:translate-y-[6px] active:shadow-none transition-all flex items-center justify-center ${
              isListening
                ? "bg-[#ec4899] text-white animate-pulse"
                : isSpeaking
                ? "bg-[#3b82f6] text-white"
                : isThinking
                ? "bg-[#f59e0b] text-black"
                : "bg-black text-white hover:bg-zinc-900"
            }`}
            title={isListening ? "Listening... Click to stop" : "Click to speak to BLUE"}
          >
            <div className="flex items-center gap-1.5 h-6 px-1">
              <span className={`w-1.5 bg-current border border-black transition-all duration-150 ${isSpeaking || isListening ? "h-6 animate-pulse" : "h-3"}`} />
              <span className={`w-1.5 bg-current border border-black transition-all duration-150 ${isSpeaking || isListening ? "h-4 animate-bounce" : "h-5"}`} />
              
              <div className="mx-1">
                <Mic className={`w-6 h-6 stroke-[3] ${isListening ? "scale-110 text-white" : ""}`} />
              </div>

              <span className={`w-1.5 bg-current border border-black transition-all duration-150 ${isSpeaking || isListening ? "h-5 animate-bounce" : "h-4"}`} />
              <span className={`w-1.5 bg-current border border-black transition-all duration-150 ${isSpeaking || isListening ? "h-6 animate-pulse" : "h-3"}`} />
            </div>

            <span className="absolute -top-1 -right-1 w-4 h-4 bg-[#3b82f6] border-2 border-black flex items-center justify-center text-[8px] font-black text-white">
              ★
            </span>
          </button>
        </div>
      </div>

      {/* Help Modal */}
      {showHelp && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white border-4 border-black shadow-[10px_10px_0px_#000000] w-full max-w-xl p-6 sm:p-8 relative animate-in zoom-in-95 duration-150 max-h-[90vh] overflow-y-auto font-sans">
            <div className="flex items-center justify-between border-b-4 border-black pb-4 mb-6">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-[#3b82f6] border-3 border-black shadow-[3px_3px_0px_#000000] flex items-center justify-center font-black text-white">
                  <Command className="w-6 h-6 stroke-[3]" />
                </div>
                <div>
                  <h3 className="text-lg font-black uppercase text-black">
                    BLUE // COMMAND MANIFEST
                  </h3>
                  <p className="text-xs font-bold text-gray-700">
                    Voice & text command reference for BLUE Commander
                  </p>
                </div>
              </div>
              <button 
                onClick={() => setShowHelp(false)}
                className="p-1 hover:bg-black hover:text-white border-2 border-black text-black transition-colors"
              >
                <X className="w-5 h-5 stroke-[2.5]" />
              </button>
            </div>

            <div className="space-y-4 text-xs font-bold">
              <div className="p-3 bg-[#fefae0] border-2 border-black">
                <h4 className="text-sm font-black uppercase text-black mb-1">⚡ 1. SEARCH THIS IDEA</h4>
                <p className="text-gray-800 font-mono">"search this idea [your idea]" or "search [idea]"</p>
                <p className="text-[11px] text-gray-600 font-normal mt-0.5">Triggers 8-agent swarm analysis for your concept.</p>
              </div>

              <div className="p-3 bg-[#fefae0] border-2 border-black">
                <h4 className="text-sm font-black uppercase text-black mb-1">📂 2. NAVIGATE TO HISTORY BOX</h4>
                <p className="text-gray-800 font-mono">"navigate to history box" or "open history"</p>
                <p className="text-[11px] text-gray-600 font-normal mt-0.5">Opens project history drawer.</p>
              </div>

              <div className="p-3 bg-[#fefae0] border-2 border-black">
                <h4 className="text-sm font-black uppercase text-black mb-1">🎯 3. OPEN SPECIFIC RESULT FROM HISTORY</h4>
                <p className="text-gray-800 font-mono">"open number 1 result from history box" or "open 2nd result"</p>
                <p className="text-[11px] text-gray-600 font-normal mt-0.5">Opens the exact saved blueprint by history index number.</p>
              </div>

              <div className="p-3 bg-[#fefae0] border-2 border-black">
                <h4 className="text-sm font-black uppercase text-black mb-1">🚪 4. CLOSE STUDIO</h4>
                <p className="text-gray-800 font-mono">"close studio" or "exit studio"</p>
                <p className="text-[11px] text-gray-600 font-normal mt-0.5">Returns to home landing screen.</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

// Export BlueAssistant alias as well
export const BlueAssistant = IrrisAssistant;
