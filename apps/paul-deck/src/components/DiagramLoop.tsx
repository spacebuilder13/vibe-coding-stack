import './DiagramLoop.css'

type Props = {
  nodes: string[]
  centerText?: string
}

export default function DiagramLoop({ nodes, centerText }: Props) {
  return (
    <div className="dloop">
      <div className="dloop__track stagger">
        {nodes.map((node, i) => (
          <div key={node} className="dloop__item">
            <div className="dloop__node">
              <span className="dloop__node-text">{node}</span>
            </div>
            {i < nodes.length - 1 && (
              <div className="dloop__connector" aria-hidden="true">
                <svg viewBox="0 0 24 32" fill="none">
                  <line x1="12" y1="0" x2="12" y2="22" stroke="var(--color-sandy-line-strong)" strokeWidth="1.5" />
                  <path d="M8 17 L12 26 L16 17" stroke="var(--color-sandy-line-strong)" strokeWidth="1.5" fill="none" />
                </svg>
              </div>
            )}
          </div>
        ))}

        {/* Loop-back arrow */}
        <div className="dloop__loopback" aria-hidden="true">
          <svg viewBox="0 0 80 120" fill="none" preserveAspectRatio="none">
            <path
              d="M40 0 L40 20 Q40 40 60 40 L76 40 Q80 40 80 44 L80 76 Q80 80 76 80 L60 80 Q40 80 40 100 L40 120"
              stroke="var(--color-sandy-gold)"
              strokeWidth="1.5"
              fill="none"
              strokeDasharray="400"
              strokeDashoffset="400"
              style={{
                animation: 'draw-path 1.8s cubic-bezier(0.22,1,0.36,1) forwards',
                animationDelay: '0.8s',
              }}
            />
            <path d="M36 116 L40 124 L44 116" stroke="var(--color-sandy-gold)" strokeWidth="1.5" fill="none"
              strokeDasharray="30" strokeDashoffset="30"
              style={{ animation: 'draw-path 0.4s ease forwards', animationDelay: '2.5s' }}
            />
          </svg>
        </div>
      </div>

      {centerText && (
        <p className="dloop__center-text blur-in blur-in--delay-2 serif">{centerText}</p>
      )}
    </div>
  )
}
