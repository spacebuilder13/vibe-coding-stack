import './GeometryForms.css'

type Form = { label: string; tradition: string }

type Props = { forms: Form[] }

export default function GeometryForms({ forms }: Props) {
  return (
    <div className="geo-forms stagger">
      {/* 1 — Zen Enso: almost-complete circle */}
      <GeoForm label={forms[0].label} tradition={forms[0].tradition}>
        <svg viewBox="0 0 80 80" fill="none">
          <circle cx="40" cy="40" r="28"
            stroke="currentColor" strokeWidth="2" strokeLinecap="round"
            strokeDasharray="160 22"
            style={{ animation: 'draw-path 1.4s cubic-bezier(0.22,1,0.36,1) forwards', strokeDashoffset: 182 }}
          />
        </svg>
      </GeoForm>

      {/* 2 — Sufism: dissolution (crisp → diffuse rings) */}
      <GeoForm label={forms[1].label} tradition={forms[1].tradition}>
        <svg viewBox="0 0 80 80" fill="none">
          {[{ r: 14, sw: 2, op: 1 }, { r: 26, sw: 1.5, op: 0.55 }, { r: 38, sw: 1, op: 0.22 }].map((ring, i) => (
            <circle key={i} cx="40" cy="40" r={ring.r}
              stroke="currentColor" strokeWidth={ring.sw} opacity={ring.op}
              strokeDasharray="200" strokeDashoffset="200"
              style={{ animation: `draw-path 1.2s cubic-bezier(0.22,1,0.36,1) forwards`, animationDelay: `${i * 0.2}s` }}
            />
          ))}
        </svg>
      </GeoForm>

      {/* 3 — Jainism: three overlapping forms */}
      <GeoForm label={forms[2].label} tradition={forms[2].tradition}>
        <svg viewBox="0 0 80 80" fill="none">
          {[{ cx: 34, cy: 34 }, { cx: 46, cy: 34 }, { cx: 40, cy: 46 }].map((c, i) => (
            <circle key={i} cx={c.cx} cy={c.cy} r="20"
              stroke="currentColor" strokeWidth="1.5" opacity="0.7"
              strokeDasharray="200" strokeDashoffset="200"
              style={{ animation: 'draw-path 1.2s cubic-bezier(0.22,1,0.36,1) forwards', animationDelay: `${i * 0.25}s` }}
            />
          ))}
        </svg>
      </GeoForm>

      {/* 4 — Yoga: concentric rings, outer dashed (turbulent → still) */}
      <GeoForm label={forms[3].label} tradition={forms[3].tradition}>
        <svg viewBox="0 0 80 80" fill="none">
          <circle cx="40" cy="40" r="8"  stroke="currentColor" strokeWidth="2.5"
            strokeDasharray="200" strokeDashoffset="200"
            style={{ animation: 'draw-path 0.8s cubic-bezier(0.22,1,0.36,1) forwards' }} />
          <circle cx="40" cy="40" r="20" stroke="currentColor" strokeWidth="1.5"
            strokeDasharray="200" strokeDashoffset="200"
            style={{ animation: 'draw-path 1s cubic-bezier(0.22,1,0.36,1) forwards', animationDelay: '0.2s' }} />
          <circle cx="40" cy="40" r="30" stroke="currentColor" strokeWidth="1" strokeDasharray="6 4"
            strokeDashoffset="200"
            style={{ animation: 'draw-path 1.2s cubic-bezier(0.22,1,0.36,1) forwards', animationDelay: '0.4s' }} />
          <circle cx="40" cy="40" r="38" stroke="currentColor" strokeWidth="0.75" strokeDasharray="3 6"
            strokeDashoffset="200"
            style={{ animation: 'draw-path 1.4s cubic-bezier(0.22,1,0.36,1) forwards', animationDelay: '0.6s' }} />
        </svg>
      </GeoForm>

      {/* 5 — Buddhism: interdependent network */}
      <GeoForm label={forms[4].label} tradition={forms[4].tradition}>
        <svg viewBox="0 0 80 80" fill="none">
          {/* 6 nodes: 1 center + 5 peripheral */}
          {[
            { cx: 40, cy: 40 }, // center
            { cx: 40, cy: 14 }, // top
            { cx: 62, cy: 27 }, // tr
            { cx: 62, cy: 53 }, // br
            { cx: 40, cy: 66 }, // bottom
            { cx: 18, cy: 40 }, // left
          ].map((n, i) => {
            if (i === 0) return null
            return (
              <line key={i} x1="40" y1="40" x2={n.cx} y2={n.cy}
                stroke="currentColor" strokeWidth="1"
                strokeDasharray="60" strokeDashoffset="60"
                style={{ animation: 'draw-path 0.8s cubic-bezier(0.22,1,0.36,1) forwards', animationDelay: `${i * 0.12}s` }}
              />
            )
          })}
          {/* outer ring connections */}
          {[[1,2],[2,3],[3,4],[4,5],[5,1]].map(([a,b], i) => {
            const pts = [
              { cx: 40, cy: 14 },
              { cx: 62, cy: 27 },
              { cx: 62, cy: 53 },
              { cx: 40, cy: 66 },
              { cx: 18, cy: 40 },
            ]
            return (
              <line key={`r${i}`} x1={pts[a-1].cx} y1={pts[a-1].cy} x2={pts[b-1].cx} y2={pts[b-1].cy}
                stroke="currentColor" strokeWidth="0.75" opacity="0.5"
                strokeDasharray="60" strokeDashoffset="60"
                style={{ animation: 'draw-path 0.7s cubic-bezier(0.22,1,0.36,1) forwards', animationDelay: `${0.7 + i * 0.1}s` }}
              />
            )
          })}
          {/* Node dots */}
          {[
            { cx: 40, cy: 40, r: 4 },
            { cx: 40, cy: 14, r: 3 },
            { cx: 62, cy: 27, r: 3 },
            { cx: 62, cy: 53, r: 3 },
            { cx: 40, cy: 66, r: 3 },
            { cx: 18, cy: 40, r: 3 },
          ].map((n, i) => (
            <circle key={`d${i}`} cx={n.cx} cy={n.cy} r={n.r} fill="currentColor" opacity={i === 0 ? 1 : 0.6} />
          ))}
        </svg>
      </GeoForm>
    </div>
  )
}

function GeoForm({ label, tradition, children }: Form & { children: React.ReactNode }) {
  return (
    <div className="geo-form">
      <div className="geo-form__svg">{children}</div>
      <span className="geo-form__label mono">{label}</span>
      <span className="geo-form__tradition mono">{tradition}</span>
    </div>
  )
}
