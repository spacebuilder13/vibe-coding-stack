## Competitive Research Skill Extension Notes

This extension adds a **ZEN design-system audit layer** to the existing crawl + IA + UX evidence flow.

### What was added

- A new audit output contract for ZEN-specific documentation:
  - `ZEN-DESIGN-PRINCIPLES-RUBRIC.md`
  - `ZEN-AUDIT-SCORECARD.md`
  - `ZEN-AUDIT-FINDINGS.md`
- A consistent pass model (`PASS`, `PARTIAL`, `FAIL`) and confidence tags.

### Why this extension exists

The original skill captures content and IA well, but it does not force a principle-based design critique.  
This extension makes the audit explicit, repeatable, and traceable to page evidence.

### Runtime hardening included in this run

The crawler was also hardened to improve execution reliability on modern websites:

1. **Malformed sitemap tolerance**
   - strict XML parse
   - recover-mode parse (`lxml`)
   - regex fallback for `<loc>` extraction
2. **Canonical domain handling (`www` vs apex)**
   - URL admission now matches same site even when `www.` differs

These are reliability improvements; they do not change the audit semantics.
