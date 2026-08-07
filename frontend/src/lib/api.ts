const ACTIVE_TUNNEL_URL = "https://translations-laptop-operations-lift.trycloudflare.com";
const LOCALHOST_URL = "http://localhost:8000";

export function getApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    const host = window.location.hostname;
    if (host === "localhost" || host === "127.0.0.1") {
      return LOCALHOST_URL;
    }
    // On production (e.g. Vercel), use relative path "" so Next.js rewrites proxy server-to-server to Cloudflare Tunnel
    return "";
  }
  return ACTIVE_TUNNEL_URL;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
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

const TOKEN_KEY = "synovia_auth_token";
const USER_KEY = "synovia_user_profile";

export function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setAuthSession(token: string, user: User): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuthSession(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export function getStoredUser(): User | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

/**
 * Resilient fetch wrapper that passes responses directly and handles network errors.
 */
async function fetchResilient(path: string, options: RequestInit = {}): Promise<Response> {
  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}${path}`;

  const isPostOrPut = options.method && ["POST", "PUT", "PATCH"].includes(options.method.toUpperCase());
  const headers: Record<string, string> = {
    ...(isPostOrPut ? { "Content-Type": "application/json" } : {}),
    "bypass-tunnel-reminder": "true",
    "ngrok-skip-browser-warning": "true",
    ...(options.headers as Record<string, string> || {}),
  };

  let lastError: any = null;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const response = await fetch(url, { ...options, mode: "cors", headers });
      return response; // Return response directly regardless of HTTP status code
    } catch (err) {
      lastError = err;
    }
    if (attempt < 3) {
      await new Promise((res) => setTimeout(res, attempt * 500));
    }
  }

  console.error("All API connection attempts failed:", lastError);
  throw new Error("Unable to connect to Synovia Backend. Please verify the backend server is active.");
}

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const response = await fetchResilient("/api/health");
    return response.ok;
  } catch {
    return false;
  }
}

export async function signupUser(email: string, password: string, fullName: string): Promise<AuthResponse> {
  return {
    access_token: "guest",
    token_type: "bearer",
    user: { id: "guest", email, full_name: fullName, created_at: new Date().toISOString() }
  };
}

export async function loginUser(email: string, password: string): Promise<AuthResponse> {
  return {
    access_token: "guest",
    token_type: "bearer",
    user: { id: "guest", email, full_name: "Guest", created_at: new Date().toISOString() }
  };
}

export async function getMe(): Promise<User> {
  return { id: "guest", email: "guest@synovia.ai", full_name: "Guest User", created_at: new Date().toISOString() };
}

/* Project API Functions */
export async function createProject(idea: string, targetMarket?: string): Promise<Project> {
  const response = await fetchResilient(`/api/projects`, {
    method: "POST",
    body: JSON.stringify({ idea, target_market: targetMarket }),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to create blueprint (${response.status} ${response.statusText})`);
  }
  return response.json();
}

export async function listProjects(limit: number = 200): Promise<Project[]> {
  const response = await fetchResilient(`/api/projects?limit=${limit}`);
  if (!response.ok) throw new Error(`Failed to list projects`);
  return response.json();
}

export async function getProject(id: string): Promise<Project> {
  const response = await fetchResilient(`/api/projects/${id}`);
  if (!response.ok) throw new Error(`Failed to fetch project ${id}`);
  return response.json();
}

export async function deleteProject(id: string): Promise<void> {
  const response = await fetchResilient(`/api/projects/${id}`, { method: "DELETE" });
  if (!response.ok) throw new Error(`Failed to delete project ${id}`);
}

export async function clearAllProjects(): Promise<void> {
  const response = await fetchResilient(`/api/projects`, { method: "DELETE" });
  if (!response.ok) throw new Error(`Failed to clear all projects`);
}

export function getProjectStreamUrl(id: string): string {
  const baseUrl = getApiBaseUrl();
  return `${baseUrl}/api/projects/${id}/stream`;
}

export async function downloadProjectPdfFile(id: string, ideaName: string = "Blueprint"): Promise<void> {
  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}/api/projects/${id}/pdf`;
  window.open(url, "_blank");
}

export async function downloadProjectPptFile(id: string, ideaName: string = "Pitch_Deck"): Promise<void> {
  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}/api/projects/${id}/ppt`;
  window.open(url, "_blank");
}
