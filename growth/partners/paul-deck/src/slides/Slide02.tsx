import GraphPaper from '../components/GraphPaper'
import { problemNodes } from '../content'
import './Slide02.css'
import '../slides/slides.css'

export default function Slide02() {
  return (
    <div className="s02">
      <GraphPaper vignette />
      <div className="slide-pad">
        <div className="s02__head">
          <span className="slide-eyebrow">The gap</span>
          <h2 className="slide-title" style={{ marginTop: 8 }}>Insight doesn't automatically<br />become decision.</h2>
        </div>

        <div className="s02__flow-wrap">
          <div className="s02__flow stagger">
            {problemNodes.map((n, i) => (
              <div key={n.label} className={`s02__node-wrap${i < problemNodes.length - 1 ? ' s02__node-wrap--arrow' : ''}`}>
                <div className={`s02__node${n.faded ? ' s02__node--faded' : ''}`}>
                  <span>{n.label}</span>
                </div>
                {i < problemNodes.length - 1 && (
                  <svg className="s02__arrow" viewBox="0 0 32 16" fill="none" aria-hidden="true">
                    <line x1="0" y1="8" x2="22" y2="8" stroke="currentColor" strokeWidth="1.5" />
                    <path d="M18 4 L26 8 L18 12" stroke="currentColor" strokeWidth="1.5" fill="none" />
                  </svg>
                )}
              </div>
            ))}
          </div>

          <p className="s02__shelf-note mono blur-in blur-in--delay-2">
            ↑ the shelf where most research stops
          </p>
        </div>
      </div>
    </div>
  )
}
