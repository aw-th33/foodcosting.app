import React from 'react';
import { AbsoluteFill, Audio, Sequence } from 'remotion';
import type { EducationalTipProps } from './carousel/types';
import { getPalette } from './carousel/tokens';
import { Hook } from './scenes/Hook';
import { Tip } from './scenes/Tip';
import { CTA } from './scenes/CTA';

export const FoodCostTip: React.FC<EducationalTipProps> = ({
  hook,
  tipLines,
  cta,
  audioSrc,
  durationInFrames,
  palette: p = 'dark',
}) => {
  const pal = getPalette(p);

  const hookEnd = Math.floor(durationInFrames * 0.20);
  const tipEnd = Math.floor(durationInFrames * 0.80);

  return (
    <AbsoluteFill style={{ backgroundColor: pal.bg }}>
      {audioSrc && <Audio src={audioSrc} />}

      <Sequence from={0} durationInFrames={hookEnd}>
        <Hook text={hook} palette={p} />
      </Sequence>

      <Sequence from={hookEnd} durationInFrames={tipEnd - hookEnd}>
        <Tip lines={tipLines} palette={p} />
      </Sequence>

      <Sequence from={tipEnd} durationInFrames={durationInFrames - tipEnd}>
        <CTA text={cta} palette={p} />
      </Sequence>
    </AbsoluteFill>
  );
};
