import { useState } from "react";
import ResumeUpload from "../components/ResumeUpload";
import JobDescription from "../components/JobDescription";
import ResultCard from "../components/ResultCard";
import { Card, CardHeader } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { uploadResume } from "../api/resume";
import type { ResumeResponse } from "../types/resume";

function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ResumeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleAnalyze() {
    if (!file) {
      setError("Please upload a resume PDF before analyzing.");
      return;
    }
    if (!jobDescription.trim()) {
      setError("Please enter a job description before analyzing.");
      return;
    }

    setError(null);
    setResult(null);

    try {
      setLoading(true);
      const response = await uploadResume(file, jobDescription);
      setResult(response);
      // Scroll to results
      setTimeout(() => {
        document.getElementById("results-card")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      setError("Analysis failed: " + msg);
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setFile(null);
    setJobDescription("");
    setResult(null);
    setError(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  const canAnalyze = !!file && jobDescription.trim().length > 0;

  return (
    <main className="home-page">
      <div className="container">

        {/* ── Page header ── */}
        <div className="home-header">
          <div>
            <h1 className="home-title">Resume Intelligence</h1>
            <p className="home-subtitle">
              Upload a resume and job description to get an AI-powered match analysis instantly.
            </p>
          </div>
          {result && (
            <Button variant="ghost" size="sm" onClick={handleReset}>
              New analysis
            </Button>
          )}
        </div>

        {/* ── Dashboard grid ── */}
        <div className="home-grid">

          {/* Card 1 — Resume Upload */}
          <Card padding="md">
            <CardHeader
              title="Resume"
              subtitle="Upload the candidate's resume in PDF format"
              icon={
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                </svg>
              }
            />
            <ResumeUpload file={file} setFile={setFile} />
          </Card>

          {/* Card 2 — Job Description */}
          <Card padding="md">
            <CardHeader
              title="Job Description"
              subtitle="Paste the full job posting to match against"
              icon={
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                  <line x1="3" y1="9" x2="21" y2="9" />
                  <line x1="9" y1="21" x2="9" y2="9" />
                </svg>
              }
            />
            <JobDescription value={jobDescription} onChange={setJobDescription} />
          </Card>

          {/* Card 3 — Analyze */}
          <Card padding="md">
            <CardHeader
              title="Analyze"
              subtitle="Run the AI-powered matching engine"
              icon={
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="11" cy="11" r="8" />
                  <line x1="21" y1="21" x2="16.65" y2="16.65" />
                </svg>
              }
            />

            <div className="home-analyze-body">
              {/* Checklist */}
              <div className="home-checklist">
                <div className={`home-check-item ${file ? "home-check--done" : ""}`}>
                  {file ? (
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <circle cx="8" cy="8" r="7" fill="var(--color-success)" />
                      <path d="M5 8l2.5 2.5L11 5.5" stroke="white" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  ) : (
                    <div className="home-check-circle" aria-hidden="true" />
                  )}
                  <span>Resume uploaded</span>
                </div>
                <div className={`home-check-item ${jobDescription.trim() ? "home-check--done" : ""}`}>
                  {jobDescription.trim() ? (
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <circle cx="8" cy="8" r="7" fill="var(--color-success)" />
                      <path d="M5 8l2.5 2.5L11 5.5" stroke="white" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  ) : (
                    <div className="home-check-circle" aria-hidden="true" />
                  )}
                  <span>Job description entered</span>
                </div>
              </div>

              {error && (
                <div className="home-error" role="alert">
                  <svg width="15" height="15" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                    <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.4" />
                    <path d="M8 5v3M8 10.5v.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
                  </svg>
                  {error}
                </div>
              )}

              <Button
                fullWidth
                size="lg"
                loading={loading}
                disabled={!canAnalyze}
                onClick={handleAnalyze}
              >
                {loading ? "Analyzing resume…" : "Analyze resume"}
              </Button>

              <p className="home-analyze-note">
                Powered by Google Gemini · Results in ~10 seconds
              </p>
            </div>
          </Card>

          {/* Card 4 — Results (only shown after analysis) */}
          {result && (
            <Card padding="md" id="results-card">
              <CardHeader
                title="Analysis Results"
                subtitle={`Match score: ${result.match_score}% · ${result.matched_skills.length} matched · ${result.missing_skills.length} missing`}
                icon={
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                  </svg>
                }
              />
              <ResultCard result={result} />
            </Card>
          )}

        </div>
      </div>

      <style>{`
        .home-page {
          flex: 1;
          padding: 2rem 0 4rem;
        }

        .home-header {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          gap: 1rem;
          margin-bottom: 2rem;
        }
        .home-title {
          font-size: 1.625rem;
          font-weight: 700;
          color: var(--color-text);
          letter-spacing: -0.03em;
          margin-bottom: 0.25rem;
        }
        .home-subtitle {
          font-size: 0.9375rem;
          color: var(--color-text-muted);
          margin: 0;
          max-width: 520px;
        }

        /* Grid */
        .home-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1.25rem;
        }
        @media (max-width: 768px) {
          .home-grid { grid-template-columns: 1fr; }
          .home-header { flex-direction: column; }
        }

        /* Analyze card body */
        .home-analyze-body {
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
        }

        /* Checklist */
        .home-checklist {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .home-check-item {
          display: flex;
          align-items: center;
          gap: 0.625rem;
          font-size: 0.875rem;
          color: var(--color-text-subtle);
          transition: color var(--transition-fast);
        }
        .home-check--done {
          color: var(--color-text-muted);
          font-weight: 500;
        }
        .home-check-circle {
          width: 16px;
          height: 16px;
          border-radius: 50%;
          border: 2px solid var(--color-border);
          flex-shrink: 0;
        }

        /* Error */
        .home-error {
          display: flex;
          align-items: flex-start;
          gap: 0.5rem;
          padding: 0.625rem 0.875rem;
          background: var(--color-error-bg);
          border: 1px solid var(--color-error-border);
          border-radius: var(--radius-md);
          font-size: 0.875rem;
          color: var(--color-error);
          line-height: 1.4;
        }

        .home-analyze-note {
          font-size: 0.8rem;
          color: var(--color-text-subtle);
          text-align: center;
          margin: 0;
        }
      `}</style>
    </main>
  );
}

export default Home;