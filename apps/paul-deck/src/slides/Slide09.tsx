import GraphPaper from '../components/GraphPaper'
import { pipeline, productTiles } from '../content'
import './Slide09.css'
import '../slides/slides.css'

export default function Slide09() {
  return (
    <div className="s09">
      <GraphPaper vignette />
      <div className="slide-pad">
        <div className="s09__head">
          <span className="slide-eyebrow">The factory · micro-product delivery</span>
          <h2 className="slide-title" style={{ marginTop: 8 }}>Brief to artifact.<br />Every time.</h2>
        </div>

        <div className="s09__body">
          {/* Pipeline */}
          <div className="s09__pipeline stagger">
            {pipeline.map((step, i) => (
              <div key={step} className="s09__pipeline-item">
                <div className="s09__pipeline-node">{step}</div>
                {i < pipeline.length - 1 && (
                  <svg className="s09__pipe-arrow" viewBox="0 0 20 14" fill="none" aria-hidden="true">
                    <line x1="0" y1="7" x2="12" y2="7" stroke="currentColor" strokeWidth="1.5" />
                    <path d="M9 3 L15 7 L9 11" stroke="currentColor" strokeWidth="1.5" fill="none" />
                  </svg>
                )}
              </div>
            ))}
          </div>

          {/* Product tiles */}
          <div className="s09__tiles stagger">
            {productTiles.map((p) => (
              <div key={p.label} className="s09__tile">
                <span className="s09__tile-label">{p.label}</span>
                <span className="s09__tile-tag mono">{p.tag}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
