export const ACCESS_TOKEN_COOKIE = "access_token";

export const AUTH_LOGIN_PATH = "/auth/login";
export const AUTH_REGISTER_PATH = "/auth/register";
export const AUTH_REFRESH_PATH = "/auth/refresh";
export const AUTH_LOGOUT_PATH = "/auth/logout";

export const AUTH_FORM_PATHS = new Set([
  AUTH_LOGIN_PATH,
  AUTH_REGISTER_PATH,
  AUTH_REFRESH_PATH,
  AUTH_LOGOUT_PATH,
]);
