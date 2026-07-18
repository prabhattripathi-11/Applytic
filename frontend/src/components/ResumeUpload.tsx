import { useRef, useState } from "react";

interface ResumeUploadProps {
  file: File | null;
  setFile: (file: File | null) => void;
}

function ResumeUpload({ file, setFile }: ResumeUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  function handleFiles(files: FileList | null) {
    if (!files || files.length === 0) return;
    const picked = files[0];
    if (picked.type !== "application/pdf") {
      alert("Only PDF files are supported.");
      return;
    }
    setFile(picked);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragging(false);
    handleFiles(e.dataTransfer.files);
  }

  function handleDragOver(e: React.DragEvent) {
    e.preventDefault();
    setDragging(true);
  }

  function handleDragLeave() {
    setDragging(false);
  }

  function handleRemove() {
    setFile(null);
    if (inputRef.current) inputRef.current.value = "";
  }

  const sizeKB = file ? (file.size / 1024).toFixed(1) : null;

  return (
    <div className="ru-wrap">
      {!file ? (
        <div
          className={`ru-dropzone${dragging ? " ru-dropzone--active" : ""}`}
          onClick={() => inputRef.current?.click()}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          role="button"
          tabIndex={0}
          aria-label="Upload resume PDF"
          onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
        >
          <div className="ru-icon" aria-hidden="true">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
          </div>
          <p className="ru-primary">
            {dragging ? "Drop your resume here" : "Drop your resume here or"}
            {!dragging && <span className="ru-browse"> browse files</span>}
          </p>
          <p className="ru-hint">PDF only · Max 5 MB</p>
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,application/pdf"
            className="ru-hidden-input"
            onChange={(e) => handleFiles(e.target.files)}
            aria-hidden="true"
            tabIndex={-1}
          />
        </div>
      ) : (
        <div className="ru-preview">
          <div className="ru-file-icon" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" y1="13" x2="8" y2="13" />
              <line x1="16" y1="17" x2="8" y2="17" />
              <polyline points="10 9 9 9 8 9" />
            </svg>
          </div>
          <div className="ru-file-info">
            <p className="ru-file-name">{file.name}</p>
            <p className="ru-file-size">{sizeKB} KB · PDF</p>
          </div>
          <button
            type="button"
            className="ru-remove"
            onClick={handleRemove}
            aria-label="Remove file"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
              <path d="M4 4l8 8M12 4l-8 8" />
            </svg>
          </button>
        </div>
      )}

      <style>{`
        .ru-wrap { width: 100%; }

        .ru-dropzone {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          padding: 2.5rem 1.5rem;
          border: 2px dashed var(--color-border);
          border-radius: var(--radius-lg);
          background: var(--color-bg);
          cursor: pointer;
          transition: border-color var(--transition-base), background var(--transition-base);
          text-align: center;
        }
        .ru-dropzone:hover,
        .ru-dropzone:focus-visible {
          border-color: var(--color-primary);
          background: #f9f9f9;
          outline: none;
        }
        .ru-dropzone--active {
          border-color: var(--color-primary);
          background: #f4f4f5;
          box-shadow: 0 0 0 4px rgb(9 9 11 / 0.06);
        }
        .ru-icon {
          color: var(--color-text-subtle);
          margin-bottom: 0.25rem;
        }
        .ru-primary {
          font-size: 0.9375rem;
          font-weight: 500;
          color: var(--color-text);
          margin: 0;
        }
        .ru-browse {
          color: var(--color-primary);
          font-weight: 600;
          text-decoration: underline;
          text-underline-offset: 2px;
          margin-left: 0.25rem;
        }
        .ru-hint {
          font-size: 0.8125rem;
          color: var(--color-text-subtle);
          margin: 0;
        }
        .ru-hidden-input {
          position: absolute;
          width: 1px;
          height: 1px;
          opacity: 0;
          pointer-events: none;
        }

        /* Preview */
        .ru-preview {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 0.875rem 1rem;
          background: var(--color-success-bg);
          border: 1px solid var(--color-success-border);
          border-radius: var(--radius-lg);
        }
        .ru-file-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          background: var(--color-surface);
          border: 1px solid var(--color-border);
          border-radius: var(--radius-md);
          color: var(--color-success);
          flex-shrink: 0;
        }
        .ru-file-info {
          flex: 1;
          min-width: 0;
        }
        .ru-file-name {
          font-size: 0.9rem;
          font-weight: 600;
          color: var(--color-text);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          margin: 0;
        }
        .ru-file-size {
          font-size: 0.8rem;
          color: var(--color-text-muted);
          margin: 0.125rem 0 0;
        }
        .ru-remove {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 28px;
          height: 28px;
          border: none;
          border-radius: var(--radius-sm);
          background: transparent;
          color: var(--color-text-muted);
          cursor: pointer;
          transition: background var(--transition-fast), color var(--transition-fast);
          flex-shrink: 0;
        }
        .ru-remove:hover {
          background: var(--color-error-bg);
          color: var(--color-error);
        }
      `}</style>
    </div>
  );
}

export default ResumeUpload;