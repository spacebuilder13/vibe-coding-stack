import GraphPaper from '../components/GraphPaper'
import DiagramFlow from '../components/DiagramFlow'
import { strategyPhases, strategyGrid } from '../content'
import './Slide06.css'
import '../slides/slides.css'

export default function Slide06() {
  return (
    <div className="s06">
      <GraphPaper vignette />
      <div className="slide-pad">
        <div className="s06__head">
          <span className="slide-eyebrow">Spaceships · strategy articulation</span>
          <h2 className="slide-title" style={{ marginTop: 8 }}>From founder voice<br />to market map.</h2>
        </div>

        <div className="s06__body">
          <DiagramFlow phases={strategyPhases} rightPanel={strategyGrid} />
          <div className="s06__tags blur-in blur-in--delay-4">
            <span className="tag">Manufacturing</span>
            <span className="tag">Creative agency</span>
            <span className="tag">Professional services</span>
          </div>
        </div>
      </div>
    </div>
  )
}
