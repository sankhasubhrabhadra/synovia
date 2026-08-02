export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Project {
  id: string;
  idea: string;
  status: "pending" | "running" | "completed" | "failed";
  current_step: string;
  created_at: string;
  updated_at: string;
  blueprint?: any;
}

export async function createProject(idea: string, targetMarket?: string, userGoal?: string): Promise<Project> {
  const response = await fetch(`${API_BASE_URL}/api/projects`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
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
  const response = await fetch(`${API_BASE_URL}/api/projects?limit=${limit}`);
  if (!response.ok) {
    throw new Error(`Failed to list projects: ${response.statusText}`);
  }
  return response.json();
}

export async function getProject(id: string): Promise<Project> {
  const response = await fetch(`${API_BASE_URL}/api/projects/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch project ${id}: ${response.statusText}`);
  }
  return response.json();
}

export async function deleteProject(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/projects/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error(`Failed to delete project ${id}`);
  }
}

export async function clearAllProjects(): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/projects`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error(`Failed to clear all projects`);
  }
}

export function getProjectStreamUrl(id: string): string {
  return `${API_BASE_URL}/api/projects/${id}/stream`;
}

export function getProjectPdfUrl(id: string): string {
  return `${API_BASE_URL}/api/projects/${id}/pdf`;
}
