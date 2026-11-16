import type { ChangeEvent } from "react";

type InputProps = {
  label: string;
  type: "email" | "password";
  name: string;
  autoComplete: string;
  value: string;
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
  className?: string;
};

const LABEL_CLASS = "block text-sm text-muted";

export function Input({ label, type, name, autoComplete, value, onChange, className }: InputProps) {
  const labelClassName = [LABEL_CLASS, className].filter(Boolean).join(" ");

  return (
    <label className={labelClassName}>
      {label}
      <input
        type={type}
        name={name}
        autoComplete={autoComplete}
        required
        value={value}
        onChange={onChange}
        className="mt-1.5 h-10 w-full rounded-xl border border-line bg-sheet px-3 text-sm text-ink outline-none focus:border-moss"
      />
    </label>
  );
}
