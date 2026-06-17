import { useEffect, useState } from 'react'
import GraphPaper from '../components/GraphPaper'
import LivingLines from '../components/LivingLines'
import './Slide01.css'

const QUESTION = '"What makes that behavior logical?"'

export default function Slide01() {
  const [displayed, setDisplayed] = useState('')
  const [done, setDone] = useState(false)

  useEffect(() => {
    const delay = 1600 / QUESTION.length
    let i = 0
    const timer = setInterval(() => {
      setDisplayed(QUESTION.slice(0, i + 1))
      i++
      if (i >= QUESTION.length) {
        clearInterval(timer)
        setDone(true)
      }
    }, delay)
    return () => clearInterval(timer)
  }, [])

  return (
    <div className="s01">
      <GraphPaper vignette />
      <LivingLines mode="dotwave" className="s01__canvas" />
      <div className="s01__center">
        <p className="s01__question serif">{displayed}<span className={`s01__cursor${done ? ' s01__cursor--hidden' : ''}`}>|</span></p>
        <p className="s01__byline mono blur-in blur-in--delay-4">Paul Harwood · Behavioral science · 101 Research</p>
      </div>
    </div>
  )
}
