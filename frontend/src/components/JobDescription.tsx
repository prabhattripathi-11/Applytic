interface JobDescriptionProps {
  value: string;
  onChange: (value: string) => void;
}

const MAX_CHARS = 4000;

function JobDescription({ value, onChange }: JobDescriptionProps) {
  const charCount = value.length;
  const isNearLimit = charCount > MAX_CHARS * 0.85;

  return (
    <div className="jd-wrap">
      <div className="jd-label-row">
        <label htmlFor="job-description">Job description</label>
        <span
          className={`jd-count${isNearLimit ? " jd-count--warn" : ""}`}
          aria-live="polite"
        >
          {charCount.toLocaleString()} / {MAX_CHARS.toLocaleString()}
        </span>
      </div>

      <textarea
        id="job-description"
        rows={10}
        value={value}
        onChange={(e) => {
          if (e.target.value.length <= MAX_CHARS) {
            onChange(e.target.value);
          }
        }}
        placeholder="Paste the full job description here — including required skills, responsibilities, qualifications, and any technical requirements. The more detail you provide, the more accurate the analysis will be."
        aria-describedby="jd-hint"
        className="jd-textarea"
        spellCheck={false}
      />

      <p id="jd-hint" className="jd-hint">
        Include the complete posting for best results.
      </p>

      <style>{`
        .jd-wrap {
          display: flex;
          flex-direction: column;
          gap: 0.375rem;
          width: 100%;
        }
        .jd-label-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 0.5rem;
        }
        .jd-count {
          font-size: 0.8125rem;
          color: var(--color-text-subtle);
          transition: color var(--transition-fast);
        }
        .jd-count--warn {
          color: var(--color-warning);
        }
        .jd-textarea {
          font-size: 0.9rem;
          line-height: 1.65;
          resize: vertical;
          min-height: 200px;
        }
        .jd-hint {
          font-size: 0.8125rem;
          color: var(--color-text-subtle);
          margin: 0;
        }
      `}</style>
    </div>
  );
}

export default JobDescription;