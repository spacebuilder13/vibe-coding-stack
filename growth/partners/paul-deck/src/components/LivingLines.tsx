import { useEffect, useRef } from 'react'

type Mode = 'dotwave' | 'dissolve'

type Props = {
  mode?: Mode
  gap?: number
  color?: string
  accent?: string
  className?: string
  style?: React.CSSProperties
  period?: number
}

const INK = 'rgba(27,26,23,'
const GOLD = '196,152,58'

export default function LivingLines({
  mode = 'dotwave',
  gap = 26,
  color = INK,
  accent = GOLD,
  className = '',
  style,
  period = 7,
}: Props) {
  const ref = useRef<HTMLCanvasElement | null>(null)

  useEffect(() => {
    const canvas = ref.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    let raf = 0
    let w = 0
    let h = 0
    let dpr = Math.min(window.devicePixelRatio || 1, 2)

    type Dot = { hx: number; hy: number; rx: number; ry: number }
    let dots: Dot[] = []

    const build = () => {
      const rect = canvas.getBoundingClientRect()
      w = Math.max(1, rect.width)
      h = Math.max(1, rect.height)
      dpr = Math.min(window.devicePixelRatio || 1, 2)
      canvas.width = Math.floor(w * dpr)
      canvas.height = Math.floor(h * dpr)
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      dots = []
      const cols = Math.ceil(w / gap) + 1
      const rows = Math.ceil(h / gap) + 1
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const hx = c * gap
          const hy = r * gap
          const ang = Math.random() * Math.PI * 2
          const dist = 40 + Math.random() * 120
          dots.push({ hx, hy, rx: hx + Math.cos(ang) * dist, ry: hy + Math.sin(ang) * dist })
        }
      }
    }

    const start = performance.now()
    const easeInOut = (t: number) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2)

    const frame = (now: number) => {
      const t = (now - start) / 1000
      ctx.clearRect(0, 0, w, h)

      if (mode === 'dissolve') {
        const phase = (t % period) / period
        let order: number
        if (phase < 0.45) order = easeInOut(phase / 0.45)
        else if (phase < 0.7) order = 1
        else order = 1 - easeInOut((phase - 0.7) / 0.3)

        for (let i = 0; i < dots.length; i++) {
          const d = dots[i]
          const x = d.rx + (d.hx - d.rx) * order
          const y = d.ry + (d.hy - d.ry) * order
          const a = 0.12 + order * 0.46
          const size = 0.8 + order * 1.0
          if (order > 0.86) {
            const m = (order - 0.86) / 0.14
            ctx.fillStyle = `rgba(${accent},${(0.5 * m).toFixed(3)})`
            ctx.beginPath()
            ctx.arc(x, y, size + 0.6, 0, Math.PI * 2)
            ctx.fill()
          }
          ctx.fillStyle = `${color}${a.toFixed(3)})`
          ctx.beginPath()
          ctx.arc(x, y, size, 0, Math.PI * 2)
          ctx.fill()
        }
      } else {
        for (let i = 0; i < dots.length; i++) {
          const d = dots[i]
          const wave = Math.sin((d.hx + d.hy) * 0.012 - t * 1.6)
          const a = 0.08 + (wave * 0.5 + 0.5) * 0.34
          ctx.fillStyle = `${color}${a.toFixed(3)})`
          ctx.beginPath()
          ctx.arc(d.hx, d.hy, 1.1, 0, Math.PI * 2)
          ctx.fill()
        }
      }

      if (!reduce) raf = requestAnimationFrame(frame)
    }

    build()
    if (reduce) {
      ctx.clearRect(0, 0, w, h)
      for (const d of dots) {
        ctx.fillStyle = `${color}0.4)`
        ctx.beginPath()
        ctx.arc(d.hx, d.hy, 1.1, 0, Math.PI * 2)
        ctx.fill()
      }
    } else {
      raf = requestAnimationFrame(frame)
    }

    const onResize = () => build()
    window.addEventListener('resize', onResize)
    return () => { cancelAnimationFrame(raf); window.removeEventListener('resize', onResize) }
  }, [mode, gap, color, accent, period])

  return (
    <canvas
      ref={ref}
      className={className}
      aria-hidden="true"
      style={{ display: 'block', width: '100%', height: '100%', ...style }}
    />
  )
}
