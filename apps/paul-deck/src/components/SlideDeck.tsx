import { useCallback, useEffect, useState } from 'react'
import './SlideDeck.css'

export type Slide = {
  id: string
  label: string
  render: () => JSX.Element
}

function readHashIndex(total: number): number {
  const raw = window.location.hash.replace('#', '')
  const n = parseInt(raw, 10)
  if (Number.isFinite(n)) return Math.min(total - 1, Math.max(0, n - 1))
  return 0
}

export default function SlideDeck({ slides }: { slides: Slide[] }) {
  const total = slides.length
  const [index, setIndex] = useState(() => readHashIndex(total))

  const go = useCallback(
    (next: number) => {
      setIndex((cur) => {
        const clamped = Math.min(total - 1, Math.max(0, next ?? cur))
        window.history.replaceState(null, '', `#${clamped + 1}`)
        return clamped
      })
    },
    [total],
  )

  useEffect(() => {
    window.history.replaceState(null, '', `#${index + 1}`)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowRight':
        case 'PageDown':
        case ' ':
          e.preventDefault(); go(index + 1); break
        case 'ArrowLeft':
        case 'PageUp':
          e.preventDefault(); go(index - 1); break
        case 'Home': go(0); break
        case 'End':  go(total - 1); break
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [index, go, total])

  const current = slides[index]

  return (
    <div className="deck">
      <button className="deck-zone deck-zone--left"  aria-label="Previous" onClick={() => go(index - 1)} disabled={index === 0} />
      <button className="deck-zone deck-zone--right" aria-label="Next"     onClick={() => go(index + 1)} disabled={index === total - 1} />

      <header className="deck-topbar">
        <div className="deck-brand">
          <span className="deck-dot" />
          <span className="mono deck-brand-text">Spaceships &amp; Atoms</span>
        </div>
        <div className="mono deck-counter">
          {String(index + 1).padStart(2, '0')}
          <span className="deck-counter-sep"> / </span>
          {String(total).padStart(2, '0')}
          <span className="deck-counter-label"> · {current.label}</span>
        </div>
      </header>

      <main className="deck-stage">
        {/* key change triggers CSS animation on remount */}
        <section key={current.id} className="deck-slide">
          {current.render()}
        </section>
      </main>

      <footer className="deck-railbar">
        <button className="deck-arrow mono" onClick={() => go(index - 1)} disabled={index === 0} aria-label="Previous">←</button>
        <div className="deck-rail" role="tablist" aria-label="Slides">
          {slides.map((s, i) => (
            <button
              key={s.id}
              className={`deck-rail-dot${i === index ? ' is-active' : ''}`}
              aria-label={`${i + 1}. ${s.label}`}
              aria-selected={i === index}
              onClick={() => go(i)}
            >
              <span className="deck-rail-tip mono">{s.label}</span>
            </button>
          ))}
        </div>
        <button className="deck-arrow mono" onClick={() => go(index + 1)} disabled={index === total - 1} aria-label="Next">→</button>
      </footer>
    </div>
  )
}
