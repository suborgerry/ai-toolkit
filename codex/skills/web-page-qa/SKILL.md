---
name: web-page-qa
description: "QA a developed web page against its approved Figma/design on desktop and mobile using chrome-devtools-mcp: design match, responsive, links, forms, console; write bug reports, retest fixes."
---

# Web Page QA (Web Department Quality Control Checklist)

**Goal:** confirm the developed page matches the approved design on desktop and mobile and has no visible or functional errors before approval. Claude acts as the QA reviewer and produces findings. Claude never approves a page: final approval belongs to the Web Department Director or project lead.

Write the report in the language the user writes in, unless they ask otherwise.

## Scope

- **In scope:** design comparison, responsive behavior, visual errors, broken links, component functionality, forms, glaring typos, retesting fixes.
- **Out of scope (do not do, even if noticed):** SEO, evaluating or rewriting messaging, content strategy, translation quality, redesigning the approved layout, making development/code changes. Lighthouse and performance traces are not part of this checklist: run them only if the user asks.
- **Copy:** check that displayed text matches the approved design or supplied copy and flag glaring typos or obvious copy errors only. Never judge or rewrite the message.

## Step 1. Request the design and other sources of truth

Before any testing, ask for everything missing in **one plain-text message**.

**Page**
- Exact page URL; production or staging; the correct production domain.
- How to reach it if protected (staging login, basic auth). Prefer connecting chrome-devtools-mcp to the user's already logged-in Chrome (`--autoConnect`) over having passwords pasted into the chat.

**Figma (main source of truth for everything visual)**
- Figma file link plus direct links to the approved frames: desktop, mobile, and tablet if it exists (frame link with `node-id`, via right-click on the frame > Copy link).
- Which page/version of the file is final (not WIP, archive or old variants).
- Where interaction states live, if anywhere: prototype, components page, or state frames (hover, open menu, active tab, form errors, success message).
- If Figma MCP is not connected or the file is not accessible: ask for PNG exports of the frames and their export scale (1x/2x).

**Other sources of truth (ask which exist)**
- Approved copy (doc/sheet): the source for text if supplied.
- Link map: where each button, CTA and menu item should lead; correct phone numbers, emails, booking or external URLs.
- Form spec: fields, required fields, validation messages, success message or redirect, where submissions go; test data; permission to submit a valid form (a real submission can create a lead, email or CRM entry).
- Brand guide / design system: fonts, colors, spacing for things the frames don't show.
- Approved assets (photos, logos, icons) if they are not in Figma.
- Approved differences from the design: a list, or the tickets/comments where they were agreed. These are never reported as bugs.
- Languages on the site and how switching works.
- Cookie/consent banner: which tool, and whether it is in the design.
- Browsers required beyond latest Chrome.
- Previous bug list, if this is a retest.

