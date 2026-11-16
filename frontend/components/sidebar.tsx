"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/Button/Button";
import { SIDEBAR_NAV } from "@/constants/sidebar";
import { reportRequestError } from "@/external/errors";
import { logout } from "@/services/auth";

export function Sidebar() {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await logout();
      router.replace("/login");
    } catch (error: unknown) {
      reportRequestError(error, "Failed to logout");
    }
  };

  return (
    <aside className="flex w-60 shrink-0 flex-col border-r border-line px-3 py-6">
      <p className="px-2 font-serif text-2xl tracking-tight">Second Brain</p>
      <nav className="mt-8 flex flex-col gap-1">
        {SIDEBAR_NAV.map((item) => (
          <span
            key={item.label}
            className={
              item.active
                ? "rounded-lg bg-recessed px-2 py-1.5 text-[13px] font-semibold text-moss"
                : "rounded-lg px-2 py-1.5 text-[13px] text-muted"
            }
          >
            {item.label}
          </span>
        ))}
      </nav>
      <div className="mt-auto flex flex-col gap-3 px-2">
        <Button type="button" className="w-full" onClick={() => void handleLogout()}>
          Log out
        </Button>
        <p className="text-[11px] font-medium tracking-wide text-faint uppercase">Local</p>
      </div>
    </aside>
  );
}
