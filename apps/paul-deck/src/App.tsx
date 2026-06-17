import SlideDeck, { Slide } from './components/SlideDeck'
import Slide01 from './slides/Slide01'
import Slide02 from './slides/Slide02'
import Slide03 from './slides/Slide03'
import Slide04 from './slides/Slide04'
import Slide05 from './slides/Slide05'
import Slide06 from './slides/Slide06'
import Slide07 from './slides/Slide07'
import Slide08 from './slides/Slide08'
import Slide09 from './slides/Slide09'
import Slide10 from './slides/Slide10'
import Slide11 from './slides/Slide11'
import Slide12 from './slides/Slide12'

const slides: Slide[] = [
  { id: 'opening',       label: 'Opening',       render: () => <Slide01 /> },
  { id: 'gap',           label: 'The gap',        render: () => <Slide02 /> },
  { id: 'worldviews',   label: 'Worldviews',     render: () => <Slide03 /> },
  { id: 'human',         label: 'Human',          render: () => <Slide04 /> },
  { id: 'money',         label: 'Money',          render: () => <Slide05 /> },
  { id: 'spaceships',   label: 'Spaceships',     render: () => <Slide06 /> },
  { id: 'atoms',         label: 'Atoms',          render: () => <Slide07 /> },
  { id: 'consciousness', label: 'Consciousness',  render: () => <Slide08 /> },
  { id: 'factory',       label: 'Factory',        render: () => <Slide09 /> },
  { id: 'edge',          label: 'Edge',           render: () => <Slide10 /> },
  { id: 'invitation',   label: 'Invitation',     render: () => <Slide11 /> },
  { id: 'conversation', label: 'Conversation',   render: () => <Slide12 /> },
]

export default function App() {
  return <SlideDeck slides={slides} />
}
