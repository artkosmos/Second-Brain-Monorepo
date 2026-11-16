import {
  AUTH_LOGIN_PATH,
  AUTH_LOGOUT_PATH,
  AUTH_REGISTER_PATH,
} from "@/constants/auth";
import { request } from "@/services/api";

export const login = (email: string, password: string) =>
  request<null>(AUTH_LOGIN_PATH, {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

export const register = (email: string, password: string) =>
  request<null>(AUTH_REGISTER_PATH, {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

export const logout = () =>
  request<null>(AUTH_LOGOUT_PATH, {
    method: "POST",
  });
