# KOT Content Templates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reskin all Remotion carousel slides and short-form scenes with the KOT brand design system, and add two new short-form content types (Myth-busting, Quick math).

**Architecture:** Update the shared design tokens first (colors, fonts, spacing), then update primitives (LogoMark, Rule, SlideFrame), then update each carousel slide and short-form scene to use new tokens. Add palette system (dark/light) as a prop. Register new compositions in Root.tsx.

**Tech Stack:** React, Remotion, TypeScript, @remotion/google-fonts

**Specs:**
- Brand tokens: `docs/brand/brand-tokens.md`
- Content templates: `docs/brand/content-templates.md`
- Design spec: `docs/superpowers/specs/2026-04-24-content-templates-design.md`

---

## File Map

| Action | File | Responsibility |
|---|---|---|
| Modify | `remotion/src/carousel/tokens.ts` | KOT colors, fonts, type scale, palette system |
| Modify | `remotion/src/carousel/fonts.ts` | Load IBM Plex Mono, drop Instrument Serif + JetBrains Mono |
| Modify | `remotion/src/carousel/types.ts` | Add `palette` prop to CarouselProps, add short-form types |
| Modify | `remotion/src/carousel/primitives/LogoMark.tsx` | Boxed monospace F mark |
| Modify | `remotion/src/carousel/primitives/Rule.tsx` | Dashed dividers (light + heavy) |
| Modify | `remotion/src/carousel/primitives/SlideFrame.tsx` | Palette-aware bg/fg defaults |
| Modify | `remotion/src/carousel/primitives/Header.tsx` | Use updated tokens |
| Modify | `remotion/src/carousel/primitives/SlideCount.tsx` | Use updated tokens |
| Modify | `remotion/src/carousel/primitives/SwipeCue.tsx` | Use updated tokens |
| Modify | `remotion/src/carousel/slides/AccentText.tsx` | Highlight stamp instead of italic+color |
| Modify | `remotion/src/carousel/slides/Cover.tsx` | KOT layout with stamp accent, receipt framing |
| Modify | `remotion/src/carousel/slides/QuoteRule.tsx` | Dashed rule framing, drop serif |
| Modify | `remotion/src/carousel/slides/Math.tsx` | Receipt line-item layout |
| Modify | `remotion/src/carousel/slides/List.tsx` | Mono counters, dashed dividers |
| Modify | `remotion/src/carousel/slides/Pullquote.tsx` | Drop decorative quote mark, add signal colors |
| Modify | `remotion/src/carousel/slides/CTA.tsx` | Always dark, receipt footer, pill |
| Modify | `remotion/src/carousel/Carousel.tsx` | Pass palette to slides |
| Modify | `remotion/src/scenes/Hook.tsx` | KOT receipt-framed hook |
| Modify | `remotion/src/scenes/Problem.tsx` | Stamp label + dashed divider |
| Modify | `remotion/src/scenes/Tip.tsx` | Receipt line-items with KOT tokens |
| Modify | `remotion/src/scenes/CTA.tsx` | Shared CTA with logo, pill, receipt footer |
| Create | `remotion/src/scenes/Myth.tsx` | Myth scene (stamp + italic quote) |
| Create | `remotion/src/scenes/Reality.tsx` | Reality scene (stamp + hero number) |
| Create | `remotion/src/scenes/Proof.tsx` | Comparison receipt blocks |
| Create | `remotion/src/scenes/Setup.tsx` | Question + "$?" |
| Create | `remotion/src/scenes/Calculation.tsx` | Ingredient receipt + result |
| Create | `remotion/src/MythBusting.tsx` | Myth-busting composition (4 scenes) |
| Create | `remotion/src/QuickMath.tsx` | Quick math composition (3 scenes) |
| Modify | `remotion/src/FoodCostTip.tsx` | Add palette prop, use KOT tokens |
| Modify | `remotion/src/Root.tsx` | Register MythBusting + QuickMath, update defaults |

---

### Task 1: Update fonts

**Files:**
- Modify: `remotion/src/carousel/fonts.ts`

- [ ] **Step 1: Replace font loading with IBM Plex Mono + Inter**

```typescript
import { loadFont as loadIBMPlexMono } from '@remotion/google-fonts/IBMPlexMono';
import { loadFont as loadInter } from '@remotion/google-fonts/Inter';

loadIBMPlexMono('normal', {
  weights: ['400', '500', '700'],
  subsets: ['latin'],
});

loadInter('normal', {
  weights: ['400', '600', '700', '800'],
  subsets: ['latin'],
});
```

- [ ] **Step 2: Install IBM Plex Mono font package if needed**

Run: `cd remotion && npm ls @remotion/google-fonts`

The `@remotion/google-fonts` package is already installed at 4.0.448. IBM Plex Mono and Inter are both available in this package — no additional install needed.

- [ ] **Step 3: Commit**

```bash
git add remotion/src/carousel/fonts.ts
git commit -m "feat: switch fonts to IBM Plex Mono + Inter for KOT brand"
```

---

### Task 2: Update design tokens

**Files:**
- Modify: `remotion/src/carousel/tokens.ts`

- [ ] **Step 1: Replace tokens.ts with KOT palette system**

```typescript
/* ── Palette ─────────────────────────────────────────── */

export type Palette = 'light' | 'dark';

const light = {
  bg: '#F8F6F0',
  fg: '#111111',
  muted: '#6B6B66',
  divider: '#DDD8CC',
  dividerHeavy: '#111111',
  stamp: { bg: '#111111', fg: '#F8F6F0' },
} as const;

const dark = {
  bg: '#111111',
  fg: '#F0ECE4',
  muted: '#888888',
  divider: '#333333',
  dividerHeavy: '#F0ECE4',
  stamp: { bg: '#F0ECE4', fg: '#111111' },
} as const;

export const palette = { light, dark } as const;

/** Convenience: resolve a full palette object from the key */
export const getPalette = (p: Palette) => palette[p];

/* ── Signal colors (data-adjacent only, both palettes) ── */

export const signal = {
  alert: '#C0392B',
  healthy: '#2E7D32',
  caution: '#E68A00',
} as const;

/* ── Legacy `color` export (backwards compat during migration) ── */

export const color = {
  bg: light.bg,
  fg: light.fg,
  muted: light.muted,
  line: light.fg,
  paper: '#F4F1EA',
  accent: signal.alert,
  ok: signal.healthy,
  warn: signal.caution,
} as const;

/* ── Typography ──────────────────────────────────────── */

export const font = {
  mono: "'IBM Plex Mono', 'Courier New', monospace",
  body: "'Inter', system-ui, sans-serif",
} as const;

export const type = {
  hero: {
    fontSize: 150,
    lineHeight: 0.98,
    letterSpacing: '-0.025em',
    fontFamily: font.body,
    fontWeight: 800,
  },
  xl: {
    fontSize: 128,
    lineHeight: 0.98,
    letterSpacing: '-0.03em',
    fontFamily: font.body,
    fontWeight: 700,
  },
  l: {
    fontSize: 108,
    lineHeight: 1.04,
    letterSpacing: '-0.02em',
    fontFamily: font.body,
    fontWeight: 700,
  },
  m: {
    fontSize: 96,
    lineHeight: 1,
    letterSpacing: '-0.02em',
    fontFamily: font.body,
    fontWeight: 700,
  },
  s: {
    fontSize: 88,
    lineHeight: 1.04,
    letterSpacing: '-0.02em',
    fontFamily: font.body,
    fontWeight: 700,
  },
  bodyL: {
    fontSize: 32,
    lineHeight: 1.4,
    fontFamily: font.body,
    fontWeight: 400,
  },
  bodyM: {
    fontSize: 28,
    lineHeight: 1.45,
    fontFamily: font.body,
    fontWeight: 400,
  },
  dataXl: {
    fontSize: 120,
    lineHeight: 1,
    fontFamily: font.mono,
    fontWeight: 700,
  },
  dataL: {
    fontSize: 64,
    lineHeight: 1,
    fontFamily: font.mono,
    fontWeight: 700,
  },
  dataM: {
    fontSize: 40,
    lineHeight: 1,
    fontFamily: font.mono,
    fontWeight: 700,
  },
  label: {
    fontSize: 24,
    lineHeight: 1,
    letterSpacing: '0.14em',
    textTransform: 'uppercase' as const,
    fontFamily: font.mono,
    fontWeight: 500,
  },
  count: {
    fontSize: 24,
    lineHeight: 1,
    letterSpacing: '0.10em',
    fontFamily: font.mono,
    fontWeight: 400,
  },
  caption: {
    fontSize: 22,
    lineHeight: 1.3,
    letterSpacing: '0.10em',
    fontFamily: font.mono,
    fontWeight: 400,
  },
  stamp: {
    fontSize: 32,
    lineHeight: 1,
    letterSpacing: '0.05em',
    fontFamily: font.mono,
    fontWeight: 700,
  },
} as const;

/* ── Canvas ──────────────────────────────────────────── */

export const canvas = {
  width: 1080,
  height: 1350,
  padding: 96,
  bodyMaxWidth: 780,
} as const;

export const videoCanvas = {
  width: 1080,
  height: 1920,
  padding: 80,
} as const;

/* ── Spacing ─────────────────────────────────────────── */

export const spacing = {
  xs: 8,
  sm: 16,
  md: 24,
  lg: 32,
  xl: 40,
  xxl: 48,
  xxxl: 56,
  huge: 64,
  block: 80,
  frame: 96,
  hero: 128,
} as const;
```

