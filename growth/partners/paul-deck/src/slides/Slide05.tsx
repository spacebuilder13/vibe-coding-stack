import GraphPaper from '../components/GraphPaper'
import DiagramFiveNodes from '../components/DiagramFiveNodes'
import { moneyArchetypes, jmaDimensions } from '../content'
import './Slide05.css'
import '../slides/slides.css'

export default function Slide05() {
  return (
    <div className="s05">
      <GraphPaper vignette />
      <div className="slide-pad">
        <div className="s05__head">
          <span className="slide-eyebrow">Financial products · behavioral layer</span>
          <h2 className="slide-title" style={{ marginTop: 8 }}>Money as identity,<br />emotion, relationship, meaning.</h2>
        </div>

        <div className="s05__body">
          <DiagramFiveNodes nodes={moneyArchetypes} dimensions={jmaDimensions} />
          <div className="s05__right">
            <p className="s05__caption mono blur-in blur-in--delay-2">
              five archetypal relationships<br />with money — in every product<br />decision, one is dominant
            </p>
            <span className="tag tag--gold blur-in blur-in--delay-3" style={{ marginTop: 16 }}>Financial products</span>
          </div>
        </div>
      </div>
    </div>
  )
}
