// Production Cloudflare Tunnel Backend URL (hardcoded for reliability)
const PRODUCTION_BACKEND = "https://fields-races-list-ethical.trycloudflare.com";

export function getApiBaseUrl(): string {
  // Client-side: if running on Vercel (not localhost), always use the production backend
  if (typeof window !== "undefined") {
    const host = window.location.hostname;
    if (host !== "localhost" && host !== "127.0.0.1") {
      return PRODUCTION_BACKEND;
    }
  }
  return "http://localhost:8000";
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

export async function createProject(idea: string, targetMarket?: string, userGoal?: string): Promise<Project> {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/api/projects`, {
    method: "POST",
    headers: defaultHeaders,
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
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/api/projects?limit=${limit}`, {
    headers: defaultHeaders,
  });
  if (!response.ok) {
    throw new Error(`Failed to list projects: ${response.statusText}`);
  }
  return response.json();
}

export async function getProject(id: string): Promise<Project> {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/api/projects/${id}`, {
    headers: defaultHeaders,
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch project ${id}: ${response.statusText}`);
  }
  return response.json();
}

export async function deleteProject(id: string): Promise<void> {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/api/projects/${id}`, {
    method: "DELETE",
    headers: defaultHeaders,
  });
  if (!response.ok) {
    throw new Error(`Failed to delete project ${id}`);
  }
}

export async function clearAllProjects(): Promise<void> {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/api/projects`, {
    method: "DELETE",
    headers: defaultHeaders,
  });
  if (!response.ok) {
    throw new Error(`Failed to clear all projects`);
  }
}

export function getProjectStreamUrl(id: string): string {
  const baseUrl = getApiBaseUrl();
  return `${baseUrl}/api/projects/${id}/stream`;
}

export function getProjectPdfUrl(id: string): string {
  const baseUrl = getApiBaseUrl();
  return `${baseUrl}/api/projects/${id}/pdf`;
}
