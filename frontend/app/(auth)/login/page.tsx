import { AuthForm } from "@/components/auth-form";

export default function LoginPage() {
  return (
    <AuthForm mode="login" title="Sign in" submitLabel="Sign in" alternateHref="/register" />
  );
}
