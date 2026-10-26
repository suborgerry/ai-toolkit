---
name: figma-pixel-perfect-frontend
description: Use for implementing Figma designs, screenshots, mockups, or visual references as pixel-perfect frontend code with browser screenshot QA. Trigger for Figma-to-HTML, static frontend components, CMS-ready sections, scoped classes, local assets, responsive visual matching, and browser comparison against a design reference. Do not use for backend-only work, ordinary UI bugs without a visual reference, or feature work that does not require pixel-perfect visual fidelity.
---

# Figma Pixel Perfect Frontend

Implement Figma designs, screenshots, mockups, and visual references as production-ready frontend sections, components, page blocks, or CMS-ready HTML layouts inside existing codebases.

This skill is for **design-to-HTML implementation with visual QA**. It may prepare markup for future CMS integration, such as reusable sections or ACF Flexible Content migration, but it must not generate PHP, WordPress templates, ACF fields, or CMS configuration unless the user explicitly asks for that separately.

## Source Of Truth

- The current project is the source of truth for technology, file structure, naming conventions, build process, styling architecture, asset handling, and integration patterns.
- The visual reference is the source of truth for output.
- Adapt design-tool output to the project instead of copying generated code blindly.
- If project-specific rules conflict with this skill, inspect the project first and follow the project when the convention is clearly intentional.
- Preserve user changes and avoid unrelated refactors.

## Required Design Reference

A pixel-perfect task requires at least one clear visual source of truth:

- Figma URL
- Design screenshot
- Mockup image
- Visual reference image
- Exported design frame

If no visual reference is provided, stop before implementation and tell the user that pixel-perfect work requires a Figma design, screenshot, mockup, or other visual reference. Do not attempt pixel-perfect implementation from text alone.

## Use And Avoid

Use this skill for:

- Figma-to-HTML implementation
- Static frontend sections, components, and page blocks
- CMS-ready HTML markup
- Scoped, prefixed component styling
- Local asset implementation
- Browser screenshot comparison and visual QA

Do not use this skill for:

- Tasks without a visual reference
- Ordinary UI bug fixes without a design reference
- Backend-only work
- Feature work where visual fidelity is not required
- Broad redesigns without a visual source of truth
- Review-only tasks unless screenshot comparison or pixel-perfect validation is requested
- WordPress, PHP, ACF field setup, or CMS template implementation unless explicitly requested separately

## Useful Prompt Details

When available, extract or ask for:

- Target scope: section, component, page block, full page, or CMS-ready HTML section
- Target file or component location
- Expected viewport or Figma frame size
- Class prefix or component name
- Output type: static HTML, reusable frontend component, or CMS-ready markup
- Project constraints or naming conventions

Infer optional details from the project when safe. Ask only when missing information blocks correct implementation or creates meaningful rework risk.

## Required Capabilities And Fallbacks

This skill works best with project files, a visual reference, local dev server, browser screenshot tools, and build/lint/typecheck commands.

If Figma access, browser screenshots, or visual diff tools are unavailable, state the limitation clearly and use the best available fallback:

- Exported screenshots
- Manual visual comparison
- Static code review
- Layout measurement from available design data
- Browser preview without automated visual diff

Do not claim pixel-perfect verification unless browser screenshot comparison was actually performed against the visual reference.

## Engineering Judgment

- Choose the simplest implementation that satisfies the design, future CMS needs, and project conventions.
- Do not add features, variants, abstractions, dependencies, or configurability that the design or user did not require.
- Push back briefly if an approach would make the implementation fragile, hard to edit, or inconsistent with the project.
- Keep small isolated components lightweight while still rendering and visually checking the result.
- Stop and name what is unclear instead of guessing when ambiguity blocks correct implementation.
- State important assumptions in the final response.

## Project Discovery

Before implementation, inspect enough of the project to follow its conventions:

- Detect the package manager from lockfiles.
- Read `package.json` scripts for dev, build, lint, and typecheck commands.
- Detect or infer the dev server URL from scripts, config, or common defaults such as Vite `5173`, Next/CRA `3000`, and Vue CLI `8080`.
- Reuse an existing dev server if available; otherwise start it with the project package manager and dev script.
- Detect the styling approach: Tailwind, SCSS/CSS, CSS Modules, CSS-in-JS, component libraries, or design tokens.
- Detect existing fonts, icon libraries, image handling, and assets before adding or importing anything new.

For small isolated components, keep discovery focused on the files, styles, assets, and scripts needed for the requested implementation.

## Core Workflow

