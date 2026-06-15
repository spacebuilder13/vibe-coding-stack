#!/usr/bin/env python3
"""
WHEN Travel — Transcript extraction engine.

Reads the system prompt from docs/schemas/when-travel-extraction.md,
processes all .docx and .txt files in the given folder (or the uploads
directory), calls Claude, and writes crm_extracted.json.

Usage (from repo root):
    ANTHROPIC_API_KEY=sk-ant-... python3 tools/attio-ingest/extract.py <folder>

The extraction intelligence lives in docs/schemas/when-travel-extraction.md.
Edit that file to change what gets extracted. Do not edit this script for
prompt changes.
"""

import os, sys, re, json, time, zipfile, urllib.request, urllib.error

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not ANTHROPIC_KEY:
    sys.exit("ANTHROPIC_API_KEY not set")

REPO_ROOT   = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMA_FILE = os.path.join(REPO_ROOT, "docs", "schemas", "when-travel-extraction.md")
OUT_FILE    = os.path.join(REPO_ROOT, "tools", "attio-ingest", "crm_extracted.json")

# ── Load prompt from MD file ───────────────────────────────────────────────────

def load_system_prompt(md_path):
    with open(md_path) as f:
        content = f.read()
    match = re.search(r'```system_prompt\n(.*?)\n```', content, re.DOTALL)
    if not match:
        sys.exit(f"Could not find ```system_prompt block in {md_path}")
    return match.group(1).strip()

# ── Text extraction ────────────────────────────────────────────────────────────

def read_docx(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml').decode('utf-8')
    text = re.sub(r'<[^>]+>', ' ', xml)
    return re.sub(r'\s+', ' ', text).strip()

def read_txt(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def read_file(path):
    if path.lower().endswith('.docx'):
        return read_docx(path)
    elif path.lower().endswith('.txt'):
        return read_txt(path)
    return None

# ── Person grouping ────────────────────────────────────────────────────────────

def person_key(filename):
    """Extract (person_name, session_number) from filename."""
    name = filename.split('-', 1)[-1]  # strip UUID prefix if present
    name = re.sub(r'_Notes_by_Gemini\.(docx|txt)$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\.(docx|txt)$', '', name, flags=re.IGNORECASE)
    m = re.search(r'[Ss]ession[_\s]+(\d+)', name)
    session_num = int(m.group(1)) if m else 0
    person = re.split(r'[_\s]+[Ss]ession', name)[0].strip('_ ')
    person = re.sub(r'_+', ' ', person).strip()
    # Fix known typos
    if person.lower().startswith('uravshi'):
        person = 'Urvashi'
    if person.lower().startswith('shruthi') or person.lower().startswith('shruthi'):
        person = person  # keep as-is
    return person, session_num

# ── Claude call ────────────────────────────────────────────────────────────────

def call_claude(system_prompt, combined_text):
    body = json.dumps({
        'model': 'claude-haiku-4-5-20251001',
        'max_tokens': 800,
        'system': system_prompt,
        'messages': [{'role': 'user', 'content': combined_text}]
    }).encode()
    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages', data=body,
        headers={
            'x-api-key': ANTHROPIC_KEY,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        },
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.load(r)
    raw = result['content'][0]['text'].strip()
    raw = re.sub(r'```json\n?|```\n?', '', raw).strip()
    return json.loads(raw)

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 tools/attio-ingest/extract.py <folder>")

    folder = sys.argv[1]
    if not os.path.isdir(folder):
        sys.exit(f"Not a directory: {folder}")

    print(f"→ Loading extraction prompt from {SCHEMA_FILE}")
    system_prompt = load_system_prompt(SCHEMA_FILE)
    print(f"   Prompt loaded ({len(system_prompt)} chars)\n")

    # Collect all files
    all_files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(('.docx', '.txt')) and not f.startswith('.')
    ]

    if not all_files:
        sys.exit(f"No .docx or .txt files found in {folder}")

    # Group by person, sorted by session number (oldest first for context,
    # but we'll reverse when building the combined text so newest is prominent)
    by_person = {}
    for fname in all_files:
        person, session = person_key(fname)
        by_person.setdefault(person, []).append((session, fname))
    for p in by_person:
        by_person[p].sort()

    print(f"→ Found {len(all_files)} file(s) across {len(by_person)} person(s):")
    for p, sessions in sorted(by_person.items()):
        print(f"   {p}: {len(sessions)} session(s)")
    print()

    # Load existing results to preserve records not in this folder
    existing = []
    existing_names = set()
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE) as f:
            existing = json.load(f)
        existing_names = {r.get('name', '').split()[0].lower() for r in existing}
        print(f"→ Existing crm_extracted.json has {len(existing)} record(s)\n")

    results = {}
    for person, sessions in sorted(by_person.items()):
        # Build combined text: newest sessions first (most current state prominent)
        parts = []
        total = 0
        for session_num, fname in reversed(sessions):
            path = os.path.join(folder, fname)
            text = read_file(path)
            if not text or len(text.strip()) < 80:
                print(f"   ~ {fname} — too short, skipping")
                continue
            chunk = f'[Session {session_num}]\n{text[:4000]}'
            if total + len(chunk) > 12000:
                break
            parts.append(chunk)
            total += len(chunk)

        if not parts:
            print(f"   ✗ {person} — no usable content")
            continue

        combined = '\n\n---\n\n'.join(parts)
        print(f"→ {person} ({len(sessions)} session(s), {total} chars sent to Claude)")

        try:
            extracted = call_claude(system_prompt, combined)
            if not extracted.get('name'):
                extracted['name'] = person.split()[0]
            results[person] = extracted
            # Show the qualitative fields
            print(f"   ✓ stage={extracted.get('journey_stage')}")
            print(f"     jtbd_functional: {extracted.get('jtbd_functional', '')[:80]}")
            print(f"     jtbd_emotional:  {extracted.get('jtbd_emotional', '')[:80]}")
            print(f"     blocker_type:    {extracted.get('blocker_type')}")
            print(f"     quote:           {str(extracted.get('memorable_quote', ''))[:80]}")
        except Exception as e:
            print(f"   ✗ Claude error: {e}")
            results[person] = {'name': person.split()[0], 'error': str(e)}

        time.sleep(0.5)
        print()

    # Merge: update existing records, add new ones
    final = []
    processed_firsts = {p.split()[0].lower() for p in results}
    for record in existing:
        first = record.get('name', '').split()[0].lower()
        if first in processed_firsts:
            continue  # will be replaced by fresh extraction
        final.append(record)

    for person, data in results.items():
        final.append(data)

    with open(OUT_FILE, 'w') as f:
        json.dump(final, f, indent=2)

    print(f"━━━ Done: {len(results)} extracted, {len(final)} total in {OUT_FILE} ━━━")

if __name__ == '__main__':
    main()
