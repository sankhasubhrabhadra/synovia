const CLOUDFLARE_TUNNEL_URL = process.env.NEXT_PUBLIC_API_URL || "https://owned-brighton-guidelines-qualify.trycloudflare.com";
const LOCALHOST_URL = "http://localhost:8000";

export function getApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    const host = window.location.hostname;
    if (host !== "localhost" && host !== "127.0.0.1") {
      // Return relative empty string so fetches try Vercel Proxy Rewrite first
      return "";
    }
  }
  return LOCALHOST_URL;
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

const defaultHeaders: Record<string, string> = {
  "Content-Type": "application/json",
  "bypass-tunnel-reminder": "true",
  "ngrok-skip-browser-warning": "true",
};

/**
 * Ultra-resilient fetch wrapper with automatic fallback between Vercel Serverless Proxy and Direct Cloudflare Tunnel
 */
async function fetchResilient(path: string, options: RequestInit = {}): Promise<Response> {
  const primaryBaseUrl = getApiBaseUrl();
  const directTunnelUrl = CLOUDFLARE_TUNNEL_URL;

  const token = getAuthToken();
  const headers: Record<string, string> = { 
    ...defaultHeaders, 
    ...(options.headers as Record<string, string> || {}) 
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Target 1: Try Primary Base URL (Vercel Same-Origin Proxy)
  try {
    const url = `${primaryBaseUrl}${path}`;
    const response = await fetch(url, { ...options, mode: "cors", headers });
    // If response is valid (2xx, 4xx auth errors), return it
    if (response.ok || response.status < 500) {
      return response;
    }
  } catch (err) {
    console.warn(`Primary proxy endpoint (${primaryBaseUrl}${path}) failed. Attempting direct tunnel fallback...`);
  }

  // Target 2: Fallback to Direct Cloudflare Tunnel URL
  try {
    const directUrl = `${directTunnelUrl}${path}`;
    const response = await fetch(directUrl, { ...options, mode: "cors", headers });
    return response;
  } catch (fallbackErr) {
    console.error("All backend connection attempts failed:", fallbackErr);
    throw new Error(
      "Unable to connect to Synovia Backend. Please verify the backend server and tunnel are active."
    );
  }
}

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const response = await fetchResilient("/api/health");
    return response.ok;
  } catch {
    return false;
  }
}

/* Authentication API Functions */
export async function signupUser(email: string, password: string, fullName: string): Promise<AuthResponse> {
  const response = await fetchResilient(`/api/auth/signup`, {
    method: "POST",
    body: JSON.stringify({ email, password, full_name: fullName }),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Account creation failed. Email address may already be registered.");
  }
  const data: AuthResponse = await response.json();
  setAuthSession(data.access_token, data.user);
  return data;
}

export async function loginUser(email: string, password: string): Promise<AuthResponse> {
  const response = await fetchResilient(`/api/auth/login`, {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Invalid email address or password. Please try again.");
  }
  const data: AuthResponse = await response.json();
  setAuthSession(data.access_token, data.user);
  return data;
}

export async function getMe(): Promise<User> {
  const response = await fetchResilient(`/api/auth/me`);
  if (!response.ok) {
    clearAuthSession();
    throw new Error("Session expired or invalid");
  }
  const data: User = await response.json();
  return data;
}

/* Project API Functions (Using clean routes without trailing slash to prevent Next.js 308 Redirects) */
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
  if (!response.ok) {
    throw new Error(`Failed to list projects`);
  }
  return response.json();
}

export async function getProject(id: string): Promise<Project> {
  const response = await fetchResilient(`/api/projects/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch project ${id}`);
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
  const baseUrl = CLOUDFLARE_TUNNEL_URL;
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
