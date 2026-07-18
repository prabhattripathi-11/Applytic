import type { ResumeResponse } from "../types/resume";
import { ScoreRing } from "./ui/ScoreRing";
import SkillList from "./SkillList";

interface ResultCardProps {
  result: ResumeResponse;
}

function ResultCard({ result }: ResultCardProps) {
  const { parsed_resume, match_score, matched_skills, missing_skills, recommendations, errors } = result;

  return (
    <div className="rc-wrap">

      {/* ── Score hero ── */}
      <div className="rc-score-section">
        <ScoreRing score={match_score} size={128} />
        <div className="rc-score-meta">
          <h2 className="rc-candidate-name">{parsed_resume.full_name || "Candidate"}</h2>
          {parsed_resume.email && (
            <p className="rc-contact">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" aria-hidden="true">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                <polyline points="22,6 12,13 2,6" />
              </svg>
              {parsed_resume.email}
            </p>
          )}
          {parsed_resume.phone && (
            <p className="rc-contact">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" aria-hidden="true">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.91a16 16 0 0 0 6.08 6.08l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z" />
              </svg>
              {parsed_resume.phone}
            </p>
          )}
          <p className="rc-score-label">
            Overall match: <strong>{match_score}%</strong>
          </p>
        </div>
      </div>

      <div className="rc-divider" />

      {/* ── Summary ── */}
      {parsed_resume.summary && (
        <div className="rc-section">
          <h4 className="rc-section-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" aria-hidden="true">
              <circle cx="12" cy="8" r="4" />
              <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
            </svg>
            Professional summary
          </h4>
          <p className="rc-summary">{parsed_resume.summary}</p>
        </div>
      )}

      {/* ── Skills ── */}
      <div className="rc-section">
        <h4 className="rc-section-title">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" aria-hidden="true">
            <path d="M12 2L2 7l10 5 10-5-10-5z" />
            <path d="M2 17l10 5 10-5" />
            <path d="M2 12l10 5 10-5" />
          </svg>
          Skills breakdown
        </h4>
        <div className="rc-skills-grid">
          <SkillList
            title="Matched skills"
            skills={matched_skills}
            variant="matched"
            emptyText="No required skills were found in the resume."
          />
          <SkillList
            title="Missing skills"
            skills={missing_skills}
            variant="missing"
            emptyText="All required skills are present!"
          />
        </div>
      </div>

      {/* ── Recommendations ── */}
      {recommendations.length > 0 && (
        <div className="rc-section">
          <h4 className="rc-section-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" aria-hidden="true">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            Recommendations
          </h4>
          <ul className="rc-recommendations">
            {recommendations.map((rec, i) => (
              <li key={i} className="rc-rec-item">
                <span className="rc-rec-dot" aria-hidden="true" />
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ── Candidate Skills ── */}
      {parsed_resume.skills?.length > 0 && (
        <div className="rc-section">
          <h4 className="rc-section-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" aria-hidden="true">
              <polyline points="16 18 22 12 16 6" />
              <polyline points="8 6 2 12 8 18" />
            </svg>
            All resume skills
          </h4>
          <SkillList
            title=""
            skills={parsed_resume.skills}
            variant="neutral"
          />
        </div>
      )}

      {/* ── Errors ── */}
      {errors.length > 0 && (
        <div className="rc-section">
          <div className="rc-errors">
            <h4 className="rc-errors-title">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" aria-hidden="true">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                <line x1="12" y1="9" x2="12" y2="13" />
                <line x1="12" y1="17" x2="12.01" y2="17" />
              </svg>
              Warnings
            </h4>
            <ul className="rc-errors-list">
              {errors.map((err, i) => (
                <li key={i} className="rc-error-item">{err}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      <style>{`
        .rc-wrap {
          display: flex;
          flex-direction: column;
          gap: 0;
        }

        /* Score hero */
        .rc-score-section {
          display: flex;
          align-items: center;
          gap: 1.5rem;
          padding-bottom: 1.25rem;
        }
        .rc-score-meta {
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
          flex: 1;
          min-width: 0;
        }
        .rc-candidate-name {
          font-size: 1.375rem;
          font-weight: 700;
          color: var(--color-text);
          letter-spacing: -0.03em;
          margin: 0;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .rc-contact {
          display: flex;
          align-items: center;
          gap: 0.4rem;
          font-size: 0.875rem;
          color: var(--color-text-muted);
          margin: 0;
        }
        .rc-score-label {
          font-size: 0.875rem;
          color: var(--color-text-muted);
          margin: 0.25rem 0 0;
        }
        .rc-score-label strong {
          color: var(--color-text);
        }

        .rc-divider {
          height: 1px;
          background: var(--color-border);
          margin: 0.25rem 0 1.25rem;
        }

        /* Sections */
        .rc-section {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          padding-bottom: 1.25rem;
          margin-bottom: 1.25rem;
          border-bottom: 1px solid var(--color-border);
        }
        .rc-section:last-child {
          border-bottom: none;
          margin-bottom: 0;
          padding-bottom: 0;
        }
        .rc-section-title {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.875rem;
          font-weight: 600;
          color: var(--color-text);
          margin: 0;
        }

        /* Summary */
        .rc-summary {
          font-size: 0.9rem;
          line-height: 1.7;
          color: var(--color-text-muted);
          margin: 0;
        }

        /* Skills grid */
        .rc-skills-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1.25rem;
        }
        @media (max-width: 640px) {
          .rc-skills-grid { grid-template-columns: 1fr; }
          .rc-score-section { flex-direction: column; align-items: flex-start; gap: 1rem; }
        }

        /* Recommendations */
        .rc-recommendations {
          list-style: none;
          padding: 0;
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .rc-rec-item {
          display: flex;
          align-items: flex-start;
          gap: 0.625rem;
          font-size: 0.9rem;
          color: var(--color-text-muted);
          line-height: 1.55;
        }
        .rc-rec-dot {
          display: block;
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: var(--color-primary);
          margin-top: 0.45rem;
          flex-shrink: 0;
        }

        /* Errors */
        .rc-errors {
          background: var(--color-warning-bg);
          border: 1px solid var(--color-warning-border);
          border-radius: var(--radius-md);
          padding: 1rem;
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .rc-errors-title {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.875rem;
          font-weight: 600;
          color: var(--color-warning);
          margin: 0;
        }
        .rc-errors-list {
          padding-left: 1.25rem;
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }
        .rc-error-item {
          font-size: 0.875rem;
          color: var(--color-warning);
        }
      `}</style>
    </div>
  );
}

export default ResultCard;