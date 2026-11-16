import { AuthForm } from "@/components/auth-form";

export default function RegisterPage() {
  return (
    <AuthForm
      mode="register"
      title="Create an account"
      submitLabel="Create account"
      alternateHref="/login"
    />
  );
}
