import * as React from "react";
import { cn } from "./utils";

export type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";

export const buttonVariants: Record<ButtonVariant, string> = {
  primary: "ui-button ui-button-primary",
  secondary: "ui-button ui-button-secondary",
  ghost: "ui-button ui-button-ghost",
  danger: "ui-button ui-button-danger",
};

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  loading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", loading = false, disabled, children, ...props }, ref) => (
    <button ref={ref} className={cn(buttonVariants[variant], className)} disabled={disabled || loading} {...props}>
      {loading ? <span aria-hidden="true" className="ui-spinner" /> : null}
      {children}
    </button>
  ),
);
Button.displayName = "Button";
