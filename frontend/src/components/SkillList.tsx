import { Badge } from "./ui/Badge";

interface SkillListProps {
  title: string;
  skills: string[];
  variant?: "matched" | "missing" | "neutral";
  emptyText?: string;
}

function SkillList({
  title,
  skills,
  variant = "neutral",
  emptyText = "None",
}: SkillListProps) {
  return (
    <div className="sl-wrap">
      <div className="sl-header">
        <span className="sl-title">{title}</span>
        <span className="sl-count">{skills.length}</span>
      </div>

      {skills.length > 0 ? (
        <div className="sl-list">
          {skills.map((skill) => (
            <Badge key={skill} variant={variant}>
              {skill}
            </Badge>
          ))}
        </div>
      ) : (
        <p className="sl-empty">{emptyText}</p>
      )}

      <style>{`
        .sl-wrap {
          display: flex;
          flex-direction: column;
          gap: 0.625rem;
        }
        .sl-header {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        .sl-title {
          font-size: 0.875rem;
          font-weight: 600;
          color: var(--color-text);
        }
        .sl-count {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          min-width: 20px;
          height: 20px;
          padding: 0 5px;
          background: var(--color-info-bg);
          border: 1px solid var(--color-border);
          border-radius: var(--radius-full);
          font-size: 0.75rem;
          font-weight: 600;
          color: var(--color-text-muted);
        }
        .sl-list {
          display: flex;
          flex-wrap: wrap;
          gap: 0.4rem;
        }
        .sl-empty {
          font-size: 0.875rem;
          color: var(--color-text-subtle);
          font-style: italic;
          margin: 0;
        }
      `}</style>
    </div>
  );
}

export default SkillList;