1. Confirm that a valid visual reference exists.
2. Inspect the project structure, styles, assets, conventions, and build scripts.
3. Inspect the design reference: dimensions, layout, assets, typography, spacing, breakpoints, and states.
4. Identify the major logical blocks.
5. State a brief implementation plan for multi-block work.
6. Implement one major block or isolated component at a time.
7. Render the implementation in the browser.
8. Capture a local browser screenshot when tooling allows it.
9. Compare the local result against the design reference.
10. Fix the highest-impact visual differences first.
11. Repeat verification until critical and medium visual issues are resolved.
12. Run build, lint, or typecheck commands according to the project.
13. Summarize changed files, verification performed, visual fixes, remaining differences, and build result.

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

- For complex pixel-perfect work, perform at least 3 verification passes.
- For small isolated components, perform at least 1 rendered visual check and additional passes only if critical or medium issues remain.
- Stop only when critical visual issues are resolved, remaining differences are minor or explained, and the implementation follows project conventions.
- Report the number of verification passes completed.

If browser screenshot comparison was not possible, say so clearly and describe the fallback verification method used.

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

## Markup And Styling Rules

- Use scoped, prefixed class names to avoid conflicts with global styles or existing components.
- Avoid generic class names such as `.section`, `.title`, `.list`, `.menu`, `.card`, `.item`, and `.image`.
- Structure markup into clear logical blocks that can later become CMS fields, reusable arrays, repeaters, or component props if needed.
- Keep content and structure separable.
- Reset or isolate styles when global styles affect the component.
- Avoid unrelated global style changes unless global rules directly break the requested design and the project context makes the change appropriate.
- Prefer existing project conventions, but prioritize visual fidelity for the requested component.
- Do not install unnecessary libraries or frameworks.

## CMS-Ready HTML Rules

When building CMS-ready markup:

- Make repeated content boundaries obvious.
- Use consistent wrapper, item, media, content, title, text, actions, caption, and meta structure.
- Keep editable text, images, links, labels, captions, and descriptions easy to identify.
- Avoid requiring future editors to enter HTML for ordinary content.
- Avoid layout logic that depends on a specific number of items unless the design requires it.
- If the design contains different row, card, media, list, or item patterns, structure them as clear markup variants.
- Keep class prefixes specific enough to avoid conflicts with existing site styles.
- Do not generate PHP, ACF fields, WordPress template files, or CMS configuration unless explicitly requested separately.

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

- Store required design assets locally in the project.
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
- Use a local SVG or exported asset when a custom icon is more faithful than an approximation.
- Do not install a new icon library before checking existing project tools and assets.

## Surgical Change Rules

- Touch only files needed for the requested implementation.
- Do not refactor adjacent code, rename unrelated classes, or reformat unrelated files.
- Match the existing project style even when another style would also work.
- Remove only unused imports, variables, assets, or code introduced by the current changes.
- Do not delete pre-existing dead code unless the user asks.
- If unrelated code looks suspicious, mention it in the final response instead of changing it.
- Every changed line should trace back to the requested design, CMS-ready markup needs, visual QA, or build fix.
- When screenshots are captured for QA, store them in a temporary or QA-appropriate location and avoid committing generated QA screenshots unless the project already does so.

## Anti-Patterns

Avoid:

- Starting without a Figma design, screenshot, mockup, or visual reference
- Claiming pixel-perfect accuracy without screenshot-based verification
- Skipping visual comparison after implementation
- Using approximate colors when exact design colors are available
- Replacing unavailable design assets with fake or unrelated placeholders
- Reproducing design export artifacts as production crop hacks
- Hardcoding arbitrary widths or heights to compensate for incorrect parent layout
- Using raw arbitrary Tailwind color utilities for reusable design colors instead of variables or tokens
- Assuming icon colors, line heights, font weights, or spacing from visual memory
- Adding dependencies before checking existing project tools
- Letting global styles silently control the component
- Treating Figma-generated code as production code
- Generating WordPress, PHP, ACF, or CMS implementation when the task only asks for design-to-HTML

## Quality Gates

Complete the task only when:

- A valid visual reference was used.
- The component or section is implemented in the correct project files.
- Required assets are local or missing assets are clearly reported.
- Markup and styles use scoped, prefixed names.
- Major blocks or isolated components were visually checked against the design reference.
- Critical visual issues are resolved.
- Responsive behavior has been checked where relevant.
- Accessibility basics are implemented, not only mentioned.
- Build, lint, or typecheck passes according to the project when available.
- Remaining differences are minor and explained.

## Final Response

Include:

- Files changed
- Design reference used
- Verification method and number of passes
- Key visual fixes
- Responsive checks performed
- Build, lint, or typecheck result
- Remaining limitations or differences

Do not overclaim. Do not say the result is pixel-perfect unless browser screenshot comparison was performed against the design reference. If verification was partial, state exactly what was and was not verified.