- [ ] **Step 2: Verify the file compiles**

Run: `cd remotion && npx tsc --noEmit src/carousel/tokens.ts`

Expected: No errors.

- [ ] **Step 3: Commit**

```bash
git add remotion/src/carousel/tokens.ts
git commit -m "feat: add KOT palette system and updated type scale to tokens"
```

---

### Task 3: Update types

**Files:**
- Modify: `remotion/src/carousel/types.ts`

- [ ] **Step 1: Add palette to CarouselProps and short-form types**

```typescript
import type { Palette } from './tokens';

export interface CoverSlide {
  type: 'cover';
  kicker: string;
  title: string;
  accent?: string;
  subtitle: string;
  issueLabel?: string;
}

export interface QuoteSlide {
  type: 'quote';
  kicker: string;
  preface?: string;
  quote: string;
  attribution?: string;
}

export interface MathSlide {
  type: 'math';
  kicker: string;
  headline: string;
  lines: { label: string; value: string; accent?: boolean }[];
  footnote?: string;
}

export interface ListSlide {
  type: 'list';
  kicker: string;
  headline: string;
  items: { term: string; description: string }[];
}

export interface PullquoteSlide {
  type: 'pullquote';
  kicker: string;
  quote: string;
  meta: { label: string; value: string; accent?: boolean }[];
}

export interface CTASlide {
  type: 'cta';
  kicker: string;
  headline: string;
  body: string;
  pill?: string;
  meta?: string;
}

export type Slide =
  | CoverSlide
  | QuoteSlide
  | MathSlide
  | ListSlide
  | PullquoteSlide
  | CTASlide;

export interface CarouselProps {
  slides: Slide[];
  palette?: Palette;
}

/* ── Short-form types ── */

export type TipLine = { label: string; value: string };

export interface EducationalTipProps {
  hook: string;
  problem: string;
  tipLines: TipLine[];
  cta: string;
  audioSrc: string | null;
  durationInFrames: number;
  palette?: Palette;
}

export interface MythBustingProps {
  myth: string;
  reality: string;
  realityNumber: string;
  realityCaption: string;
  proofTitle: string;
  proofBlocks: {
    label: string;
    lines: TipLine[];
  }[];
  cta: string;
  audioSrc: string | null;
  durationInFrames: number;
  palette?: Palette;
}

export interface QuickMathProps {
  question: string;
  ingredients: TipLine[];
  totalCost: string;
  targetPercent: string;
  result: string;
  resultCaption: string;
  cta: string;
  audioSrc: string | null;
  durationInFrames: number;
  palette?: Palette;
}
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/carousel/types.ts
git commit -m "feat: add palette prop and short-form content type interfaces"
```

---

### Task 4: Update primitives — LogoMark

**Files:**
- Modify: `remotion/src/carousel/primitives/LogoMark.tsx`

- [ ] **Step 1: Replace SVG logo with boxed monospace F**

```tsx
import React from 'react';
import { font } from '../tokens';

type LogoMarkProps = {
  size?: number;
  withWordmark?: boolean;
  colorValue?: string;
};

export const LogoMark: React.FC<LogoMarkProps> = ({
  size = 42,
  withWordmark = true,
  colorValue = '#111111',
}) => {
  const borderSize = Math.max(2, Math.round(size / 20));
  const fontSize = Math.round(size * 0.55);
  const wordmarkSize = Math.round(size * 0.65);
  const suffixSize = Math.round(size * 0.45);

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: Math.round(size * 0.2),
        color: colorValue,
      }}
    >
      <span
        style={{
          width: size,
          height: size,
          border: `${borderSize}px solid currentColor`,
          borderRadius: 3,
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: font.mono,
          fontWeight: 700,
          fontSize,
          lineHeight: 1,
        }}
      >
        f
      </span>
      {withWordmark && (
        <span
          style={{
            display: 'inline-flex',
            alignItems: 'baseline',
            gap: 2,
          }}
        >
          <span
            style={{
              fontFamily: font.mono,
              fontWeight: 700,
              fontSize: wordmarkSize,
              letterSpacing: '0.05em',
              lineHeight: 1,
            }}
          >
            foodcosting
          </span>
          <span
            style={{
              fontFamily: font.mono,
              fontWeight: 500,
              fontSize: suffixSize,
              lineHeight: 1,
              opacity: 0.5,
            }}
          >
            .app
          </span>
        </span>
      )}
    </span>
  );
};
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/carousel/primitives/LogoMark.tsx
git commit -m "feat: replace geometric F logo with KOT boxed monospace F"
```

---

### Task 5: Update primitives — Rule

**Files:**
- Modify: `remotion/src/carousel/primitives/Rule.tsx`

- [ ] **Step 1: Replace solid rule with dashed dividers**

```tsx
import React from 'react';

type RuleProps = {
  heavy?: boolean;
  color?: string;
  style?: React.CSSProperties;
};

export const Rule: React.FC<RuleProps> = ({
  heavy = false,
  color = '#DDD8CC',
  style,
}) => {
  return (
    <div
      style={{
        width: '100%',
        height: 0,
        borderTop: `${heavy ? 2 : 1}px dashed ${color}`,
        ...style,
      }}
    />
  );
};
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/carousel/primitives/Rule.tsx
git commit -m "feat: update Rule to dashed dividers with heavy variant"
```

---

### Task 6: Update primitives — SlideFrame, Header, SlideCount, SwipeCue

**Files:**
- Modify: `remotion/src/carousel/primitives/SlideFrame.tsx`
- Modify: `remotion/src/carousel/primitives/Header.tsx`
- Modify: `remotion/src/carousel/primitives/SlideCount.tsx`
- Modify: `remotion/src/carousel/primitives/SwipeCue.tsx`

- [ ] **Step 1: Update SlideFrame to accept palette**

```tsx
import React from 'react';
import { AbsoluteFill } from 'remotion';
import { canvas, font, getPalette, type Palette } from '../tokens';

type SlideFrameProps = React.PropsWithChildren<{
  palette?: Palette;
  bg?: string;
  fg?: string;
  style?: React.CSSProperties;
}>;

export const SlideFrame: React.FC<SlideFrameProps> = ({
  palette: p = 'light',
  bg,
  fg,
  style,
  children,
}) => {
  const pal = getPalette(p);
  return (
    <AbsoluteFill
      style={{
        background: bg ?? pal.bg,
        color: fg ?? pal.fg,
        fontFamily: font.body,
        padding: canvas.padding,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        ...style,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
```

- [ ] **Step 2: Update Header to use palette**

```tsx
import React from 'react';
import { getPalette, type as typ, type Palette } from '../tokens';
import { SlideCount } from './SlideCount';

type HeaderProps = {
  n: number;
  total: number;
  label: string;
  palette?: Palette;
};

export const Header: React.FC<HeaderProps> = ({
  n,
  total,
  label,
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}
    >
      <SlideCount n={n} total={total} palette={p} />
      <span
        style={{
          ...typ.caption,
          color: pal.muted,
          textTransform: 'uppercase',
        }}
      >
        {label}
      </span>
    </div>
  );
};
```

