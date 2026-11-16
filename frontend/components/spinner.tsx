export function Spinner({ label = "Loading", size = "size-4" }: { label?: string, size?: string }) {
  return (
    <span role="status" className="inline-flex items-center gap-2 text-sm text-muted">
      <span className={`${size} animate-spin rounded-full border-2 border-line-strong border-t-moss`} />
      <span className="sr-only">{label}</span>
    </span>
  );
}
