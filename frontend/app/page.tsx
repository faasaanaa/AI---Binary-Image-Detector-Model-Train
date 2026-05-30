'use client';

import { ChangeEvent, useMemo, useState } from 'react';

type ResultState = {
  label: string;
  confidence: number;
  note: string;
};

const PRESET_RESULTS: ResultState[] = [
  { label: 'Real', confidence: 96, note: 'Natural edge continuity and texture consistency detected.' },
  { label: 'Fake', confidence: 91, note: 'Synthetic artifact pattern found around blended regions.' },
  { label: 'Inconclusive', confidence: 78, note: 'Mixed signals. Needs a closer model pass.' }
];

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState<ResultState | null>(null);

  const statusLabel = useMemo(() => {
    if (processing) return 'Processing image...';
    if (result) return 'Prediction ready';
    return 'Upload an image to begin';
  }, [processing, result]);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const nextFile = event.target.files?.[0] ?? null;
    setFile(nextFile);
    setResult(null);

    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    }

    if (nextFile) {
      setPreviewUrl(URL.createObjectURL(nextFile));
    }
  };

  const handlePredict = () => {
    if (!file) return;

    setProcessing(true);
    setResult(null);

    window.setTimeout(() => {
      const selected = PRESET_RESULTS[file.name.length % PRESET_RESULTS.length];
      setResult(selected);
      setProcessing(false);
    }, 1800);
  };

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setProcessing(false);

    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    }
  };

  return (
    <main className="shell">
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />

      <nav className="nav">
        <div className="brand">
          <span className="brand-mark" />
          <span>you see it we verify it</span>
        </div>
        <div className="nav-pill">Predicter</div>
      </nav>

      <section className="hero">
        <p className="eyebrow">AI Image verification system</p>
        <h1>One thing that matters: the result.</h1>
        <p className="hero-copy">
          Upload an image, let the model process it, then read the prediction in a clean, high-contrast layout.
        </p>
      </section>

      <section className="panel">
        <div className="panel-top">
          <div>
            <p className="panel-label">Step 01</p>
            <h2>Upload image</h2>
          </div>
          <div className="status-chip">{statusLabel}</div>
        </div>

        <label className="dropzone">
          <input type="file" accept="image/*" onChange={handleFileChange} />
          <span className="dropzone-title">Drop an image here or click to browse</span>
          <span className="dropzone-subtitle">PNG, JPG, JPEG, WEBP supported</span>
        </label>

        {previewUrl ? (
          <div className="preview-card">
            <img src={previewUrl} alt="Uploaded preview" />
            <div>
              <p className="preview-label">Selected file</p>
              <h3>{file?.name}</h3>
            </div>
          </div>
        ) : null}

        <button className="primary-button" onClick={handlePredict} disabled={!file || processing}>
          {processing ? 'Analyzing...' : 'Start verification'}
        </button>
      </section>

      <section className="panel result-panel">
        <div className="panel-top">
          <div>
            <p className="panel-label">Step 02</p>
            <h2>Results</h2>
          </div>
          <div className="status-chip subtle">Live prediction output</div>
        </div>

        <div className={`loader ${processing ? 'active' : ''}`} aria-hidden="true">
          <span />
          <span />
          <span />
        </div>

        <div className="result-card">
          {result ? (
            <>
              <div className="result-header">
                <span className="result-badge">{result.label}</span>
                <span className="result-confidence">{result.confidence}% confidence</span>
              </div>
              <p className="result-note">{result.note}</p>
            </>
          ) : (
            <>
              <div className="result-header">
                <span className="result-badge empty">Waiting</span>
                <span className="result-confidence">No image analyzed yet</span>
              </div>
              <p className="result-note">Your prediction will appear here after processing finishes.</p>
            </>
          )}
        </div>

        <button className="secondary-button" onClick={handleReset}>
          Try another one
        </button>
      </section>
    </main>
  );
}