import './DiagramQuadrant.css'

type Q = { label: string; sub: string }

type Props = {
  tl: Q; tr: Q; bl: Q; br: Q
  timeline?: string[]
  timelineTarget?: number
}

export default function DiagramQuadrant({ tl, tr, bl, br, timeline, timelineTarget = 2 }: Props) {
  return (
    <div className="dquad">
      <div className="dquad__grid stagger">
        {[tl, tr, bl, br].map((q, i) => (
          <div key={i} className={`dquad__cell${i >= 2 ? ' dquad__cell--bottom' : ''}`}>
            <span className="dquad__label mono">{q.label}</span>
            <span className="dquad__sub">{q.sub}</span>
          </div>
        ))}
        <div className="dquad__vline" aria-hidden="true" />
        <div className="dquad__hline" aria-hidden="true" />
      </div>

      {timeline && (
        <div className="dquad__timeline blur-in blur-in--delay-3">
          {timeline.map((step, i) => (
            <div key={step} className={`dquad__step${i === timelineTarget ? ' dquad__step--active' : ''}`}>
              <div className="dquad__step-dot" />
              <span className="dquad__step-label mono">{step}</span>
            </div>
          ))}
          <div className="dquad__timeline-line" aria-hidden="true" />
        </div>
      )}
    </div>
  )
}
