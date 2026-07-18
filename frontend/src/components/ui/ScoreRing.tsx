interface ScoreRingProps {
  score: number; // 0–100
  size?: number;
}

export function ScoreRing({ score, size = 120 }: ScoreRingProps) {
  const clamped = Math.max(0, Math.min(100, score));
  const radius = 44;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (clamped / 100) * circumference;

  const color =
    clamped >= 70 ? "var(--color-success)" :
    clamped >= 40 ? "var(--color-warning)" :
                    "var(--color-error)";

  const label =
    clamped >= 90 ? "Excellent" :
    clamped >= 70 ? "Good" :
    clamped >= 40 ? "Moderate" :
                    "Low";

  return (
    <div className="score-ring-wrap" style={{ width: size, height: size }}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 100 100"
        fill="none"
        aria-label={`Match score: ${clamped}%`}
        role="img"
      >
        {/* Track */}
        <circle
          cx="50"
          cy="50"
          r={radius}
          stroke="var(--color-border)"
          strokeWidth="8"
        />
        {/* Progress */}
        <circle
          cx="50"
          cy="50"
          r={radius}
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform="rotate(-90 50 50)"
          style={{ transition: "stroke-dashoffset 0.8s cubic-bezier(0.4,0,0.2,1), stroke 0.4s ease" }}
        />
      </svg>
      <div className="score-ring-label">
        <span className="score-ring-value" style={{ color }}>{clamped}%</span>
        <span className="score-ring-text">{label}</span>
      </div>

      <style>{`
        .score-ring-wrap {
          position: relative;
          flex-shrink: 0;
        }
        .score-ring-wrap svg {
          display: block;
        }
        .score-ring-label {
          position: absolute;
          inset: 0;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 1px;
          pointer-events: none;
        }
        .score-ring-value {
          font-size: 1.25rem;
          font-weight: 700;
          line-height: 1;
          letter-spacing: -0.03em;
        }
        .score-ring-text {
          font-size: 0.6875rem;
          font-weight: 500;
          color: var(--color-text-muted);
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
      `}</style>
    </div>
  );
}
