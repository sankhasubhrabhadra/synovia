export function getApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    const saved = localStorage.getItem("SYNOVIA_API_URL");
    if (saved && saved.trim()) {
      return saved.trim().replace(/\/$/, "");
    }
  }
  return (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");
}

export function setApiBaseUrl(url: string): void {
  if (typeof window !== "undefined") {
    if (url && url.trim()) {
      localStorage.setItem("SYNOVIA_API_URL", url.trim().replace(/\/$/, ""));
    } else {
      localStorage.removeItem("SYNOVIA_API_URL");
    }
  }
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

const getHeaders = () => ({
  "Content-Type": "application/json",
  "bypass-tunnel-reminder": "true",
  "ngrok-skip-browser-warning": "true",
});

export async function createProject(idea: string, targetMarket?: string, userGoal?: string): Promise<Project> {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/api/projects`, {
    method: "POST",
    headers: getHeaders(),
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
    headers: getHeaders(),
  });
  if (!response.ok) {
    throw new Error(`Failed to list projects: ${response.statusText}`);
  }
  return response.json();
}

export async function getProject(id: string): Promise<Project> {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/api/projects/${id}`, {
    headers: getHeaders(),
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
    headers: getHeaders(),
  });
  if (!response.ok) {
    throw new Error(`Failed to delete project ${id}`);
  }
}

export async function clearAllProjects(): Promise<void> {
  const baseUrl = getApiBaseUrl();
  const response = await fetch(`${baseUrl}/api/projects`, {
    method: "DELETE",
    headers: getHeaders(),
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
