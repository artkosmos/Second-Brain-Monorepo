import { decodeJwt } from "jose";

export function getJwtExpiration(token: string): number | undefined {
  return decodeJwt(token).exp;
}