- [ ] **Step 3: Update SlideCount to use palette**

```tsx
import React from 'react';
import { getPalette, type as typ, type Palette } from '../tokens';

type SlideCountProps = {
  n: number;
  total: number;
  palette?: Palette;
  style?: React.CSSProperties;
};

export const SlideCount: React.FC<SlideCountProps> = ({
  n,
  total,
  palette: p = 'light',
  style,
}) => {
  const pal = getPalette(p);
  return (
    <span
      style={{
        ...typ.count,
        color: pal.muted,
        ...style,
      }}
    >
      {String(n).padStart(2, '0')} / {String(total).padStart(2, '0')}
    </span>
  );
};
```

- [ ] **Step 4: Update SwipeCue to use palette**

```tsx
import React from 'react';
import { getPalette, type as typ, type Palette } from '../tokens';

type SwipeCueProps = {
  label?: string;
  palette?: Palette;
};

export const SwipeCue: React.FC<SwipeCueProps> = ({
  label = 'Swipe',
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <div
      style={{
        ...typ.caption,
        display: 'flex',
        alignItems: 'center',
        gap: 10,
        color: pal.muted,
        opacity: 0.85,
        textTransform: 'uppercase',
      }}
    >
      <span>{label}</span>
      <svg width="28" height="12" viewBox="0 0 28 12" fill="none">
        <path
          d="M1 6 H24 M18 1 L25 6 L18 11"
          stroke="currentColor"
          strokeWidth="1.6"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
};
```

- [ ] **Step 5: Commit**

```bash
git add remotion/src/carousel/primitives/SlideFrame.tsx remotion/src/carousel/primitives/Header.tsx remotion/src/carousel/primitives/SlideCount.tsx remotion/src/carousel/primitives/SwipeCue.tsx
git commit -m "feat: update all primitives to support palette system"
```

---

### Task 7: Update carousel slides — AccentText (highlight stamp)

**Files:**
- Modify: `remotion/src/carousel/slides/AccentText.tsx`

- [ ] **Step 1: Replace italic+color accent with highlight stamp**

```tsx
import React from 'react';
import { font, getPalette, type Palette } from '../tokens';

type AccentTextProps = {
  text: string;
  accent?: string;
  palette?: Palette;
};

export const AccentText: React.FC<AccentTextProps> = ({
  text,
  accent,
  palette: p = 'light',
}) => {
  if (!accent) {
    return <>{text}</>;
  }

  const pal = getPalette(p);
  const start = text.toLowerCase().indexOf(accent.toLowerCase());
  if (start === -1) {
    return <>{text}</>;
  }

  const before = text.slice(0, start);
  const matched = text.slice(start, start + accent.length);
  const after = text.slice(start + accent.length);

  return (
    <>
      {before}
      <span
        style={{
          background: pal.stamp.bg,
          color: pal.stamp.fg,
          fontFamily: font.mono,
          fontWeight: 700,
          padding: '0 12px',
          fontStyle: 'normal',
        }}
      >
        {matched}
      </span>
      {after}
    </>
  );
};
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/carousel/slides/AccentText.tsx
git commit -m "feat: replace italic accent with KOT highlight stamp"
```

---

### Task 8: Update carousel slides — Cover

**Files:**
- Modify: `remotion/src/carousel/slides/Cover.tsx`

- [ ] **Step 1: Update Cover with KOT layout**

```tsx
import React from 'react';
import type { CoverSlide } from '../types';
import { getPalette, type as typ, type Palette } from '../tokens';
import { LogoMark } from '../primitives/LogoMark';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';
import { SwipeCue } from '../primitives/SwipeCue';
import { AccentText } from './AccentText';

type CoverProps = CoverSlide & {
  n: number;
  total: number;
  palette?: Palette;
};

export const Cover: React.FC<CoverProps> = ({
  kicker,
  title,
  accent,
  subtitle,
  issueLabel,
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <SlideFrame palette={p} style={{ justifyContent: 'space-between', paddingBottom: 80 }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <LogoMark size={42} withWordmark colorValue={pal.fg} />
        {issueLabel && (
          <span style={{ ...typ.caption, color: pal.muted, textTransform: 'uppercase' }}>
            {issueLabel}
          </span>
        )}
      </div>

      <div>
        <Rule color={pal.divider} style={{ marginBottom: 40 }} />
        <div
          style={{
            ...typ.label,
            color: pal.muted,
            letterSpacing: '0.18em',
            marginBottom: 40,
          }}
        >
          {kicker}
        </div>
        <h1
          style={{
            ...typ.hero,
            margin: 0,
            maxWidth: 888,
          }}
        >
          <AccentText text={title} accent={accent} palette={p} />
        </h1>
        <Rule color={pal.divider} style={{ marginTop: 40 }} />
      </div>

      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-end',
          gap: 48,
        }}
      >
        <p style={{ ...typ.bodyM, color: pal.muted, maxWidth: 520, margin: 0 }}>
          {subtitle}
        </p>
        <SwipeCue palette={p} />
      </div>
    </SlideFrame>
  );
};
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/carousel/slides/Cover.tsx
git commit -m "feat: update Cover slide with KOT receipt framing"
```

---

### Task 9: Update carousel slides — QuoteRule

**Files:**
- Modify: `remotion/src/carousel/slides/QuoteRule.tsx`

- [ ] **Step 1: Update QuoteRule with dashed framing**

```tsx
import React from 'react';
import type { QuoteSlide } from '../types';
import { getPalette, type as typ, type Palette } from '../tokens';
import { Header } from '../primitives/Header';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';

type QuoteRuleProps = QuoteSlide & {
  n: number;
  total: number;
  palette?: Palette;
};

export const QuoteRule: React.FC<QuoteRuleProps> = ({
  n,
  total,
  kicker,
  preface,
  quote,
  attribution,
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <SlideFrame palette={p}>
      <Header n={n} total={total} label={kicker} palette={p} />

      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}
      >
        <Rule color={pal.divider} style={{ marginBottom: 40 }} />
        {preface && (
          <div
            style={{
              ...typ.bodyL,
              color: pal.muted,
              marginBottom: 40,
              textTransform: 'uppercase',
              letterSpacing: '0.10em',
            }}
          >
            {preface}
          </div>
        )}
        <p
          style={{
            ...typ.l,
            fontStyle: 'italic',
            margin: 0,
          }}
        >
          {quote}
        </p>
        <Rule color={pal.divider} style={{ marginTop: 40 }} />
      </div>

      {attribution && (
        <div style={{ ...typ.caption, color: pal.muted }}>
          {attribution}
        </div>
      )}
    </SlideFrame>
  );
};
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/carousel/slides/QuoteRule.tsx
git commit -m "feat: update QuoteRule slide with dashed rule framing"
```

---

### Task 10: Update carousel slides — Math

**Files:**
- Modify: `remotion/src/carousel/slides/Math.tsx`

- [ ] **Step 1: Update Math with receipt line-item layout**

```tsx
import React from 'react';
import type { MathSlide } from '../types';
import { canvas, getPalette, signal, type as typ, type Palette } from '../tokens';
import { Header } from '../primitives/Header';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';

type MathProps = MathSlide & {
  n: number;
  total: number;
  palette?: Palette;
};

export const Math: React.FC<MathProps> = ({
  n,
  total,
  kicker,
  headline,
  lines,
  footnote,
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <SlideFrame palette={p}>
      <Header n={n} total={total} label={kicker} palette={p} />

      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          gap: 36,
        }}
      >
        <p style={{ ...typ.s, margin: 0 }}>{headline}</p>
        <Rule color={pal.divider} />
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          {lines.map((line, i) => {
            const isLast = i === lines.length - 1;
            return (
              <div
                key={`${line.label}-${line.value}`}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline',
                  padding: '18px 0',
                  borderBottom: isLast
                    ? `2px dashed ${pal.dividerHeavy}`
                    : `1px dashed ${pal.divider}`,
                }}
              >
                <span style={{ ...typ.label, textTransform: 'none', letterSpacing: 0, color: pal.muted }}>
                  {line.label}
                </span>
                <span
                  style={{
                    ...typ.dataM,
                    color: line.accent ? signal.alert : pal.fg,
                  }}
                >
                  {line.value}
                </span>
              </div>
            );
          })}
        </div>
        {footnote && (
          <p style={{ ...typ.bodyL, color: pal.muted, maxWidth: canvas.bodyMaxWidth, margin: 0 }}>
            {footnote}
          </p>
        )}
      </div>
    </SlideFrame>
  );
};
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/carousel/slides/Math.tsx
git commit -m "feat: update Math slide with receipt line-item layout"
```

