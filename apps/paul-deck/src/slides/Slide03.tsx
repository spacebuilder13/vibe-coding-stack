import GraphPaper from '../components/GraphPaper'
import ChipCloud from '../components/ChipCloud'
import { worldviews } from '../content'
import './Slide03.css'
import '../slides/slides.css'

export default function Slide03() {
  return (
    <div className="s03">
      <GraphPaper vignette />
      <div className="slide-pad">
        <div style={{ marginBottom: 36 }}>
          <span className="slide-eyebrow">Two worldviews, one table</span>
        </div>
        <div className="s03__cloud-wrap">
          <ChipCloud
            left={worldviews.left}
            right={worldviews.right}
            centerText={worldviews.center}
          />
        </div>
      </div>
    </div>
  )
}
