import { capitalize } from "@/utils/string";

type ValidationErrorBody = {
  field?: string;
  message?: string;
};

type ErrorBody = {
  message?: string;
  detail?: string;
};

export async function throwApiError(response: Response): Promise<never> {
  const body: ValidationErrorBody & ErrorBody = await response.json().catch(() => ({}));

  if (response.status === 422) {
    throw new Error(capitalize(`${body.field}: ${body.message}`));
  }

  throw new Error(body.message ?? body.detail ?? "Unknown error");
}
