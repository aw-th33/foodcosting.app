import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { CarouselProps, Slide } from './types';
import { HookSlide } from './HookSlide';
import { ContentSlide } from './ContentSlide';
import { DataSlide } from './DataSlide';
import { CTASlide } from './CTASlide';

const renderSlide = (slide: Slide) => {
  switch (slide.type) {
    case 'hook':
      return <HookSlide {...slide} />;
    case 'content':
      return <ContentSlide {...slide} />;
    case 'data':
      return <DataSlide {...slide} />;
    case 'cta':
      return <CTASlide {...slide} />;
  }
};

export const Carousel: React.FC<CarouselProps> = ({ slides }) => {
  const frame = useCurrentFrame();
  const slide = slides[frame];
  if (!slide) return null;
  return renderSlide(slide);
};
