import type { ButtonHTMLAttributes, ReactNode } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
  children: ReactNode;
  fullWidth?: boolean;
}

const sizeStyles: Record<string, string> = {
  sm: "btn-sm",
  md: "btn-md",
  lg: "btn-lg",
};

export function Button({
  variant = "primary",
  size = "md",
  loading = false,
  fullWidth = false,
  children,
  disabled,
  className = "",
  ...rest
}: ButtonProps) {
  const classes = [
    "btn",
    `btn-${variant}`,
    sizeStyles[size],
    fullWidth ? "btn-full" : "",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button className={classes} disabled={disabled || loading} {...rest}>
      {loading ? (
        <span className="btn-spinner-wrap">
          <span className="btn-spinner" />
          <span>{children}</span>
        </span>
      ) : (
        children
      )}

      <style>{`
        .btn {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          font-family: var(--font-sans);
          font-weight: 500;
          letter-spacing: -0.01em;
          border: 1px solid transparent;
          border-radius: var(--radius-md);
          cursor: pointer;
          transition: background var(--transition-fast), color var(--transition-fast),
            border-color var(--transition-fast), box-shadow var(--transition-fast),
            opacity var(--transition-fast), transform var(--transition-fast);
          white-space: nowrap;
          user-select: none;
          text-decoration: none;
          -webkit-tap-highlight-color: transparent;
        }
        .btn:active:not(:disabled) { transform: scale(0.97); }
        .btn:disabled {
          opacity: 0.45;
          cursor: not-allowed;
          transform: none;
        }

        /* Variants */
        .btn-primary {
          background: var(--color-primary);
          color: var(--color-primary-fg);
          border-color: var(--color-primary);
          box-shadow: var(--shadow-xs);
        }
        .btn-primary:hover:not(:disabled) {
          background: var(--color-primary-hover);
          border-color: var(--color-primary-hover);
          box-shadow: var(--shadow-sm);
        }

        .btn-ghost {
          background: transparent;
          color: var(--color-text);
          border-color: var(--color-border);
        }
        .btn-ghost:hover:not(:disabled) {
          background: var(--color-info-bg);
          border-color: var(--color-border-hover);
        }

        .btn-danger {
          background: var(--color-error-bg);
          color: var(--color-error);
          border-color: var(--color-error-border);
        }
        .btn-danger:hover:not(:disabled) {
          background: #fee2e2;
        }

        /* Sizes */
        .btn-sm  { font-size: 0.8125rem; padding: 0.375rem 0.75rem;  border-radius: var(--radius-sm); }
        .btn-md  { font-size: 0.9375rem; padding: 0.625rem 1.125rem; }
        .btn-lg  { font-size: 1rem;      padding: 0.8rem 1.5rem;     border-radius: var(--radius-lg); }

        .btn-full { width: 100%; }

        /* Spinner */
        .btn-spinner-wrap {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
        }
        .btn-spinner {
          display: inline-block;
          width: 14px;
          height: 14px;
          border: 2px solid currentColor;
          border-top-color: transparent;
          border-radius: 50%;
          animation: btn-spin 0.65s linear infinite;
          flex-shrink: 0;
        }
        @keyframes btn-spin { to { transform: rotate(360deg); } }
      `}</style>
    </button>
  );
}