---

### Task 11: Update carousel slides — List

**Files:**
- Modify: `remotion/src/carousel/slides/List.tsx`

- [ ] **Step 1: Update List with mono counters and dashed dividers**

```tsx
import React from 'react';
import type { ListSlide } from '../types';
import { getPalette, type as typ, type Palette } from '../tokens';
import { Header } from '../primitives/Header';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';

type ListProps = ListSlide & {
  n: number;
  total: number;
  palette?: Palette;
};

export const List: React.FC<ListProps> = ({
  n,
  total,
  kicker,
  headline,
  items,
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <SlideFrame palette={p}>
      <Header n={n} total={total} label={kicker} palette={p} />

      <h2 style={{ ...typ.m, margin: '24px 0 48px' }}>{headline}</h2>

      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-start',
        }}
      >
        {items.map((item, index) => (
          <div
            key={`${item.term}-${index}`}
            style={{
              display: 'grid',
              gridTemplateColumns: '60px 280px 1fr',
              alignItems: 'baseline',
              padding: '28px 0',
              borderTop: `1px dashed ${pal.divider}`,
            }}
          >
            <span style={{ ...typ.count, color: pal.divider }}>
              {String(index + 1).padStart(2, '0')}
            </span>
            <span
              style={{
                fontFamily: typ.s.fontFamily,
                fontSize: 56,
                lineHeight: 1,
                fontWeight: 700,
              }}
            >
              {item.term}
            </span>
            <span style={{ ...typ.bodyM, fontSize: 30, color: pal.muted }}>
              {item.description}
            </span>
          </div>
        ))}
        <Rule color={pal.divider} />
      </div>
    </SlideFrame>
  );
};
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/carousel/slides/List.tsx
git commit -m "feat: update List slide with mono counters and dashed dividers"
```

---

### Task 12: Update carousel slides — Pullquote

**Files:**
- Modify: `remotion/src/carousel/slides/Pullquote.tsx`

- [ ] **Step 1: Update Pullquote with signal colors and no decorative quote mark**

```tsx
import React from 'react';
import type { PullquoteSlide } from '../types';
import { getPalette, signal, type as typ, type Palette } from '../tokens';
import { Header } from '../primitives/Header';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';

type PullquoteProps = PullquoteSlide & {
  n: number;
  total: number;
  palette?: Palette;
};

export const Pullquote: React.FC<PullquoteProps> = ({
  n,
  total,
  kicker,
  quote,
  meta,
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <SlideFrame palette={p}>
      <Header n={n} total={total} label={kicker} palette={p} />

      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign: 'center',
        }}
      >
        <p style={{ ...typ.s, fontSize: 92, lineHeight: 1.08, margin: '0 0 48px' }}>
          {quote}
        </p>
        <Rule color={pal.divider} style={{ marginBottom: 40 }} />
        <div
          style={{
            display: 'flex',
            gap: 48,
          }}
        >
          {meta.map((item) => (
            <div key={`${item.label}-${item.value}`} style={{ textAlign: 'center' }}>
              <div
                style={{
                  ...typ.label,
                  fontSize: 20,
                  color: pal.muted,
                  marginBottom: 8,
                }}
              >
                {item.label}
              </div>
              <div
                style={{
                  ...typ.dataM,
                  fontSize: 34,
                  color: item.accent ? signal.healthy : pal.fg,
                }}
              >
                {item.value}
              </div>
            </div>
          ))}
        </div>
      </div>
    </SlideFrame>
  );
};
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/carousel/slides/Pullquote.tsx
git commit -m "feat: update Pullquote slide with signal colors, remove decorative quote mark"
```

---

### Task 13: Update carousel slides — CTA (always dark)

**Files:**
- Modify: `remotion/src/carousel/slides/CTA.tsx`

- [ ] **Step 1: Update CTA with always-dark palette, receipt footer**

```tsx
import React from 'react';
import type { CTASlide } from '../types';
import { palette, type as typ, font } from '../tokens';
import { LogoMark } from '../primitives/LogoMark';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';

type CTAProps = CTASlide & {
  n: number;
  total: number;
};

export const CTA: React.FC<CTAProps> = ({
  kicker,
  headline,
  body,
  pill = 'link in bio',
  meta = 'save · share · price right',
}) => {
  const pal = palette.dark;
  return (
    <SlideFrame palette="dark" style={{ justifyContent: 'space-between' }}>
      <LogoMark size={48} withWordmark colorValue={pal.fg} />

      <div>
        <Rule color={pal.divider} style={{ marginBottom: 32 }} />
        <div
          style={{
            ...typ.label,
            color: pal.muted,
            letterSpacing: '0.16em',
            marginBottom: 32,
          }}
        >
          {kicker}
        </div>
        <h2 style={{ ...typ.xl, margin: '0 0 40px' }}>{headline}</h2>
        <p style={{ ...typ.bodyL, color: pal.muted, maxWidth: 720, margin: 0 }}>
          {body}
        </p>
      </div>

      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: 48,
        }}
      >
        <div
          style={{
            fontFamily: font.body,
            fontSize: 30,
            fontWeight: 600,
            lineHeight: 1,
            padding: '20px 32px',
            background: pal.fg,
            color: pal.bg,
            borderRadius: 999,
          }}
        >
          {pill}
        </div>
        <span
          style={{
            ...typ.caption,
            color: pal.muted,
          }}
        >
          * * * {meta} * * *
        </span>
      </div>
    </SlideFrame>
  );
};
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/carousel/slides/CTA.tsx
git commit -m "feat: update CTA slide to always-dark with receipt footer"
```

---

### Task 14: Update Carousel.tsx to pass palette

**Files:**
- Modify: `remotion/src/carousel/Carousel.tsx`

- [ ] **Step 1: Thread palette prop through to slides**

```tsx
import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { CarouselProps, Slide, Palette } from './types';
import { Cover } from './slides/Cover';
import { QuoteRule } from './slides/QuoteRule';
import { Math } from './slides/Math';
import { List } from './slides/List';
import { Pullquote } from './slides/Pullquote';
import { CTA } from './slides/CTA';

const renderSlide = (slide: Slide, n: number, total: number, palette: Palette) => {
  switch (slide.type) {
    case 'cover':
      return <Cover {...slide} n={n} total={total} palette={palette} />;
    case 'quote':
      return <QuoteRule {...slide} n={n} total={total} palette={palette} />;
    case 'math':
      return <Math {...slide} n={n} total={total} palette={palette} />;
    case 'list':
      return <List {...slide} n={n} total={total} palette={palette} />;
    case 'pullquote':
      return <Pullquote {...slide} n={n} total={total} palette={palette} />;
    case 'cta':
      return <CTA {...slide} n={n} total={total} />;
  }
};

export const Carousel: React.FC<CarouselProps> = ({ slides, palette = 'light' }) => {
  const frame = useCurrentFrame();
  const slide = slides[frame];

  if (!slide) {
    return null;
  }

  return renderSlide(slide, frame + 1, slides.length, palette);
};
```

Note: `Palette` is re-exported from `types.ts` which imports it from `tokens.ts`. The import uses `type` since it's a type-only import. Update the import in `types.ts` if the TypeScript compiler flags it — it should already work since we added `import type { Palette } from './tokens'` in Task 3.

- [ ] **Step 2: Commit**

```bash
git add remotion/src/carousel/Carousel.tsx
git commit -m "feat: thread palette prop through Carousel to all slides"
```

---

### Task 15: Update short-form scenes — Hook, Problem, Tip, CTA

**Files:**
- Modify: `remotion/src/scenes/Hook.tsx`
- Modify: `remotion/src/scenes/Problem.tsx`
- Modify: `remotion/src/scenes/Tip.tsx`
- Modify: `remotion/src/scenes/CTA.tsx`

