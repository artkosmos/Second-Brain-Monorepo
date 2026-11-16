import { ACCESS_TOKEN_COOKIE } from "@/constants/auth";
import { refreshSession } from "@/services/token";
import { isAccessTokenAlive } from "@/utils/auth-token";
import { NextResponse, type NextRequest } from "next/server";

export async function proxy(request: NextRequest) {
  const loginUrl = new URL("/login", request.url);
  const access = request.cookies.get(ACCESS_TOKEN_COOKIE)?.value;

  if (access && isAccessTokenAlive(access)) {
    return NextResponse.next();
  }

  const refreshed = await refreshSession(request.headers.get("cookie") ?? undefined);

  if (!refreshed.ok) {
    return NextResponse.redirect(loginUrl);
  }

  const response = NextResponse.next();

  for (const cookie of refreshed.headers.getSetCookie()) {
    response.headers.append("set-cookie", cookie);
  }

  return response;
}

export const config = {
  // Every path except /login, /register, and static assets.
  matcher: [
    "/((?!login|register|_next/static|_next/image|favicon.ico|.*\\.(?:png|svg|ico)$).*)",
  ],
};
