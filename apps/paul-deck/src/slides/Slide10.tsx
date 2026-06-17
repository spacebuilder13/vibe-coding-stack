import GraphPaper from '../components/GraphPaper'
import LivingLines from '../components/LivingLines'
import DiagramLoop from '../components/DiagramLoop'
import { loopNodes, loopCenterText } from '../content'
import './Slide10.css'
import '../slides/slides.css'

export default function Slide10() {
  return (
    <div className="s10">
      <GraphPaper vignette />
      <LivingLines mode="dissolve" className="s10__canvas" period={9} />
      <div className="slide-pad">
        <div className="s10__head">
          <span className="slide-eyebrow">The edge · compounding intelligence</span>
        </div>
        <div className="s10__body">
          <DiagramLoop nodes={loopNodes} centerText={loopCenterText} />
        </div>
      </div>
    </div>
  )
}
