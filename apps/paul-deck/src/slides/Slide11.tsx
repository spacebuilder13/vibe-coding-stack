import GraphPaper from '../components/GraphPaper'
import { invitationCols } from '../content'
import './Slide11.css'
import '../slides/slides.css'

export default function Slide11() {
  return (
    <div className="s11">
      <GraphPaper vignette />
      <div className="slide-pad">
        <div className="s11__head">
          <span className="slide-eyebrow">An intersection</span>
          <h2 className="slide-title" style={{ marginTop: 8 }}>Where your depth meets<br />our delivery system.</h2>
        </div>

        <div className="s11__grid stagger">
          {invitationCols.map((col) => (
            <div key={col.label} className="s11__col">
              <div className="s11__col-head">
                <div className="s11__col-dot" />
                <span className="s11__col-label mono">{col.label}</span>
              </div>
              <ul className="s11__items">
                {col.items.map((item) => (
                  <li key={item} className="s11__item">
                    <span className="s11__item-dot" aria-hidden="true" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <p className="s11__footnote mono blur-in blur-in--delay-4">
          research depth × AI productization × taste = compounding advantage
        </p>
      </div>
    </div>
  )
}