- [ ] **Step 1: Rewrite Hook.tsx with KOT receipt-framed layout**

```tsx
import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { font, getPalette, type Palette, videoCanvas } from '../carousel/tokens';

type HookProps = {
  text: string;
  number?: string;
  numberCaption?: string;
  palette?: Palette;
};

export const Hook: React.FC<HookProps> = ({
  text,
  number,
  numberCaption,
  palette: p = 'dark',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(p);

  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 180 } });
  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'center',
        alignItems: 'center',
        padding: videoCanvas.padding,
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          gap: 40,
          width: '100%',
        }}
      >
        {/* Receipt header */}
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
        <span
          style={{
            fontFamily: font.mono,
            fontSize: 22,
            letterSpacing: '0.14em',
            textTransform: 'uppercase',
            color: pal.muted,
          }}
        >
          foodcosting.app
        </span>
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />

        {/* Headline */}
        <div
          style={{
            color: pal.fg,
            fontSize: 72,
            fontWeight: 800,
            fontFamily: font.body,
            lineHeight: 1.15,
            letterSpacing: '-1px',
          }}
        >
          {text}
        </div>

        {/* Hero number */}
        {number && (
          <>
            <div
              style={{
                fontFamily: font.mono,
                fontWeight: 700,
                fontSize: 120,
                lineHeight: 1,
                color: '#C0392B',
              }}
            >
              {number}
            </div>
            {numberCaption && (
              <span
                style={{
                  fontFamily: font.mono,
                  fontSize: 22,
                  color: pal.muted,
                  letterSpacing: '0.05em',
                }}
              >
                {numberCaption}
              </span>
            )}
          </>
        )}

        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
      </div>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 2: Rewrite Problem.tsx with stamp label**

```tsx
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { font, getPalette, signal, type Palette, videoCanvas } from '../carousel/tokens';

type ProblemProps = {
  text: string;
  body?: string;
  palette?: Palette;
};

export const Problem: React.FC<ProblemProps> = ({
  text,
  body,
  palette: p = 'dark',
}) => {
  const frame = useCurrentFrame();
  const pal = getPalette(p);

  const translateY = interpolate(frame, [0, 20], [40, 0], { extrapolateRight: 'clamp' });
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'center',
        padding: videoCanvas.padding,
      }}
    >
      <div
        style={{
          transform: `translateY(${translateY}px)`,
          opacity,
          display: 'flex',
          flexDirection: 'column',
          gap: 32,
        }}
      >
        {/* Stamp */}
        <span
          style={{
            alignSelf: 'flex-start',
            background: signal.alert,
            color: '#FFFFFF',
            fontFamily: font.mono,
            fontWeight: 700,
            fontSize: 28,
            letterSpacing: '0.05em',
            padding: '8px 20px',
          }}
        >
          THE PROBLEM
        </span>

        {/* Headline */}
        <div
          style={{
            color: pal.fg,
            fontSize: 64,
            fontWeight: 700,
            fontFamily: font.body,
            lineHeight: 1.25,
          }}
        >
          {text}
        </div>

        {/* Divider */}
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />

        {/* Body */}
        {body && (
          <div
            style={{
              color: pal.muted,
              fontSize: 36,
              fontFamily: font.body,
              lineHeight: 1.5,
            }}
          >
            {body}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 3: Rewrite Tip.tsx with receipt line-items**

```tsx
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { font, getPalette, signal, type Palette, videoCanvas } from '../carousel/tokens';
import type { TipLine } from '../carousel/types';

type TipProps = {
  lines: TipLine[];
  title?: string;
  totalLabel?: string;
  totalValue?: string;
  palette?: Palette;
};

export const Tip: React.FC<TipProps> = ({
  lines,
  title = 'Ideal food cost %',
  totalLabel,
  totalValue,
  palette: p = 'dark',
}) => {
  const frame = useCurrentFrame();
  const pal = getPalette(p);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'center',
        padding: videoCanvas.padding,
        flexDirection: 'column',
      }}
    >
      {/* Receipt header */}
      <div
        style={{
          textAlign: 'center',
          fontFamily: font.mono,
          fontSize: 22,
          letterSpacing: '0.14em',
          textTransform: 'uppercase',
          color: pal.muted,
          marginBottom: 16,
        }}
      >
        — {title} —
      </div>
      <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}`, marginBottom: 32 }} />

      {/* Staggered line items */}
      {lines.map((line, i) => {
        const delay = i * 25;
        const lineOpacity = interpolate(frame, [delay, delay + 20], [0, 1], {
          extrapolateRight: 'clamp',
        });
        const translateX = interpolate(frame, [delay, delay + 20], [-30, 0], {
          extrapolateRight: 'clamp',
        });

        return (
          <div
            key={`${line.label}-${i}`}
            style={{
              opacity: lineOpacity,
              transform: `translateX(${translateX}px)`,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'baseline',
              padding: '24px 0',
              borderBottom: `1px dashed ${pal.divider}`,
            }}
          >
            <span
              style={{
                fontFamily: font.mono,
                fontSize: 32,
                color: pal.muted,
                letterSpacing: '0.04em',
              }}
            >
              {line.label}
            </span>
            <span
              style={{
                fontFamily: font.mono,
                fontWeight: 700,
                fontSize: 40,
                color: pal.fg,
              }}
            >
              {line.value}
            </span>
          </div>
        );
      })}

      {/* Total row */}
      {totalLabel && totalValue && (
        <>
          <div
            style={{ width: '100%', borderTop: `2px dashed ${pal.dividerHeavy}`, marginTop: 8 }}
          />
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'baseline',
              padding: '24px 0',
            }}
          >
            <span
              style={{
                fontFamily: font.mono,
                fontWeight: 700,
                fontSize: 32,
                color: pal.fg,
              }}
            >
              {totalLabel}
            </span>
            <span
              style={{
                fontFamily: font.mono,
                fontWeight: 700,
                fontSize: 48,
                color: signal.healthy,
              }}
            >
              {totalValue}
            </span>
          </div>
        </>
      )}

      <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}`, marginTop: 16 }} />
    </AbsoluteFill>
  );
};
```

- [ ] **Step 4: Rewrite scenes/CTA.tsx with logo, pill, receipt footer**

```tsx
import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { font, getPalette, type Palette, videoCanvas } from '../carousel/tokens';
import { LogoMark } from '../carousel/primitives/LogoMark';

type CTAProps = {
  text: string;
  palette?: Palette;
};

export const CTA: React.FC<CTAProps> = ({ text, palette: p = 'dark' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(p);

  const scale = spring({ frame, fps, config: { damping: 14, stiffness: 160 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        gap: 48,
        padding: videoCanvas.padding,
      }}
    >
      <div style={{ opacity, transform: `scale(${scale})`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 40 }}>
        <LogoMark size={56} withWordmark colorValue={pal.fg} />

        <div
          style={{
            color: pal.fg,
            fontSize: 52,
            fontWeight: 700,
            fontFamily: font.body,
            textAlign: 'center',
            lineHeight: 1.2,
          }}
        >
          {text}
        </div>

        <div style={{ width: '60%', borderTop: `1px dashed ${pal.divider}` }} />

        {/* Pill */}
        <div
          style={{
            background: pal.fg,
            color: pal.bg,
            borderRadius: 999,
            padding: '16px 48px',
            fontFamily: font.body,
            fontSize: 38,
            fontWeight: 600,
          }}
        >
          foodcosting.app
        </div>

        {/* Receipt footer */}
        <span
          style={{
            fontFamily: font.mono,
            fontSize: 22,
            color: pal.muted,
            letterSpacing: '0.10em',
          }}
        >
          * * * try it free * * *
        </span>
      </div>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 5: Commit**

```bash
git add remotion/src/scenes/Hook.tsx remotion/src/scenes/Problem.tsx remotion/src/scenes/Tip.tsx remotion/src/scenes/CTA.tsx
git commit -m "feat: redesign all short-form scenes with KOT receipt DNA"
```

---

### Task 16: Create Myth-busting scenes

**Files:**
- Create: `remotion/src/scenes/Myth.tsx`
- Create: `remotion/src/scenes/Reality.tsx`
- Create: `remotion/src/scenes/Proof.tsx`

- [ ] **Step 1: Create Myth.tsx**

```tsx
import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { font, getPalette, type Palette, videoCanvas } from '../carousel/tokens';

