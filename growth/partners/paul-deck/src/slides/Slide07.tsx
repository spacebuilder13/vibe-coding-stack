import GraphPaper from '../components/GraphPaper'
import DiagramQuadrant from '../components/DiagramQuadrant'
import { fourForces, buyerJourney } from '../content'
import './Slide07.css'
import '../slides/slides.css'

export default function Slide07() {
  return (
    <div className="s07">
      <GraphPaper vignette />
      <div className="slide-pad">
        <div className="s07__head">
          <span className="slide-eyebrow">Atoms · demand-side sales</span>
          <h2 className="slide-title" style={{ marginTop: 8 }}>Four forces. One moment of switch.</h2>
        </div>

        <div className="s07__body">
          <DiagramQuadrant
            tl={fourForces.tl}
            tr={fourForces.tr}
            bl={fourForces.bl}
            br={fourForces.br}
            timeline={buyerJourney}
            timelineTarget={2}
          />
          <div className="s07__right blur-in blur-in--delay-3">
            <p className="s07__note mono">
              The moment someone hires<br />a new solution is the richest<br />data you'll ever collect.
            </p>
            <div className="s07__tags" style={{ marginTop: 16 }}>
              <span className="tag">Financial products</span>
              <span className="tag">Conscious brand</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
