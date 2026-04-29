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
    fontSize: 128,
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
