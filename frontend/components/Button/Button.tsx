import type { ReactNode } from "react";

type ButtonProps = {
  type?: "button" | "submit";
  className?: string;
  onClick?: () => void;
  children: ReactNode;
};

const BUTTON_CLASS =
  "h-9 rounded-lg border border-moss bg-moss text-sm text-sheet hover:bg-moss-hover";

export function Button({ type = "button", className, onClick, children }: ButtonProps) {
  const buttonClassName = [BUTTON_CLASS, className].filter(Boolean).join(" ");

  return (
    <button type={type} onClick={onClick} className={buttonClassName}>
      {children}
    </button>
  );
}
