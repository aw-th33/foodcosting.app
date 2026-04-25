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
