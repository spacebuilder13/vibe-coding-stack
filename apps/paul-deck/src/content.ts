/* ─────────────────────────────────────────────────────────────────────────────
   content.ts — all deck data, labels and copy
   No company names. Use abstracted industry segments only.
   ───────────────────────────────────────────────────────────────────────────── */

// SLIDE 2 — problem horizon
export const problemNodes = [
  { label: 'Observation', faded: false },
  { label: 'Framework', faded: false },
  { label: 'Analysis', faded: false },
  { label: 'Insight', faded: false },
  { label: 'Recommendation', faded: false },
  { label: 'Decision', faded: true }, // the shelf — where it usually stops
]

// SLIDE 3 — two worldviews
export const worldviews = {
  left: [
    'behavior in context',
    'qual before quant',
    'participant-centered',
    'typing tools',
    'not a factory',
  ],
  right: [
    'metacognition',
    'living systems',
    'compounding IP',
    'always-on edge',
    'human elevation',
  ],
  center: 'Research that reveals.\nProducts that remember.',
}

// SLIDE 4 — the human center
export const emotionalStates = [
  'CALMNESS',
  'THINKING',
  'PONDERING',
  'PREPAREDNESS',
  'ACCEPTANCE',
  'COURAGE',
  'STRENGTH',
  'WISDOM',
]

// SLIDE 5 — money archetypes
export const moneyArchetypes = [
  { label: 'Soldier', sublabel: 'protection' },
  { label: 'Farmer',   sublabel: 'growth' },
  { label: 'Laborer',  sublabel: 'operations' },
  { label: 'Ambassador', sublabel: 'identity' },
  { label: 'Strategist', sublabel: 'leverage' },
]

export const jmaDimensions = ['Financial', 'Emotional', 'Relational', 'Social', 'Temporal']

// SLIDE 6 — strategy / Spaceships
export const strategyPhases = [
  { label: 'Conversation', tag: 'voice · questions · hypotheses · tensions' },
  { label: 'Structured signal', tag: 'facts · aspirations · contradictions' },
  { label: 'Strategy map', tag: 'positioning · segmentation · differentiation' },
]

export const strategyGrid = {
  xLabel: 'specificity →',
  yLabel: '← confidence',
}

// SLIDE 7 — demand-side / Atoms
export const fourForces = {
  tl: { label: 'F1  PUSH', sub: 'intolerable now — the trigger to move' },
  tr: { label: 'F2  PULL', sub: 'the better future they can see' },
  bl: { label: 'F3  ANXIETY', sub: 'what stops them switching' },
  br: { label: 'F4  HABIT', sub: 'why nothing changes by default' },
}

export const buyerJourney = [
  'First thought',
  'Passive looking',
  'Active looking',
  'Deciding',
  'Onboarding',
  'Ongoing',
]

// SLIDE 8 — consciousness in design
export const geometryForms = [
  { label: 'Incompleteness', tradition: 'Zen' },
  { label: 'Dissolution', tradition: 'Sufism' },
  { label: 'Multiplicity', tradition: 'Jainism' },
  { label: 'Stillness', tradition: 'Yoga' },
  { label: 'Interdependence', tradition: 'Buddhism' },
]

// SLIDE 9 — the factory
export const pipeline = [
  'Brief',
  'Program',
  'Spec',
  'Visual gate',
  'Build',
  'QA',
  'Ship',
]

export const productTiles = [
  { label: 'Financial products', tag: 'advisory agent' },
  { label: 'Manufacturing', tag: 'strategy agent' },
  { label: 'Creative agency', tag: 'positioning agent' },
  { label: 'Conscious brand', tag: 'values agent' },
  { label: 'Professional services', tag: 'cohort agent' },
]

// SLIDE 10 — the Edge loop
export const loopNodes = [
  'Individual understanding',
  'Business + market map',
  'Decision · action',
  'Learning loop',
]

export const loopCenterText = 'The always-on\nEdge.'

// SLIDE 11 — invitation
export const invitationCols = [
  {
    label: 'Research depth',
    items: ['behavioral diagnosis', 'mixed methods', 'segmentation', 'typing tools'],
  },
  {
    label: 'AI productization',
    items: ['conversation agents', 'memory loops', 'synthesis engines', 'release discipline'],
  },
  {
    label: 'Taste + delivery',
    items: ['design systems', 'motion language', 'anti-slop constraints', 'micro-products'],
  },
]

// SLIDE 12 — conversation starters
export const conversationQuestions = [
  'Where do your clients struggle most to apply\nwhat you find?',
  'What parts of behavioral diagnosis feel too\nimportant to ever automate?',
  'Where does insight currently leak before\nit becomes a decision?',
]
