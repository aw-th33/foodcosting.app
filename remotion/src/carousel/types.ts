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