**Precedence when sources disagree**
1. Explicitly approved differences.
2. Supplied approved copy (text only).
3. Approved Figma frames.
4. Design system / brand guide (only for what the frames don't show).

If two sources contradict each other, do not pick one: list it under **Source conflicts** in the report as a question for the user, not as a bug.

**If something is missing**
- No design at all: run only the functional checks and the report; state that design match was not checked.
- Desktop design only: check mobile against general responsive rules (sections B, C) and mark mobile design match as not verified.

## Step 2. Browser: chrome-devtools-mcp

All live-page testing goes through the **chrome-devtools-mcp** server (Google's official Chrome DevTools MCP). Below, its tools are named without any client prefix.

**Check availability first.** If no chrome-devtools tools are in the session, stop and tell the user. Do not silently switch to another browser tool. Suggested setup in `~/.codex/config.toml`:

```toml
[mcp_servers.chrome-devtools]
command = "npx"
args = ["-y", "chrome-devtools-mcp@latest", "--isolated"]
```

- `--isolated`: temporary clean profile (no cache, no cookies, logged out). Default choice for QA.
- `--autoConnect` (Chrome 144+, remote debugging enabled at `chrome://inspect/#remote-debugging`): attach to the user's running Chrome, e.g. for staging behind a login or basic auth.
- `--headless`: no visible window. `--viewport 1920x1080`: initial size.

Tool names and parameters change between versions: go by the tool schemas actually present in the session. Most tools need `pageId` (from `new_page` / `list_pages`).

### Tool map

| Task | Tool |
|---|---|
| Open page in a fresh tab | `new_page` (`url`; `isolatedContext` for a separate cookie/storage context = logged-out, first-visit view) |
| Hard refresh | `navigate_page` with `type: "reload"`, `ignoreCache: true` |
| Exact viewport / device | `emulate` with `viewport: "<w>x<h>x<dpr>[,mobile][,touch][,landscape]"`; `userAgent` if needed |
| Plain resize | `resize_page` (`width`, `height`) |
| Element uids for interaction | `take_snapshot` (re-take after every navigation or big DOM change: uids go stale) |
| Click / hover / keyboard | `click`, `hover`, `press_key` (`Tab`, `Enter`, `Escape`), `type_text` |
| Forms | `fill_form` (several fields at once), `fill`, `upload_file`; `wait_for` (`text: [...]`) for the success message |
| Alerts/confirms | `handle_dialog` |
| Screenshots | `take_screenshot` (`fullPage: true` for whole page; `uid` for one element; `filePath` to save evidence) |
| DOM checks, page prep, link check, overflow | `evaluate_script` (`function: "async () => {...}"`) |
| Computed styles vs Figma | `get_css_styles` if present, otherwise `evaluate_script` with `getComputedStyle` |
| Console errors | `list_console_messages` (filter `types` to errors/warnings), `get_console_message` for details |
| Failed requests (404/500 assets, form submit) | `list_network_requests` (`resourceTypes`), `get_network_request` (`reqid`) |

### Setup routine
1. `new_page` with the page URL (use `isolatedContext` unless the user wants the logged-in state).
2. `navigate_page` reload with `ignoreCache: true`.
3. If a WordPress admin bar or Shopify preview bar is visible, the session is logged in: it shifts the layout and hides public-state bugs. Switch to an isolated context.

### Viewports
Compare at the same width as the design frame. Standard sweep with `emulate`:
- Desktop: `1920x1080x1`, `1440x900x1`, `1280x800x1`, `1024x768x1`
- Tablet: `768x1024x2,mobile,touch`
- Mobile: `390x844x3,mobile,touch`, `375x667x2,mobile,touch`, `320x568x2,mobile,touch`

Rules:
- After changing to or from a mobile viewport, reload the page: some scripts and sliders initialise only on load.
- `mobile` flag does not change the user agent. If the theme or a plugin detects mobile server-side (e.g. WordPress `wp_is_mobile()`), also set a mobile `userAgent` and reload.
- When going back to desktop, set a desktop viewport string explicitly (without `mobile`/`touch`).
- Between-breakpoint sweep (item 17): step through widths from 320 to 1920 (denser around the site's breakpoints), run the overflow script at each, and take screenshots only where something breaks.

## Step 3. Prepare the page before every comparison screenshot

Entrance animations (Elementor motion effects, AOS, WOW.js) and lazy-loaded images do not appear until scrolled into view. Without this step, screenshots show empty or half-faded sections and produce false bugs. Run it after every viewport change and reload.

1. **Scroll through and wait** with this script, then check the result:
```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  await document.fonts.ready;
  const step = Math.round(innerHeight * 0.8);
  for (let y = 0, n = 0; y < document.documentElement.scrollHeight && n < 200; y += step, n++) { scrollTo(0, y); await sleep(300); }
  await sleep(500);
  const imgs = [...document.images];
  await Promise.all(imgs.filter(i => !i.complete).map(i => new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 5000); })));
  scrollTo(0, 0); await sleep(300);
  return {
    pageHeight: document.documentElement.scrollHeight,
    brokenImages: imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.currentSrc || i.src),
    stillHidden: document.querySelectorAll('.elementor-invisible, [data-aos]:not(.aos-animate)').length
  };
}
```
   - `brokenImages`: candidates for item 18 (confirm in `list_network_requests`).
   - `stillHidden > 0`: scroll those elements into view again; if they stay invisible, report it (content never appears).
2. **Freeze motion** so screenshots are stable:
```js
() => { const s = document.createElement('style'); s.id = 'qa-freeze';
  s.textContent = '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition:none!important;caret-color:transparent!important}';
  document.head.appendChild(s); return true; }
```
   Compare an autoplay slider at its first slide unless the design shows another one.
3. **Fixed and sticky elements:** a full-page screenshot repeats or overlays fixed headers, chat widgets and banners. Use section captures (Step 4) and offset each scroll by the sticky header height so it doesn't cover the section's top. Item 27 is still checked on the normal, unmodified page.
4. **Translated versions:** client-side translation widgets (e.g. GTranslate's free mode) replace text after load. Wait (`wait_for` a known translated word) before preparing and capturing.
5. **Reload before functional and interaction tests.** The freeze style and scrolling change page state.

## Step 4. Compare with the design section by section

Comparing a whole long page in one image is imprecise. Work one section at a time, at the same width as the frame.

1. **Figma sections:** `get_metadata` on the approved frame gives its top-level children (name, node id, position, height).
2. **Live sections:** after Step 3, map the page:
```js
() => {
  const q = s => [...document.querySelectorAll(s)];
  let secs = q('.shopify-section');
  if (!secs.length) secs = q('.elementor-top-section, .e-con.e-parent');
  if (!secs.length) secs = q('main section, main > *');
  secs = [...new Set([...q('body header'), ...secs, ...q('body footer')])];
  secs = secs.filter(el => !secs.some(o => o !== el && o.contains(el)));
  return secs.map(el => { const r = el.getBoundingClientRect(); return {
      tag: el.tagName.toLowerCase(), id: el.id, cls: String(el.className).slice(0, 80),
      top: Math.round(r.top + scrollY), height: Math.round(r.height),
      heading: (el.querySelector('h1,h2,h3')?.innerText || '').trim().slice(0, 60) }; })
    .filter(s => s.height > 20).sort((a, b) => a.top - b.top);
}
```
   Selectors cover Shopify sections, Elementor sections/containers and generic `main` children; adjust them for other builders.
3. **Match** live sections to Figma sections by order and heading text. A missing, extra or reordered section is a finding for item 1.
4. **Capture each pair:**
   - Figma: `get_screenshot` of that section's node.
   - Live: scroll the section into view (`el.scrollIntoView()` then `scrollBy(0, -stickyHeaderHeight)`) and take a viewport `take_screenshot` if the section fits the viewport. For a taller section use its `uid` from `take_snapshot` if it is exposed; otherwise take a `fullPage` screenshot and crop it by the section's `top`/`height` multiplied by `devicePixelRatio` with an available image tool (e.g. Python Pillow).
5. **Compare one pair at a time** against checklist items 2-8 and record differences under the section's name. Where something looks off, measure it with the computed-style script instead of guessing:
```js
(sel) => { const el = document.querySelector(sel); if (!el) return null; const s = getComputedStyle(el);
  return { font: s.fontFamily, size: s.fontSize, weight: s.fontWeight, lineHeight: s.lineHeight, color: s.color, letterSpacing: s.letterSpacing, textTransform: s.textTransform, margin: s.margin, padding: s.padding, width: el.getBoundingClientRect().width }; }
```
   Pass the selector in `args`; compare against `get_variable_defs` / `get_metadata` values from Figma.
6. Repeat for the tablet and mobile frames.

## Step 5. Checklist

### A. Match the developed page to the design
Compare section by section (Step 4), header to footer.
1. All sections present and in the correct order.
2. Text, images, icons, logos, buttons and other assets match.
3. Fonts, sizes, weights, line heights, colors and capitalization match.
4. Spacing, alignment, widths, heights, padding, margins and column gaps match.
5. Borders, shadows, backgrounds, gradients, corner radii and dividers match.
6. Image crops, focal points, aspect ratios and quality match.
7. Header, navigation, footer, cards, forms, sliders and other components match.
8. Hover, active, open, selected and disabled states match when shown in the design (`hover` / `click` on the uid, then element `take_screenshot`).

### B. Desktop, mobile and responsive
9. Desktop layout matches the approved desktop design.
10. Mobile layout matches the approved mobile design.
11. Content stacks in the correct order on mobile (and tablet).
12. Navigation switches correctly between desktop and mobile (open/close the burger menu, submenus).
13. Text, buttons, images, forms, tables and embeds fit without clipping or overlap.
14. No unwanted horizontal scrolling at any tested width (overflow script below).
15. Buttons and links stay readable, visible and easy to tap.
16. Images and videos scale without stretching, pixelation or bad cropping.
17. Sweep ~320 px to 1920 px and check for errors between standard breakpoints.

**Horizontal overflow script (item 14):**
```js
() => {
  const w = document.documentElement.clientWidth;
  const offenders = [...document.querySelectorAll('body *')]
    .filter(el => { const r = el.getBoundingClientRect(); return r.width && r.right > w + 1; })
    .slice(0, 20)
    .map(el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
      (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).join('.') : ''));
  return { viewport: w, scrollWidth: document.documentElement.scrollWidth, hasOverflow: document.documentElement.scrollWidth > w, offenders };
}
```

### C. Errors and functionality
18. Page loads without broken images, missing icons, unstyled sections or visible error messages (`list_network_requests` for failed images/fonts/CSS/JS).
19. Header navigation, mobile menu, dropdowns and footer links work.
20. Buttons, linked cards, phone/email links, anchors, downloads and external links go to the correct destination (compare with the link map if supplied).
21. Link check: no internal or external URL returns 404, another error page, or an unexpected destination.
22. No link points to `#`, a demo/template site, localhost, or the wrong staging domain.
23. Accordions, tabs, sliders, popups, filters, video, maps and other interactive components work (`click` + screenshot of the result).
24. Every clickable/interactive element works; nothing is inactive or broken.
25. Forms display correctly, required fields validate, errors are clear, and a valid submission gives the expected success result (compare with the form spec). Submit only with the user's permission: `fill_form` with the agreed test data, `click` submit, `wait_for` the success text, and confirm the submit request status in `list_network_requests`. Without permission, test validation only (submit empty / invalid) and mark the valid submission Needs Manual Verification.
26. No glaring typos, duplicated/missing words or obvious punctuation errors (`take_snapshot` gives the page text).
27. Sticky headers, buttons, cookie notices and chat widgets do not cover important content (check at mobile widths too, after scrolling).
28. Primary interactions work with mouse, touch and keyboard: keyboard via `press_key` (`Tab`, `Enter`, `Escape`) with visible focus; touch via `emulate` with `touch` flag (emulated only: real-device touch is Needs Manual Verification).
29. `list_console_messages`: no page-breaking errors; point any to the developer with the message text and source.
30. Tested in Chrome via chrome-devtools-mcp (it drives Chrome only). Other required browsers are Needs Manual Verification.

**Link check script (items 20-22):**
```js
async () => {
  const origin = location.origin;
  const unsafe = /add-to-cart|logout|log-out|action=|delete|remove|unsubscribe|wp-admin/i; // never GET these
  const links = [...document.querySelectorAll('a[href], area[href]')].map(a => ({
    text: (a.innerText || a.getAttribute('aria-label') || a.title || '').trim().slice(0, 60),
    href: a.getAttribute('href').trim(), abs: a.href,
    visible: !!a.getClientRects().length
  }));
  const issue = l => {
    if (!l.href || l.href === '#') return 'empty-or-hash';
    if (/^javascript:/i.test(l.href)) return 'javascript-href';
    if (l.href.startsWith('#') && !document.getElementById(decodeURIComponent(l.href.slice(1)))) return 'missing-anchor-target';
    if (/\/\/(localhost|127\.0\.0\.1)/i.test(l.abs)) return 'localhost';
    return null;
  };
  const internal = [...new Set(links.filter(l => l.abs.startsWith(origin) && !unsafe.test(l.abs)).map(l => l.abs.split('#')[0]))];
  const internalStatus = [];
  for (const url of internal) {
    try { const r = await fetch(url, { redirect: 'follow', credentials: 'omit' }); internalStatus.push({ url, status: r.status, finalUrl: r.url }); }
    catch (e) { internalStatus.push({ url, error: String(e) }); }
  }
  return {
    total: links.length,
    flagged: links.filter(issue).map(l => ({ ...l, issue: issue(l) })),
    skippedUnsafe: links.filter(l => unsafe.test(l.abs)).map(l => l.abs),
    telMailto: links.filter(l => /^(tel|mailto):/i.test(l.abs)).map(l => ({ text: l.text, href: l.abs })),
    external: [...new Set(links.filter(l => /^https?:/i.test(l.abs) && !l.abs.startsWith(origin)).map(l => l.abs))],
    internalStatus
  };
}
```
Then:
- Report every internal URL with status >= 400, an error page, or an unexpected `finalUrl`.
- Review `external` for demo/template sites, staging domains and any domain that should be the production domain.
- Cross-origin `fetch` cannot read status. Check each external link by opening it with `new_page` and reading the document status in `list_network_requests` (`resourceTypes: ["document"]`); close the page afterwards. Any external link not opened is listed as untested.
- Check that `tel:` / `mailto:` values match the design, supplied copy or link map.

### D. Cookie / consent banner (added; not in the original checklist; skip if the site has none)
Consent is stored in cookies/localStorage, so use a new `isolatedContext` for each state.
- **D1. First visit:** the banner appears; at desktop and mobile it does not block navigation or primary CTAs; its buttons (accept, decline, settings) and privacy-policy link work; no glaring typos; it matches the design if the design includes it.
- **D2. After accept:** the banner closes, stays closed after reload, and leaves no empty space or layout jump; embeds that wait for consent (maps, video, chat) load.
- **D3. After decline** (if offered): the banner closes; consent-gated embeds show their placeholder instead of breaking the layout.
- Design-comparison screenshots are taken in the accepted state unless the design shows the banner.

### E. Multilingual (added; not in the original checklist; only if the site has more than one language)
There is usually no Figma per language: compare each language's layout with the main design and report breakage only. Translation quality is out of scope.
- **E1.** The language switcher is visible and usable on desktop and mobile (including inside the mobile menu); the current language is indicated.
- **E2.** Switching keeps the user on the same page in the target language, not the homepage (unless the project says otherwise).
- **E3.** In each language, at desktop and at least 375 and 320 px: no clipping, overlap or overflow from longer strings in buttons, menu, headings and forms (run the overflow script per language).
- **E4.** No visibly untranslated fragments in a translated version, and no broken characters or encoding.
- **E5.** Internal links and forms in a translated version stay in that language (with URL-based languages the subdirectory/subdomain is kept); form validation and success messages appear in that language if they are supposed to.

## Step 6. Findings discipline

- Label every finding:
  - **Confirmed**: reproduced on the live page with a chrome-devtools tool.
  - **Likely**: visible in a screenshot/design comparison but not reproduced interactively.
  - **Needs Manual Verification**: could not be tested here (real device, real touch, other browsers, form submission not permitted).
- Never claim a link, form or interaction was tested unless a tool call actually tested it. State which URLs were actually checked.
- Do not report approved differences.
- Source contradictions go under Source conflicts, not into bugs.

## Step 7. Bug report

One issue per bug:
- **Title** (short) and **exact page URL**
- **Environment:** viewport string used in `emulate`, desktop/mobile, Chrome version/channel, device emulated, language, consent state (if relevant)
- **Steps to reproduce**
- **Actual result** and **expected result** (based on the approved design or other source of truth, named)
- **Evidence:** screenshot saved with `take_screenshot` `filePath` (name it `<issue-number>_<viewport>.png`), the matching Figma frame/node link, and console/network details when relevant
- **Severity:** Critical / High / Medium / Low
- **Status label:** Confirmed / Likely / Needs Manual Verification
- **Recommended correction:** what should change to match the design (describe the expected outcome; do not write or apply code)

Severity guide (suggested; follow the project's own scale if given):
- **Critical:** page or primary flow broken (page doesn't load, form can't be submitted, navigation unusable).
- **High:** key CTA/link broken or 404, major layout mismatch, content hidden or overlapped.
- **Medium:** noticeable visual or responsive deviation, secondary component not working.
- **Low:** minor spacing/pixel deviation, small typo.

## Step 8. Summary and approval readiness

End with:
1. **Coverage:** sources of truth used, viewports emulated, Chrome version, languages and consent states tested, which URLs were checked, and what was not tested.
2. **Source conflicts** (if any), as questions for the user.
3. **Issue count by severity**, then the issue list ordered by severity.
4. **Final approval checklist**, each marked pass / fail / not verified:
   - Page matches the approved desktop and mobile design.
   - No known visual, responsive, link, form, navigation or interaction errors remain.
   - Every clickable element works; no URL returns 404, another error page or an unintended destination.
   - No glaring typos or obvious copy errors remain.
   - All reported fixes were retested.
   - Any remaining difference is documented and approved.
5. **Verdict:** "Not ready for approval" if any item fails; otherwise "Ready for approval by the Web Department Director / project lead". Approval rule: the page is not approved while it differs from the design or a known error is unresolved, unless the Director or project lead has explicitly accepted that difference or issue.

## Retest mode

When the user supplies a previous bug list: reload with `ignoreCache: true`, run Step 3, retest each original issue at its original `emulate` viewport (and language/consent state) plus related screen sizes, mark each Fixed / Not fixed / Regressed, add any new issues found nearby, and update the final approval checklist.