import { redirect } from "next/navigation";
import { API_BASE } from "@/config/api";
import { AUTH_FORM_PATHS } from "@/constants/auth";
import { throwApiError } from "@/services/api-error";
import { refreshSession } from "@/services/token";

function apiFetch(path: string, init?: RequestInit): Promise<Response> {
  return fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
    credentials: "include",
    mode: "cors",
  });
}

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res = await apiFetch(path, init);

  if (res.status === 401 && !AUTH_FORM_PATHS.has(path)) {
    const refreshed = await refreshSession();
    if (!refreshed.ok) {
      redirect("/login");
    }
    res = await apiFetch(path, init);
  }

  if (!res.ok) {
    await throwApiError(res);
  }

  if (res.status === 204) {
    return undefined as T;
  }

  const text = await res.text();
  if (!text || text === "null") {
    return null as T;
  }

  return JSON.parse(text) as T;
}
