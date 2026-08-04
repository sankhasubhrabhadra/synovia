const CLOUDFLARE_TUNNEL_URL = process.env.NEXT_PUBLIC_API_URL || "https://cst-beatles-blanket-chelsea.trycloudflare.com";
const LOCALHOST_URL = "http://localhost:8000";

export function getApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    const host = window.location.hostname;
    if (host !== "localhost" && host !== "127.0.0.1") {
      // Use Vercel Serverless Proxy Rewrite (/api) for 100% same-origin reliability on all devices
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
 * Ultra-resilient fetch wrapper with automatic retries and fallback
 */
async function fetchResilient(path: string, options: RequestInit = {}): Promise<Response> {
  const primaryBaseUrl = getApiBaseUrl();
  const secondaryBaseUrl = primaryBaseUrl === CLOUDFLARE_TUNNEL_URL ? LOCALHOST_URL : CLOUDFLARE_TUNNEL_URL;

  const token = getAuthToken();
  const headers: Record<string, string> = { 
    ...defaultHeaders, 
    ...(options.headers as Record<string, string> || {}) 
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Attempt up to 3 retries on primary backend URL to handle transient tunnel wake-up delays
  let lastError: any = null;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const response = await fetch(`${primaryBaseUrl}${path}`, { 
        ...options, 
        mode: "cors",
        headers 
      });
      return response;
    } catch (err) {
      lastError = err;
      console.warn(`Attempt ${attempt}/3 to primary backend (${primaryBaseUrl}${path}) failed. Retrying...`);
      if (attempt < 3) {
        await new Promise((res) => setTimeout(res, attempt * 600));
      }
    }
  }

  // Fallback attempt to secondary backend
  try {
    const fallbackResponse = await fetch(`${secondaryBaseUrl}${path}`, { 
      ...options, 
      mode: "cors",
      headers 
    });
    return fallbackResponse;
  } catch (fallbackErr) {
    console.error("All backend connection attempts failed:", lastError || fallbackErr);
    throw new Error(
      "Unable to connect to Synovia Backend. Please check your internet connection or verify the server is active."
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
    throw new Error(errorData.detail || "Account creation failed. An account with this email may already exist.");
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

/* Project API Functions */
export async function createProject(idea: string, targetMarket?: string): Promise<Project> {
  const response = await fetchResilient(`/api/projects`, {
    method: "POST",
    body: JSON.stringify({ idea, target_market: targetMarket }),
  });
  if (!response.ok) {
    throw new Error(`Failed to create project: ${response.statusText}`);
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
