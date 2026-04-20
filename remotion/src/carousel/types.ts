export interface HookSlide {
  type: 'hook';
  headline: string;
  subtext?: string;
  ghostNumber?: string;
}

export interface ContentSlide {
  type: 'content';
  phaseLabel: string;
  keyPoint: string;
  detail: string;
  chart?: {
    type: 'horizontal-bar' | 'two-column' | 'percentage-bar';
    data: { label: string; value: number; color: string }[];
    unit?: string;
  };
}

export interface DataSlide {
  type: 'data';
  number: string;
  unit: string;
  context: string;
  label?: string;
}

export interface CTASlide {
  type: 'cta';
  headline: string;
  ctaLine: string;
  socialProof?: string;
}

export type Slide = HookSlide | ContentSlide | DataSlide | CTASlide;

export interface CarouselProps {
  slides: Slide[];
}
