# Figma fidelity: extraction, verification, styling, assets

## Design Data Extraction

Before writing styles for an element, extract or verify:

- Text: font family, font size, font weight, line height, letter spacing, color, opacity, alignment, transform, decoration, and wrapping
- Containers: width, intentional height, padding, margin, gap, background, border, radius, shadow, opacity, and overflow
- Images: rendered dimensions, natural aspect ratio, object fit, radius, border, and alignment
- Icons: width, height, stroke, fill, stroke width, color, and alignment
- Layout: parent-child relationships, section boundaries, shared backgrounds, dividers, edge-to-edge areas, and inset areas
- States: hover, focus, active, open, closed, loading, disabled, and selected where visible in the reference

Do not assume inheritance or browser defaults when the design provides explicit values.

## Visual Verification

For multi-block designs, do not continue to the next major block until the current block has been implemented, rendered, compared against the reference, and adjusted for critical visual differences.

Check:

- Layout structure, container width, intentional heights, spacing, padding, margin, and gaps
- Typography, line height, font weight, wrapping, and alignment
- Colors, opacity, borders, radii, shadows, and backgrounds
- Image placement, aspect ratio, cropping, and object fit
- Icons, decorative elements, dividers, clipping, and overflow
- Responsive behavior and content order
- Semantic markup, content hierarchy, and CMS-ready separation where relevant
- Global-style leakage, layout shifts, unnecessary dependencies, build errors, and unrelated file changes

Use measurement where practical instead of visual intuition only.

### Visual Fix Priority

Fix issues in this order:

1. Layout structure and section dimensions
2. Spacing, alignment, and container width
3. Typography and text wrapping
4. Images, icons, and decorative elements
5. Colors, borders, shadows, and small details
6. Micro-interactions and hover/focus states

### Verification Passes

- Repeat render → compare → fix until no critical or medium differences remain at the checked widths.
- After 5 passes on one section with critical or medium differences left, stop and report them instead of continuing.
- Report the number of verification passes completed.

If browser screenshot comparison was not possible, say so clearly and describe the fallback verification method used.

Store QA screenshots in a temporary location; do not commit them unless the project already does.

## Responsive Verification

Check the design-provided breakpoints first. If breakpoints are not provided, verify common widths such as:

- `1440px` desktop
- `1024px` tablet
- `768px` tablet/mobile boundary
- `375px` mobile

Do not invent complex responsive behavior unless the design or project conventions imply it. When a mobile design is missing, preserve hierarchy, spacing rhythm, readability, content order, and accessible interaction. State responsive assumptions in the final response.

## Design System Sync

Use the existing design system when it exists:

- Map design values to existing tokens before creating new values.
- If SCSS/CSS is used, prefer scoped component variables or existing CSS custom properties.
- If CSS-in-JS or a component library is used, map design values to the existing theme first.
- If no token system exists, exact design values may be used locally inside scoped component styles.
- Do not install new styling or component libraries unless the user asks or the project clearly requires it.

## Tailwind Projects

When Tailwind is used:

- Prefer Tailwind CSS v4+ architecture through CSS-first configuration and CSS variables, not legacy JavaScript config, unless the existing project is already intentionally using the older setup.
- Prefer existing utilities, theme tokens, CSS custom properties, and project-defined variables.
- Do not write raw color utilities like `bg-[#fff]`, `text-[#111]`, or `border-[#ddd]` for reusable design values. Move colors and repeated design values into the project style layer as variables or tokens, then reference them through semantic utilities or project conventions.
- Use arbitrary values only for one-off measurements that are required for design fidelity and do not belong in the design token layer.
- Avoid dynamic class names that may not be detected by the build process.
- Keep long utility groups readable and consistent with the project style.
- Do not create custom CSS for values already covered by project utilities.

## Fonts

- Check existing project fonts, font loading, and design tokens before adding or importing fonts.
- Do not import external fonts without permission unless the project already uses that source.
- If the exact design font is unavailable, use the closest project-approved font and report the substitution.
- Match font family, size, weight, line height, letter spacing, alignment, and text wrapping.
- Remember that design-tool text boxes may not match natural browser text height.

## Layout Ownership Checks

During visual comparison, verify:

- Whether padding belongs to the parent section, inner container, card, list, or child element
- Whether backgrounds extend edge-to-edge or only wrap content
- Whether borders and dividers span the full parent width or only the content width
- Whether visible gaps reveal the wrong parent background
- Whether decorative elements are positioned against the viewport, outer wrapper, content container, or a specific block

## Accessibility Rules

Accessibility is part of implementation, not only a final quality check.

- Use semantic HTML before ARIA.
- Use real links for navigation and real buttons for actions.
- Do not use clickable `div` or `span` elements for interactive controls.
- Add meaningful `alt` text for content images and empty `alt=""` for decorative images.
- Preserve visible focus states for interactive elements.
- Ensure keyboard access for menus, accordions, tabs, modals, sliders, and other interactive UI.
- Keep heading order logical.
- Ensure form controls have labels where relevant.
- Avoid hiding meaningful content from assistive technologies.
- Match the visual design without breaking accessibility.

## Asset, Image, And Icon Rules

- Route assets as described in `SKILL.md` → "Assets": inline SVG, theme asset, or media library.
- Do not rely on temporary Figma, MCP, or external asset URLs.
- Do not replace missing design images with unrelated placeholders unless the user explicitly allows placeholders.
- If an asset is unavailable, create the correct layout slot and clearly report the missing asset.
- Do not copy design export artifacts, grouped sprite offsets, mask hacks, or arbitrary export bounds into production code.
- Use final prepared or exported assets in the exact visual format needed by the design.
- Render images normally and preserve natural aspect ratio unless the design intentionally defines a fixed frame.
- Avoid hardcoded image dimensions when correct typography, spacing, parent width, and natural image ratio would produce the intended layout.
- Use fixed dimensions only for intentional frames, controls, icons, image slots, or measurable component boundaries.
- Position decorative elements relative to the correct parent and verify their placement at screenshot edges.
- Allow decorative elements to overflow only from the intended wrapper and clip only at the intended boundary.
- Use the project existing icon library when available.
- Match icon size, stroke width, fill, stroke color, and alignment to the design.
- Use an inline SVG from Figma when a custom icon is more faithful than an approximation.
- Do not install a new icon library before checking existing project tools and assets.
