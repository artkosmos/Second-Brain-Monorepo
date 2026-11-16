"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type ChangeEvent, type SubmitEvent } from "react";
import { Button } from "@/components/Button/Button";
import { Input } from "@/components/Input/Input";
import { login, register } from "@/services/auth";

type AuthMode = "login" | "register";

type AuthFormProps = {
  mode: AuthMode;
  title: string;
  submitLabel: string;
  alternateHref: string;
};

const ALTERNATE_LABEL: Record<AuthMode, string> = {
  login: "Create an account",
  register: "Sign in",
};

export function AuthForm({ mode, title, submitLabel, alternateHref }: AuthFormProps) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const authenticate = async () => {
    setError(null);
    try {
      if (mode === "login") {
        await login(email, password);
      } else {
        await register(email, password);
      }
      router.push("/");
    } catch (error: unknown) {
      setError(error instanceof Error ? error.message : "Unknown error");
    }
  };

  const handleSubmit = (event: SubmitEvent<HTMLFormElement>) => {
    event.preventDefault();
    void authenticate();
  };

  const handleEmailChange = (event: ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  };

  return (
    <div className="flex h-full items-center justify-center bg-paper px-6 text-ink">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm rounded-xl border border-line bg-sheet px-8 py-10"
      >
        <h1 className="font-serif text-3xl tracking-tight">{title}</h1>
        {error ? (
          <p className="mt-6 rounded-xl border border-danger-line bg-danger-bg px-4 py-2 text-sm text-danger">
            {error}
          </p>
        ) : null}
        <Input
          className="mt-6"
          label="Email"
          type="email"
          name="email"
          autoComplete="email"
          value={email}
          onChange={handleEmailChange}
        />
        <Input
          className="mt-4"
          label="Password"
          type="password"
          name="password"
          autoComplete={mode === "login" ? "current-password" : "new-password"}
          value={password}
          onChange={handlePasswordChange}
        />
        <Button type="submit" className="mt-6 w-full">
          {submitLabel}
        </Button>
        <p className="mt-4 text-center text-sm">
          <Link href={alternateHref} className="text-muted hover:text-ink">
            {ALTERNATE_LABEL[mode]}
          </Link>
        </p>
      </form>
    </div>
  );
}
