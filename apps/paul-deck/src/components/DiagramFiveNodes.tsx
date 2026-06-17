import './DiagramFiveNodes.css'

type Node = { label: string; sublabel: string }

type Props = {
  nodes: Node[]
  dimensions?: string[]
}

export default function DiagramFiveNodes({ nodes, dimensions }: Props) {
  // Pentagon positions (0 = top, going clockwise)
  const cx = 140
  const cy = 130
  const r = 90

  const positions = nodes.map((_, i) => {
    const angle = (i / nodes.length) * Math.PI * 2 - Math.PI / 2
    return { x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle) }
  })

  return (
    <div className="dfive">
      <div className="dfive__svg-wrap stagger">
        <svg viewBox="0 0 280 260" className="dfive__svg" aria-hidden="true">
          {/* Connecting pentagon outline */}
          <polygon
            points={positions.map((p) => `${p.x},${p.y}`).join(' ')}
            fill="none"
            stroke="var(--color-sandy-line)"
            strokeWidth="1"
            strokeDasharray="600"
            strokeDashoffset="600"
            style={{ animation: 'draw-path 1.4s cubic-bezier(0.22,1,0.36,1) forwards', animationDelay: '0.2s' }}
          />

          {/* Spoke lines from center */}
          {positions.map((p, i) => (
            <line
              key={i}
              x1={cx} y1={cy}
              x2={p.x} y2={p.y}
              stroke="var(--color-sandy-line)"
              strokeWidth="0.75"
              strokeDasharray="120"
              strokeDashoffset="120"
              style={{ animation: 'draw-path 0.8s cubic-bezier(0.22,1,0.36,1) forwards', animationDelay: `${0.3 + i * 0.1}s` }}
            />
          ))}

          {/* Node circles */}
          {positions.map((p, i) => (
            <g key={i}>
              <circle
                cx={p.x} cy={p.y} r="26"
                fill="var(--color-sandy-surface)"
                stroke="var(--color-sandy-line-strong)"
                strokeWidth="1"
                style={{ filter: 'drop-shadow(0 2px 6px rgba(27,26,23,0.07))' }}
              />
              <text x={p.x} y={p.y - 4} textAnchor="middle" className="dfive__node-label">{nodes[i].label}</text>
              <text x={p.x} y={p.y + 11} textAnchor="middle" className="dfive__node-sub">{nodes[i].sublabel}</text>
            </g>
          ))}

          {/* Center dot */}
          <circle cx={cx} cy={cy} r="4" fill="var(--color-sandy-gold)" />
        </svg>
      </div>

      {dimensions && (
        <div className="dfive__dims blur-in blur-in--delay-3">
          {dimensions.map((d) => (
            <span key={d} className="dfive__dim mono">{d}</span>
          ))}
        </div>
      )}
    </div>
  )
}
