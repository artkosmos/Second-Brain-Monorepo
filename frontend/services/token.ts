import { API_BASE } from "@/config/api";
import { AUTH_REFRESH_PATH } from "@/constants/auth";

export function refreshSession(cookie?: string): Promise<Response> {
  return fetch(`${API_BASE}${AUTH_REFRESH_PATH}`, {
    method: "POST",
    credentials: "include",
    mode: "cors",
    headers: cookie ? { cookie } : undefined,
  });
}
