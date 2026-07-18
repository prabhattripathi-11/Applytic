interface BadgeProps {
  children: string;
  variant?: "matched" | "missing" | "neutral" | "info";
  size?: "sm" | "md";
}

export function Badge({ children, variant = "neutral", size = "md" }: BadgeProps) {
  return (
    <span className={`badge badge-${variant} badge-${size}`}>
      {variant === "matched" && (
        <svg width="9" height="9" viewBox="0 0 9 9" fill="none" aria-hidden="true">
          <circle cx="4.5" cy="4.5" r="4.5" fill="currentColor" opacity="0.3" />
          <path d="M2.5 4.5L3.9 5.9L6.5 3.3" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      )}
      {variant === "missing" && (
        <svg width="9" height="9" viewBox="0 0 9 9" fill="none" aria-hidden="true">
          <circle cx="4.5" cy="4.5" r="4.5" fill="currentColor" opacity="0.3" />
          <path d="M3 3L6 6M6 3L3 6" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" />
        </svg>
      )}
      {children}

      <style>{`
        .badge {
          display: inline-flex;
          align-items: center;
          gap: 0.3rem;
          font-family: var(--font-sans);
          font-weight: 500;
          border-radius: var(--radius-full);
          border: 1px solid transparent;
          white-space: nowrap;
        }

        .badge-sm { font-size: 0.75rem;   padding: 0.2rem  0.5rem;  }
        .badge-md { font-size: 0.8125rem; padding: 0.3rem  0.7rem;  }

        .badge-matched {
          background: var(--color-success-bg);
          color: var(--color-success);
          border-color: var(--color-success-border);
        }
        .badge-missing {
          background: var(--color-error-bg);
          color: var(--color-error);
          border-color: var(--color-error-border);
        }
        .badge-neutral {
          background: var(--color-info-bg);
          color: var(--color-text-muted);
          border-color: var(--color-border);
        }
        .badge-info {
          background: var(--color-primary);
          color: var(--color-primary-fg);
        }
      `}</style>
    </span>
  );
}
