import { getJwtExpiration } from "@/external/jwt";

export function isAccessTokenAlive(token: string): boolean {
  try {
    const exp = getJwtExpiration(token);
    return typeof exp === "number" && exp * 1000 > Date.now();
  } catch {
    return false;
  }
}
