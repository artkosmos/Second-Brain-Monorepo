import { unstable_rethrow } from "next/navigation";
import { toast } from "sonner";

export const reportRequestError = (error: unknown, fallback: string) => {
  // Re-throw Next.js control-flow errors so they are not shown as toasts.
  unstable_rethrow(error);
  toast.error(error instanceof Error ? error.message : fallback);
};
