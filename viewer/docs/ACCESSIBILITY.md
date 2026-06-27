# Accessibility — validation & release gate

The viewer is built for accessibility (a `/explorer/text` screen-reader shadow
site, CVD-safe partisan palette, focus management, reduced-motion, RTL). This
file records how that is *validated* and what still requires a human pass.

## Automated gate (axe-core via Playwright)

`viewer/tests/a11y/smoke.spec.ts` runs axe-core in Firefox against the
production build (`vite preview`) and **fails on any serious or critical**
WCAG 2.0/2.1 A/AA violation. Routes covered:

- `/` — the report (also re-run in Arabic to exercise the `dir="rtl"` path)
- `/explorer` — the deck.gl map
- `/explorer/text` — the screen-reader text shadow site

Run it:

```bash
cd viewer
npm run build       # the suite tests the built site via vite preview
npm run test:a11y
```

Moderate/minor axe findings are printed but do not fail the run, to keep the
gate stable. As of the last run all four routes report **0 serious/critical**
violations (contrast fixes landed for the scroll-spy nav label, the
preliminary badge, the back-to-stakes links, and links inside dark table
headers).

This is a smoke test, not a proof of accessibility — axe catches roughly a
third of WCAG issues. It is a regression floor, not a ceiling.

## Manual gate (human sign-off — REQUIRED before release)

Automated tooling cannot confirm the experience for an assistive-technology
user. Before a release that touches markup, navigation, the map, or the text
shadow site, complete a manual pass and record it here:

- [ ] **Screen reader** — NVDA (Firefox) or VoiceOver (Safari): read `/`,
      `/explorer`, and `/explorer/text` end to end. Headings, landmarks, the
      map's text alternative, and the language switcher must be announced
      coherently.
- [ ] **Keyboard only** — tab through `/` and `/explorer`: every control
      reachable, visible focus ring, logical order, no traps; the scroll-spy
      and the map's controls operable without a mouse.
- [ ] **RTL** — spot-check Arabic/Urdu for mirrored layout and correct focus
      order.

Record the date, tool, and findings of each pass below.

### Pass log

_(none yet — the screen-reader pass remains the outstanding release gate)_
