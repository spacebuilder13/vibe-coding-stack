import GraphPaper from '../components/GraphPaper'
import { emotionalStates } from '../content'
import './Slide04.css'
import '../slides/slides.css'

export default function Slide04() {
  return (
    <div className="s04">
      <GraphPaper vignette breathe />
      <div className="slide-pad s04__pad">
        <span className="slide-eyebrow" style={{ marginBottom: 12 }}>The human center</span>

        <div className="s04__stage">
          {/* Orbit ring */}
          <div className="s04__orbit-wrap">
            <div className="s04__orbit-ring" aria-hidden="true" />
            {emotionalStates.map((state, i) => {
              const angleDeg = (i / emotionalStates.length) * 360 - 90
              return (
                <div
                  key={state}
                  className="s04__orbit-label mono"
                  style={{ '--angle': `${angleDeg}deg` } as React.CSSProperties}
                >
                  {state}
                </div>
              )
            })}
            {/* Center dot */}
            <div className="s04__center-dot" />
          </div>

          {/* Thesis */}
          <p className="s04__thesis serif blur-in blur-in--delay-2">
            Every product interaction<br />is a conversation with the self.
          </p>
        </div>
      </div>
    </div>
  )
}
