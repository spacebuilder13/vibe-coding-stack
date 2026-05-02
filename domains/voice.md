# Domain: Voice

When to load: brief mentions voice input, voice output, or audio processing.

## ElevenLabs

Connector: `elevenlabs` — see `registry/connectors.json`

### TTS (text-to-speech)
```js
// POST /api/voice-generate
const response = await fetch('https://api.elevenlabs.io/v1/text-to-speech/' + voiceId, {
  method: 'POST',
  headers: {
    'xi-api-key': process.env.ELEVENLABS_API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ text, model_id: 'eleven_turbo_v2', voice_settings: { stability: 0.5, similarity_boost: 0.75 } })
})
const audioBuffer = await response.arrayBuffer()
// return as audio/mpeg
```

### STT (speech-to-text)
```js
// POST /api/voice-transcribe
const formData = new FormData()
formData.append('audio', audioBlob, 'recording.webm')
const response = await fetch('https://api.elevenlabs.io/v1/speech-to-text', {
  method: 'POST',
  headers: { 'xi-api-key': process.env.ELEVENLABS_API_KEY },
  body: formData
})
const { text } = await response.json()
```

### Post-call webhook
```js
// POST /api/elevenlabs/post-call
// Receives: call metadata, transcript, duration
// Use to log session, trigger follow-up actions
```

## Known voice IDs
- Sandy: `EXAVITQu4vr4xnSDxMaL`
- Add new IDs to `registry/connectors.json` → `elevenlabs.known_voice_ids`

## API routes pattern (from project-insurance)
- `POST /api/voice-generate` — TTS
- `POST /api/voice-transcribe` — STT
- `POST /api/elevenlabs/post-call` — webhook handler

## Client-side mic capture
```js
const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
const recorder = new MediaRecorder(stream)
recorder.ondataavailable = (e) => chunks.push(e.data)
recorder.onstop = () => {
  const blob = new Blob(chunks, { type: 'audio/webm' })
  // POST to /api/voice-transcribe
}
```

## Cost notes
ElevenLabs is `high` cost tier — streaming audio is expensive.
Only enable voice if explicitly in PROGRAM.md constraints.
Turbo v2 model is 2x cheaper than standard — use by default.

## Anti-patterns
- Enabling voice without it being in PROGRAM.md
- Using standard model when turbo suffices
- No fallback for mic permission denied
- Streaming audio to client via Vercel Functions without buffer size limit
