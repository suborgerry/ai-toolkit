// Stylesheets with top-level prefers-reduced-motion rules. Cross-origin sheets can't be read: listed as unreadable.
() => {
  const sheets = [];
  const unreadable = [];
  for (const sh of document.styleSheets) {
    try {
      if ([...sh.cssRules].some(r => r.conditionText?.includes("prefers-reduced-motion"))) {
        sheets.push(sh.href || "inline");
      }
    } catch {
      unreadable.push(sh.href);
    }
  }
  return { sheets: [...new Set(sheets)], unreadable };
}
