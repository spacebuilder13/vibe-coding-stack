import './DiagramFlow.css'

type Phase = { label: string; tag: string }

type Props = {
  phases: Phase[]
  rightPanel?: { xLabel: string; yLabel: string }
}

export default function DiagramFlow({ phases, rightPanel }: Props) {
  return (
    <div className="dflow">
      <div className="dflow__phases stagger">
        {phases.map((p, i) => (
          <div key={p.label} className="dflow__phase-wrap">
            <div className="dflow__phase">
              <span className="dflow__phase-label">{p.label}</span>
              <span className="dflow__phase-tag mono">{p.tag}</span>
            </div>
            {i < phases.length - 1 && (
              <div className="dflow__arrow" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none">
                  <line x1="12" y1="0" x2="12" y2="16" stroke="currentColor" strokeWidth="1.5" />
                  <path d="M7 12 L12 20 L17 12" stroke="currentColor" strokeWidth="1.5" fill="none" />
                </svg>
              </div>
            )}
          </div>
        ))}
      </div>

      {rightPanel && (
        <div className="dflow__grid-wrap blur-in blur-in--delay-3">
          <div className="dflow__grid">
            <div className="dflow__grid-inner">
              <div className="dflow__grid-cell dflow__grid-cell--active" />
              <div className="dflow__grid-cell" />
              <div className="dflow__grid-cell" />
              <div className="dflow__grid-cell" />
            </div>
            <span className="dflow__axis dflow__axis--x mono">{rightPanel.xLabel}</span>
            <span className="dflow__axis dflow__axis--y mono">{rightPanel.yLabel}</span>
            <svg className="dflow__cross" viewBox="0 0 60 60" aria-hidden="true">
              <line className="dflow__cross-line" x1="30" y1="8" x2="30" y2="52" stroke="var(--color-sandy-gold)" strokeWidth="1.5" />
              <line className="dflow__cross-line" x1="8" y1="30" x2="52" y2="30" stroke="var(--color-sandy-gold)" strokeWidth="1.5" />
              <circle cx="30" cy="30" r="4" fill="var(--color-sandy-gold)" />
            </svg>
          </div>
        </div>
      )}
    </div>
  )
}
