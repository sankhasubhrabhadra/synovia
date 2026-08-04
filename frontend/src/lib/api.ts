// Active Cloudflare Tunnel Backend URL
const CLOUDFLARE_TUNNEL_URL = process.env.NEXT_PUBLIC_API_URL || "https://franklin-spies-senior-trace.trycloudflare.com";
const LOCALHOST_URL = "http://localhost:8000";

export function getApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    const host = window.location.hostname;
    if (host !== "localhost" && host !== "127.0.0.1") {
      return CLOUDFLARE_TUNNEL_URL;
    }
  }
  return LOCALHOST_URL;
}

export interface Project {
  id: string;
  idea: string;
  status: "pending" | "running" | "completed" | "failed";
  current_step: string;
  created_at: string;
  updated_at: string;
  blueprint?: any;
}

const defaultHeaders: Record<string, string> = {
  "Content-Type": "application/json",
  "bypass-tunnel-reminder": "true",
  "ngrok-skip-browser-warning": "true",
};

/**
 * Resilient fetch wrapper with automatic fallback between Cloudflare Tunnel and Localhost
 */
async function fetchResilient(path: string, options: RequestInit = {}): Promise<Response> {
  const primaryBaseUrl = getApiBaseUrl();
  const secondaryBaseUrl = primaryBaseUrl === CLOUDFLARE_TUNNEL_URL ? LOCALHOST_URL : CLOUDFLARE_TUNNEL_URL;

  const headers = { ...defaultHeaders, ...(options.headers as Record<string, string> || {}) };

  try {
    const response = await fetch(`${primaryBaseUrl}${path}`, { ...options, headers });
    return response;
  } catch (err) {
    console.warn(`Primary backend (${primaryBaseUrl}) unreachable, trying secondary backend (${secondaryBaseUrl})...`);
    try {
      const fallbackResponse = await fetch(`${secondaryBaseUrl}${path}`, { ...options, headers });
      return fallbackResponse;
    } catch (fallbackErr) {
      throw new Error(`Failed to connect to backend server. Please verify your backend server is running.`);
    }
  }
}

export async function createProject(idea: string, targetMarket?: string, userGoal?: string): Promise<Project> {
  const response = await fetchResilient(`/api/projects`, {
    method: "POST",
    body: JSON.stringify({
      idea,
      target_market: targetMarket,
      user_goal: userGoal,
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to create project: ${response.statusText}`);
  }

  return response.json();
}

export async function listProjects(limit: number = 200): Promise<Project[]> {
  const response = await fetchResilient(`/api/projects?limit=${limit}`);
  if (!response.ok) {
    throw new Error(`Failed to list projects: ${response.statusText}`);
  }
  return response.json();
}

export async function getProject(id: string): Promise<Project> {
  const response = await fetchResilient(`/api/projects/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch project ${id}: ${response.statusText}`);
  }
  return response.json();
}

export async function deleteProject(id: string): Promise<void> {
  const response = await fetchResilient(`/api/projects/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error(`Failed to delete project ${id}`);
  }
}

export async function clearAllProjects(): Promise<void> {
  const response = await fetchResilient(`/api/projects`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error(`Failed to clear all projects`);
  }
}

export function getProjectStreamUrl(id: string): string {
  const baseUrl = getApiBaseUrl();
  return `${baseUrl}/api/projects/${id}/stream`;
}

export async function downloadProjectPdfFile(id: string, ideaName: string = "Blueprint"): Promise<void> {
  const response = await fetchResilient(`/api/projects/${id}/pdf`);
  if (!response.ok) {
    throw new Error(`Failed to download PDF: ${response.statusText}`);
  }
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Synovia_Blueprint_${ideaName.slice(0, 15).replace(/\s+/g, "_")}.pdf`;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

export async function downloadProjectPptFile(id: string, ideaName: string = "Pitch_Deck"): Promise<void> {
  const response = await fetchResilient(`/api/projects/${id}/ppt`);
  if (!response.ok) {
    throw new Error(`Failed to download PPT: ${response.statusText}`);
  }
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Synovia_Pitch_Deck_${ideaName.slice(0, 15).replace(/\s+/g, "_")}.pptx`;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}


