import * as React from "react";
import { cn } from "./utils";

export const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => <input ref={ref} className={cn("ui-input", className)} {...props} />,
);
Input.displayName = "Input";

export function Field({ label, hint, error, children }: { label: string; hint?: string; error?: string; children: React.ReactNode }) {
  return (
    <label className="ui-field">
      <span className="ui-field-label">{label}</span>
      {children}
      {error ? <span className="ui-field-error" role="alert">{error}</span> : hint ? <span className="ui-field-hint">{hint}</span> : null}
    </label>
  );
}
