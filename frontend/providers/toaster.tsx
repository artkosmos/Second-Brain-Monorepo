"use client";

import { Toaster as SonnerToaster } from "sonner";

export function Toaster() {
  return (
    <SonnerToaster
      position="bottom-right"
      closeButton
      toastOptions={{
        duration: 6000,
        classNames: {
          error: "!border-danger-line !bg-danger-bg !text-danger",
        },
      }}
    />
  );
}
