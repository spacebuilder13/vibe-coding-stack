import GraphPaper from '../components/GraphPaper'
import LivingLines from '../components/LivingLines'
import { conversationQuestions } from '../content'
import './Slide12.css'
import '../slides/slides.css'

export default function Slide12() {
  return (
    <div className="s12">
      <GraphPaper vignette />
      <LivingLines mode="dotwave" className="s12__canvas" />
      <div className="slide-pad">
        <div style={{ marginBottom: 40 }}>
          <span className="slide-eyebrow">To start</span>
        </div>
        <div className="s12__cards stagger">
          {conversationQuestions.map((q, i) => (
            <div key={i} className="s12__card">
              <span className="s12__card-num mono">0{i + 1}</span>
              <p className="s12__card-q serif">{q}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
