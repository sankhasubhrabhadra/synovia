const CLOUDFLARE_BACKEND = "https://headquarters-statistics-band-implement.trycloudflare.com";

export function getApiBaseUrl(): string {
  // If NEXT_PUBLIC_API_URL is set and not localhost, use it
  const envUrl = process.env.NEXT_PUBLIC_API_URL;
  if (envUrl && !envUrl.includes("localhost") && !envUrl.includes("127.0.0.1")) {
    return envUrl.replace(/\/$/, "");
  }
  
  // If running in browser on Vercel or any non-localhost domain, default to Cloudflare backend
  if (typeof window !== "undefined" && window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1") {
    return CLOUDFLARE_BACKEND;
  }

  return (envUrl || "http://localhost:8000").replace(/\/$/, "");
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
