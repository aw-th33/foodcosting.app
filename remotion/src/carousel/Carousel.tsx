import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { CarouselProps, Slide } from './types';
import type { Palette } from './tokens';
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
