import './ChipCloud.css'

type Props = {
  left: string[]
  right: string[]
  centerText: string
}

export default function ChipCloud({ left, right, centerText }: Props) {
  return (
    <div className="chip-cloud">
      <div className="chip-cloud__col stagger">
        {left.map((c) => (
          <span key={c} className="chip chip--left">{c}</span>
        ))}
      </div>

      <div className="chip-cloud__divider" aria-hidden="true">
        <div className="chip-cloud__line" />
        <p className="chip-cloud__center blur-in blur-in--delay-2 serif">{centerText}</p>
        <div className="chip-cloud__line" />
      </div>

      <div className="chip-cloud__col stagger">
        {right.map((c) => (
          <span key={c} className="chip chip--right">{c}</span>
        ))}
      </div>
    </div>
  )
}