type MythProps = {
  text: string;
  palette?: Palette;
};

export const Myth: React.FC<MythProps> = ({ text, palette: p = 'dark' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(p);

  const stampScale = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });
  const textOpacity = interpolate(frame, [8, 20], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'center',
        alignItems: 'center',
        padding: videoCanvas.padding,
        textAlign: 'center',
      }}
    >
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 40, width: '100%' }}>
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />

        {/* Stamp */}
        <span
          style={{
            transform: `scale(${stampScale})`,
            display: 'inline-block',
            background: pal.stamp.bg,
            color: pal.stamp.fg,
            fontFamily: font.mono,
            fontWeight: 700,
            fontSize: 36,
            letterSpacing: '0.05em',
            padding: '10px 24px',
          }}
        >
          MYTH
        </span>

        {/* Quote */}
        <div
          style={{
            opacity: textOpacity,
            color: pal.fg,
            fontSize: 60,
            fontWeight: 700,
            fontFamily: font.body,
            fontStyle: 'italic',
            lineHeight: 1.2,
            maxWidth: 900,
          }}
        >
          "{text}"
        </div>

        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />

        <span
          style={{
            opacity: textOpacity,
            fontFamily: font.mono,
            fontSize: 22,
            color: pal.muted,
            letterSpacing: '0.05em',
          }}
        >
          swipe for the truth →
        </span>
      </div>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 2: Create Reality.tsx**

```tsx
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { font, getPalette, signal, type Palette, videoCanvas } from '../carousel/tokens';

type RealityProps = {
  text: string;
  body?: string;
  number: string;
  numberCaption?: string;
  palette?: Palette;
};

export const Reality: React.FC<RealityProps> = ({
  text,
  body,
  number,
  numberCaption,
  palette: p = 'dark',
}) => {
  const frame = useCurrentFrame();
  const pal = getPalette(p);

  const translateY = interpolate(frame, [0, 20], [40, 0], { extrapolateRight: 'clamp' });
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'center',
        padding: videoCanvas.padding,
      }}
    >
      <div
        style={{
          transform: `translateY(${translateY}px)`,
          opacity,
          display: 'flex',
          flexDirection: 'column',
          gap: 32,
        }}
      >
        {/* Stamp */}
        <span
          style={{
            alignSelf: 'flex-start',
            background: signal.healthy,
            color: '#FFFFFF',
            fontFamily: font.mono,
            fontWeight: 700,
            fontSize: 28,
            letterSpacing: '0.05em',
            padding: '8px 20px',
          }}
        >
          REALITY
        </span>

        <div
          style={{
            color: pal.fg,
            fontSize: 56,
            fontWeight: 700,
            fontFamily: font.body,
            lineHeight: 1.25,
          }}
        >
          {text}
        </div>

        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />

        {body && (
          <div
            style={{
              color: pal.muted,
              fontSize: 36,
              fontFamily: font.body,
              lineHeight: 1.5,
            }}
          >
            {body}
          </div>
        )}

        <div
          style={{
            fontFamily: font.mono,
            fontWeight: 700,
            fontSize: 120,
            lineHeight: 1,
            color: signal.healthy,
            marginTop: 16,
          }}
        >
          {number}
        </div>
        {numberCaption && (
          <span
            style={{
              fontFamily: font.mono,
              fontSize: 22,
              color: pal.muted,
              letterSpacing: '0.05em',
            }}
          >
            {numberCaption}
          </span>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 3: Create Proof.tsx**

```tsx
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { font, getPalette, signal, type Palette, videoCanvas } from '../carousel/tokens';
import type { TipLine } from '../carousel/types';

type ProofBlock = {
  label: string;
  lines: TipLine[];
};

type ProofProps = {
  title?: string;
  blocks: ProofBlock[];
  palette?: Palette;
};

