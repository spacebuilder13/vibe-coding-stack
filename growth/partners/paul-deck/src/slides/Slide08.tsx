import GraphPaper from '../components/GraphPaper'
import GeometryForms from '../components/GeometryForms'
import { geometryForms } from '../content'
import './Slide08.css'
import '../slides/slides.css'

export default function Slide08() {
  return (
    <div className="s08">
      <GraphPaper vignette />
      <div className="slide-pad">
        <div className="s08__head">
          <span className="slide-eyebrow">Design philosophy · conscious brand</span>
        </div>

        <div className="s08__body">
          <div className="s08__forms-wrap">
            <GeometryForms forms={geometryForms} />
          </div>
          <p className="s08__thesis serif blur-in blur-in--delay-3">
            Every product carries<br />a philosophy of the person<br />who might use it.
          </p>
        </div>
      </div>
    </div>
  )
}
