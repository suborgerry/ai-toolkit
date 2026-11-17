// The focused element after a Tab press. outline and boxShadow both false: confirm focus visibility from a screenshot.
() => {
  const el = document.activeElement;
  if (!el || el === document.body) {
    return null;
  }

  const s = getComputedStyle(el);
  const r = el.getBoundingClientRect();
  return {
    el: el.tagName.toLowerCase() + (el.id ? "#" + el.id : ""),
    text: (el.innerText || el.getAttribute("aria-label") || "").trim().slice(0, 40),
    outline: s.outlineStyle !== "none" && parseFloat(s.outlineWidth) > 0,
    boxShadow: s.boxShadow !== "none",
    inView: r.width > 0 && r.bottom > 0 && r.top < innerHeight,
    expanded: el.getAttribute("aria-expanded"),
  };
}