export const Proof: React.FC<ProofProps> = ({
  title = 'The math',
  blocks,
  palette: p = 'dark',
}) => {
  const frame = useCurrentFrame();
  const pal = getPalette(p);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'space-between',
        padding: videoCanvas.padding,
        flexDirection: 'column',
      }}
    >
      {/* Receipt header */}
      <div>
        <div
          style={{
            textAlign: 'center',
            fontFamily: font.mono,
            fontSize: 22,
            letterSpacing: '0.14em',
            textTransform: 'uppercase',
            color: pal.muted,
            marginBottom: 16,
          }}
        >
          — {title} —
        </div>
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
      </div>

      {/* Blocks */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 32 }}>
        {blocks.map((block, bi) => {
          const blockDelay = bi * 15;
          const blockOpacity = interpolate(frame, [blockDelay, blockDelay + 15], [0, 1], {
            extrapolateRight: 'clamp',
          });

          return (
            <div key={block.label} style={{ opacity: blockOpacity }}>
              <div
                style={{
                  fontFamily: font.mono,
                  fontSize: 22,
                  color: pal.muted,
                  letterSpacing: '0.05em',
                  textTransform: 'uppercase',
                  marginBottom: 12,
                }}
              >
                {block.label}
              </div>
              {block.lines.map((line, li) => {
                const isLast = li === block.lines.length - 1;
                const lineDelay = blockDelay + (li + 1) * 8;
                const lineOpacity = interpolate(frame, [lineDelay, lineDelay + 12], [0, 1], {
                  extrapolateRight: 'clamp',
                });

                // Color profit lines green, cost lines amber
                const valueColor = line.label.toLowerCase().includes('profit')
                  ? signal.healthy
                  : line.label.toLowerCase().includes('cost')
                    ? signal.caution
                    : pal.fg;

                return (
                  <div
                    key={`${line.label}-${li}`}
                    style={{
                      opacity: lineOpacity,
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'baseline',
                      padding: '16px 0',
                      borderBottom: isLast
                        ? `2px dashed ${pal.dividerHeavy}`
                        : `1px dashed ${pal.divider}`,
                    }}
                  >
                    <span
                      style={{
                        fontFamily: font.mono,
                        fontSize: 28,
                        color: pal.muted,
                      }}
                    >
                      {line.label}
                    </span>
                    <span
                      style={{
                        fontFamily: font.mono,
                        fontWeight: 700,
                        fontSize: 36,
                        color: valueColor,
                      }}
                    >
                      {line.value}
                    </span>
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>

      <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
    </AbsoluteFill>
  );
};
```

- [ ] **Step 4: Commit**

```bash
git add remotion/src/scenes/Myth.tsx remotion/src/scenes/Reality.tsx remotion/src/scenes/Proof.tsx
git commit -m "feat: add Myth, Reality, Proof scenes for myth-busting content type"
```

---

### Task 17: Create Quick Math scenes

**Files:**
- Create: `remotion/src/scenes/Setup.tsx`
- Create: `remotion/src/scenes/Calculation.tsx`

- [ ] **Step 1: Create Setup.tsx**

```tsx
import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { font, getPalette, type Palette, videoCanvas } from '../carousel/tokens';

type SetupProps = {
  question: string;
  palette?: Palette;
};

export const Setup: React.FC<SetupProps> = ({ question, palette: p = 'dark' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(p);

  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 180 } });
  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'center',
        alignItems: 'center',
        padding: videoCanvas.padding,
        textAlign: 'center',
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 40,
          width: '100%',
        }}
      >
        {/* Receipt header */}
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
        <span
          style={{
            fontFamily: font.mono,
            fontSize: 22,
            letterSpacing: '0.14em',
            textTransform: 'uppercase',
            color: pal.muted,
          }}
        >
          foodcosting.app
        </span>
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />

        {/* Question */}
        <div
          style={{
            color: pal.fg,
            fontSize: 64,
            fontWeight: 800,
            fontFamily: font.body,
            lineHeight: 1.15,
          }}
        >
          {question}
        </div>

        {/* $? */}
        <div
          style={{
            fontFamily: font.mono,
            fontWeight: 700,
            fontSize: 140,
            lineHeight: 1,
            color: pal.fg,
          }}
        >
          $?
        </div>

        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
        <span
          style={{
            fontFamily: font.mono,
            fontSize: 22,
            color: pal.muted,
            letterSpacing: '0.05em',
          }}
        >
          let's do the math →
        </span>
      </div>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 2: Create Calculation.tsx**

```tsx
import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { font, getPalette, signal, type Palette, videoCanvas } from '../carousel/tokens';
import type { TipLine } from '../carousel/types';

type CalculationProps = {
  title?: string;
  ingredients: TipLine[];
  totalCost: string;
  targetPercent: string;
  result: string;
  resultCaption?: string;
  palette?: Palette;
};

export const Calculation: React.FC<CalculationProps> = ({
  title = 'Menu price calc',
  ingredients,
  totalCost,
  targetPercent,
  result,
  resultCaption = 'minimum menu price',
  palette: p = 'dark',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(p);

  const resultDelay = (ingredients.length + 2) * 25;
  const resultScale = spring({
    frame: Math.max(0, frame - resultDelay),
    fps,
    config: { damping: 12, stiffness: 160 },
  });
  const resultOpacity = interpolate(frame, [resultDelay, resultDelay + 10], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'space-between',
        padding: videoCanvas.padding,
        flexDirection: 'column',
      }}
    >
      {/* Receipt header */}
      <div>
        <div
          style={{
            textAlign: 'center',
            fontFamily: font.mono,
            fontSize: 22,
            letterSpacing: '0.14em',
            textTransform: 'uppercase',
            color: pal.muted,
            marginBottom: 16,
          }}
        >
          — {title} —
        </div>
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
      </div>

      {/* Ingredients */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        {ingredients.map((item, i) => {
          const delay = i * 25;
          const lineOpacity = interpolate(frame, [delay, delay + 20], [0, 1], {
            extrapolateRight: 'clamp',
          });
          const translateX = interpolate(frame, [delay, delay + 20], [-30, 0], {
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={`${item.label}-${i}`}
              style={{
                opacity: lineOpacity,
                transform: `translateX(${translateX}px)`,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'baseline',
                padding: '20px 0',
                borderBottom: `1px dashed ${pal.divider}`,
              }}
            >
              <span style={{ fontFamily: font.mono, fontSize: 28, color: pal.muted }}>
                {item.label}
              </span>
              <span style={{ fontFamily: font.mono, fontWeight: 700, fontSize: 36, color: pal.fg }}>
                {item.value}
              </span>
            </div>
          );
        })}

        {/* Total cost */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'baseline',
            padding: '20px 0',
            borderBottom: `2px dashed ${pal.dividerHeavy}`,
            opacity: interpolate(frame, [ingredients.length * 25, ingredients.length * 25 + 20], [0, 1], { extrapolateRight: 'clamp' }),
          }}
        >
          <span style={{ fontFamily: font.mono, fontWeight: 700, fontSize: 28, color: pal.fg }}>
            TOTAL COST
          </span>
          <span style={{ fontFamily: font.mono, fontWeight: 700, fontSize: 44, color: pal.fg }}>
            {totalCost}
          </span>
        </div>

        {/* Target % */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'baseline',
            padding: '20px 0',
            borderBottom: `1px dashed ${pal.divider}`,
            opacity: interpolate(frame, [(ingredients.length + 1) * 25, (ingredients.length + 1) * 25 + 20], [0, 1], { extrapolateRight: 'clamp' }),
          }}
        >
          <span style={{ fontFamily: font.mono, fontSize: 28, color: pal.muted }}>
            Target food cost
          </span>
          <span style={{ fontFamily: font.mono, fontWeight: 700, fontSize: 36, color: signal.caution }}>
            {targetPercent}
          </span>
        </div>

        {/* Result */}
        <div
          style={{
            textAlign: 'center',
            marginTop: 40,
            opacity: resultOpacity,
            transform: `scale(${resultScale})`,
          }}
        >
          <div
            style={{
              fontFamily: font.mono,
              fontWeight: 700,
              fontSize: 120,
              lineHeight: 1,
              color: signal.healthy,
            }}
          >
            {result}
          </div>
          <span
            style={{
              fontFamily: font.mono,
              fontSize: 22,
              color: pal.muted,
              letterSpacing: '0.05em',
            }}
          >
            {resultCaption}
          </span>
        </div>
      </div>

      <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
    </AbsoluteFill>
  );
};
```

- [ ] **Step 3: Commit**

```bash
git add remotion/src/scenes/Setup.tsx remotion/src/scenes/Calculation.tsx
git commit -m "feat: add Setup and Calculation scenes for quick math content type"
```

---

### Task 18: Create MythBusting and QuickMath compositions

**Files:**
- Create: `remotion/src/MythBusting.tsx`
- Create: `remotion/src/QuickMath.tsx`

- [ ] **Step 1: Create MythBusting.tsx**

```tsx
import React from 'react';
import { AbsoluteFill, Audio, Sequence } from 'remotion';
import type { MythBustingProps } from './carousel/types';
import { getPalette } from './carousel/tokens';
import { Myth } from './scenes/Myth';
import { Reality } from './scenes/Reality';
import { Proof } from './scenes/Proof';
import { CTA } from './scenes/CTA';

export const MythBusting: React.FC<MythBustingProps> = ({
  myth,
  reality,
  realityNumber,
  realityCaption,
  proofTitle,
  proofBlocks,
  cta,
  audioSrc,
  durationInFrames,
  palette: p = 'dark',
}) => {
  const pal = getPalette(p);
  const mythEnd = Math.floor(durationInFrames * 0.2);
  const realityEnd = Math.floor(durationInFrames * 0.4);
  const proofEnd = Math.floor(durationInFrames * 0.8);

  return (
    <AbsoluteFill style={{ backgroundColor: pal.bg }}>
      {audioSrc && <Audio src={audioSrc} />}

      <Sequence from={0} durationInFrames={mythEnd}>
        <Myth text={myth} palette={p} />
      </Sequence>

      <Sequence from={mythEnd} durationInFrames={realityEnd - mythEnd}>
        <Reality
          text={reality}
          number={realityNumber}
          numberCaption={realityCaption}
          palette={p}
        />
      </Sequence>

      <Sequence from={realityEnd} durationInFrames={proofEnd - realityEnd}>
        <Proof title={proofTitle} blocks={proofBlocks} palette={p} />
      </Sequence>

      <Sequence from={proofEnd} durationInFrames={durationInFrames - proofEnd}>
        <CTA text={cta} palette={p} />
      </Sequence>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 2: Create QuickMath.tsx**

```tsx
import React from 'react';
import { AbsoluteFill, Audio, Sequence } from 'remotion';
import type { QuickMathProps } from './carousel/types';
import { getPalette } from './carousel/tokens';
import { Setup } from './scenes/Setup';
import { Calculation } from './scenes/Calculation';
import { CTA } from './scenes/CTA';

export const QuickMath: React.FC<QuickMathProps> = ({
  question,
  ingredients,
  totalCost,
  targetPercent,
  result,
  resultCaption,
  cta,
  audioSrc,
  durationInFrames,
  palette: p = 'dark',
}) => {
  const pal = getPalette(p);
  const setupEnd = Math.floor(durationInFrames * 0.2);
  const calcEnd = Math.floor(durationInFrames * 0.8);

  return (
    <AbsoluteFill style={{ backgroundColor: pal.bg }}>
      {audioSrc && <Audio src={audioSrc} />}

      <Sequence from={0} durationInFrames={setupEnd}>
        <Setup question={question} palette={p} />
      </Sequence>

      <Sequence from={setupEnd} durationInFrames={calcEnd - setupEnd}>
        <Calculation
          ingredients={ingredients}
          totalCost={totalCost}
          targetPercent={targetPercent}
          result={result}
          resultCaption={resultCaption}
          palette={p}
        />
      </Sequence>

      <Sequence from={calcEnd} durationInFrames={durationInFrames - calcEnd}>
        <CTA text={cta} palette={p} />
      </Sequence>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 3: Commit**

```bash
git add remotion/src/MythBusting.tsx remotion/src/QuickMath.tsx
git commit -m "feat: add MythBusting and QuickMath composition wrappers"
```

---

### Task 19: Update FoodCostTip.tsx with palette support

**Files:**
- Modify: `remotion/src/FoodCostTip.tsx`

- [ ] **Step 1: Add palette prop and use KOT tokens**

```tsx
import React from 'react';
import { AbsoluteFill, Audio, Sequence } from 'remotion';
import type { EducationalTipProps } from './carousel/types';
import { getPalette } from './carousel/tokens';
import { Hook } from './scenes/Hook';
import { Problem } from './scenes/Problem';
import { Tip } from './scenes/Tip';
import { CTA } from './scenes/CTA';

export const FoodCostTip: React.FC<EducationalTipProps> = ({
  hook,
  problem,
  tipLines,
  cta,
  audioSrc,
  durationInFrames,
  palette: p = 'dark',
}) => {
  const pal = getPalette(p);

  const hookEnd = Math.floor(durationInFrames * 0.12);
  const problemEnd = Math.floor(durationInFrames * 0.28);
  const tipEnd = Math.floor(durationInFrames * 0.82);

  return (
    <AbsoluteFill style={{ backgroundColor: pal.bg }}>
      {audioSrc && <Audio src={audioSrc} />}

      <Sequence from={0} durationInFrames={hookEnd}>
        <Hook text={hook} palette={p} />
      </Sequence>

      <Sequence from={hookEnd} durationInFrames={problemEnd - hookEnd}>
        <Problem text={problem} palette={p} />
      </Sequence>

      <Sequence from={problemEnd} durationInFrames={tipEnd - problemEnd}>
        <Tip lines={tipLines} palette={p} />
      </Sequence>

      <Sequence from={tipEnd} durationInFrames={durationInFrames - tipEnd}>
        <CTA text={cta} palette={p} />
      </Sequence>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/FoodCostTip.tsx
git commit -m "feat: update FoodCostTip to use EducationalTipProps with palette"
```

---

### Task 20: Update Root.tsx — register all compositions

**Files:**
- Modify: `remotion/src/Root.tsx`

- [ ] **Step 1: Register MythBusting and QuickMath, update defaults**

```tsx
import React from 'react';
import { Composition } from 'remotion';
import { FoodCostTip } from './FoodCostTip';
import { MythBusting } from './MythBusting';
import { QuickMath } from './QuickMath';
import { Carousel } from './carousel/Carousel';
import './carousel/fonts';
import type { Slide } from './carousel/types';

const defaultCarouselSlides: Slide[] = [
  {
    type: 'cover',
    kicker: 'FOOD COST',
    title: 'Most restaurants calculate food cost after profit is already gone.',
    accent: 'after',
    subtitle:
      'The formula is simple. The hard part is using current prices and real portions before margins drift.',
    issueLabel: 'Field Notes / 02',
  },
  {
    type: 'quote',
    kicker: 'THE OLD HABIT',
    preface: 'You hear it after every busy week -',
    quote: '"Sales were strong, so food cost must be fine."',
    attribution: '- said before the invoices were checked',
  },
  {
    type: 'math',
    kicker: 'FAST MATH',
    headline: 'One burger can move from healthy to risky with a two dollar price gap.',
    lines: [
      { label: 'Plate cost', value: '$3.00' },
      { label: 'Menu price', value: '$10.00' },
      { label: 'Food cost', value: '30%' },
      { label: 'If price drops to $8', value: '37.5%', accent: true },
    ],
    footnote: 'Same burger. Same portion. Very different margin.',
  },
  {
    type: 'list',
    kicker: 'WHAT BREAKS IT',
    headline: 'Three common mistakes make the formula lie.',
    items: [
      { term: 'Portions', description: 'A few extra grams per plate turns a target into a guess.' },
      { term: 'Old prices', description: 'Supplier invoices change before menu prices do.' },
      { term: 'Timing', description: 'Food cost is not a one-time setup task.' },
    ],
  },
  {
    type: 'pullquote',
    kicker: 'DO THIS INSTEAD',
    quote: 'Calculate food cost when prices, portions, or menu items change.',
    meta: [
      { label: 'Best habit', value: 'recalculate before pricing', accent: true },
      { label: 'Watch closely', value: 'prices, portions, menu mix' },
    ],
  },
  {
    type: 'cta',
    kicker: 'PRICE SMARTER',
    headline: 'Cost the plate before you price it.',
    body: 'Use the free calculator to turn ingredient costs into menu prices that leave room for profit.',
    pill: 'link in bio',
    meta: 'save · share · price right',
  },
];

export const RemotionRoot = () => {
  return (
    <>
      {/* Educational Tip (existing, redesigned) */}
      <Composition
        id="FoodCostTip"
        component={FoodCostTip}
        durationInFrames={1650}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          hook: 'Sales can hide food cost problems',
          problem: 'Busy restaurants can still lose profit',
          tipLines: [
            { label: 'Formula', value: 'Food cost / sales' },
            { label: 'Example', value: '$1,200 / $4,000' },
            { label: 'Result', value: '30%' },
            { label: 'Target range', value: '28-35%' },
          ],
          cta: 'Know your numbers.\nPrice with confidence.',
          audioSrc: null,
          durationInFrames: 1650,
          palette: 'dark' as const,
        }}
      />

      {/* Myth-Busting (new) */}
      <Composition
        id="MythBusting"
        component={MythBusting}
        durationInFrames={1500}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          myth: 'Food cost should always be under 30%',
          reality: 'It depends entirely on your concept.',
          realityNumber: '$42',
          realityCaption: 'avg check matters more than %',
          proofTitle: 'The math',
          proofBlocks: [
            {
              label: 'Steakhouse (38% FC)',
              lines: [
                { label: 'Avg check', value: '$42.00' },
                { label: 'Food cost', value: '$15.96' },
                { label: 'Gross profit', value: '$26.04' },
              ],
            },
            {
              label: 'Sandwich shop (28% FC)',
              lines: [
                { label: 'Avg check', value: '$12.00' },
                { label: 'Food cost', value: '$3.36' },
                { label: 'Gross profit', value: '$8.64' },
              ],
            },
          ],
          cta: 'Stop guessing.\nStart calculating.',
          audioSrc: null,
          durationInFrames: 1500,
          palette: 'dark' as const,
        }}
      />

      {/* Quick Math (new) */}
      <Composition
        id="QuickMath"
        component={QuickMath}
        durationInFrames={1050}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          question: 'What should a burger cost on your menu?',
          ingredients: [
            { label: 'Bun', value: '$0.45' },
            { label: 'Patty (6oz)', value: '$2.10' },
            { label: 'Cheese', value: '$0.35' },
            { label: 'Toppings', value: '$0.60' },
          ],
          totalCost: '$3.50',
          targetPercent: '30%',
          result: '$11.67',
          resultCaption: 'minimum menu price',
          cta: 'Price every item\nin minutes.',
          audioSrc: null,
          durationInFrames: 1050,
          palette: 'dark' as const,
        }}
      />

      {/* Carousel */}
      <Composition
        id="Carousel"
        component={Carousel as unknown as React.FC<Record<string, unknown>>}
        durationInFrames={defaultCarouselSlides.length}
        fps={30}
        width={1080}
        height={1350}
        defaultProps={{
          slides: defaultCarouselSlides,
          palette: 'light' as const,
        }}
      />
    </>
  );
};
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/Root.tsx
git commit -m "feat: register MythBusting and QuickMath compositions in Root"
```

---

### Task 21: Build and verify

- [ ] **Step 1: Run TypeScript compilation check**

Run: `cd remotion && npx tsc --noEmit`

Expected: No errors. If there are type errors, fix them before proceeding.

- [ ] **Step 2: Start Remotion studio and visually verify**

Run: `cd remotion && npx remotion studio`

Expected: Studio opens at http://localhost:3000 with 4 compositions:
- FoodCostTip (1080×1920)
- MythBusting (1080×1920)
- QuickMath (1080×1920)
- Carousel (1080×1350)

Check each composition in the preview:
- Colors match KOT tokens (dark: #111 bg, #F0ECE4 text; light: #F8F6F0 bg, #111 text)
- Fonts are IBM Plex Mono (numbers, labels) and Inter (headlines, body)
- Dividers are all dashed, never solid
- Logo is boxed monospace F
- CTA slide in carousel is always dark

- [ ] **Step 3: Fix any visual issues found in studio preview**

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "fix: resolve any build/visual issues from KOT template implementation"
```

Only create this commit if there were fixes. If everything passes clean, skip this step.
