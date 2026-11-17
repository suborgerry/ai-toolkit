// Text contrast inside `root` (WCAG AA: 4.5:1, large text 3:1).
// `root`: element passed as a snapshot uid in `args`; defaults to body.
// Canvas parses any CSS color format (rgb, oklch, color()).
// `manual`: text over images, gradients or semi-transparent layers; check from a screenshot.
(root = document.body) => {
  const NORMAL_MIN = 4.5;
  const LARGE_MIN = 3;
  const LARGE_PX = 24;
  const LARGE_BOLD_PX = 18.66;
  const BOLD = 700;
  const OPAQUE = 255;

  const ctx = Object.assign(document.createElement("canvas"), { width: 1, height: 1 }).getContext("2d", { willReadFrequently: true });
  const rgba = c => {
    ctx.clearRect(0, 0, 1, 1);
    ctx.fillStyle = c;
    ctx.fillRect(0, 0, 1, 1);
    return [...ctx.getImageData(0, 0, 1, 1).data];
  };
  const channel = v => (v / 255 <= 0.03928 ? v / 255 / 12.92 : ((v / 255 + 0.055) / 1.055) ** 2.4);
  const lum = ([r, g, b]) => 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b);

  // First opaque background up the tree; null when it can't be computed.
  const bgOf = el => {
    for (; el; el = el.parentElement) {
      const s = getComputedStyle(el);
      if (s.backgroundImage !== "none") {
        return null;
      }

      const c = rgba(s.backgroundColor);
      if (c[3] === OPAQUE) {
        return c;
      }
      if (c[3] > 0) {
        return null;
      }
    }
    return [OPAQUE, OPAQUE, OPAQUE, OPAQUE];
  };

  const out = { fail: [], manual: [] };
  for (const el of root.querySelectorAll("*")) {
    const ownText = [...el.childNodes].some(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim());
    if (!ownText || !el.getClientRects().length) {
      continue;
    }

    const s = getComputedStyle(el);
    if (s.visibility === "hidden" || +s.opacity === 0) {
      continue;
    }

    const label = el.tagName.toLowerCase() + ": " + el.innerText.trim().slice(0, 40);
    const fg = rgba(s.color);
    const bg = bgOf(el);
    if (!bg || fg[3] < OPAQUE) {
      out.manual.push(label);
      continue;
    }

    // Ratio = (lighter + 0.05) / (darker + 0.05), e.g. #777 on white = 4.48 → fail.
    const [hi, lo] = [lum(fg), lum(bg)].sort((a, b) => b - a);
    const ratio = (hi + 0.05) / (lo + 0.05);
    const size = parseFloat(s.fontSize);
    const large = size >= LARGE_PX || (size >= LARGE_BOLD_PX && +s.fontWeight >= BOLD);
    if (ratio >= (large ? LARGE_MIN : NORMAL_MIN)) {
      continue;
    }

    out.fail.push({ label, ratio: +ratio.toFixed(2), color: s.color, background: `rgb(${bg.slice(0, 3)})`, size: s.fontSize });
  }

  for (const k in out) {
    out[k] = out[k].slice(0, 40);
  }
  return out;
}
