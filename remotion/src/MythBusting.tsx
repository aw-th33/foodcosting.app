import React from 'react';
import { AbsoluteFill, Audio, Sequence } from 'remotion';
import type { MythBustingProps } from './carousel/types';
import { getPalette } from './carousel/tokens';
import { Myth } from './scenes/Myth';
import { Reality } from './scenes/Reality';
import { CTA } from './scenes/CTA';

export const MythBusting: React.FC<MythBustingProps> = ({
  myth,
  reality,
  realityNumber,
  realityCaption,
  cta,
  audioSrc,
  musicSrc,
  durationInFrames,
  palette: p = 'dark',
}) => {
  const pal = getPalette(p);

  const mythEnd = Math.floor(durationInFrames * 0.30);
  const realityEnd = Math.floor(durationInFrames * 0.60);

  return (
    <AbsoluteFill style={{ backgroundColor: pal.bg }}>
      {audioSrc && <Audio src={audioSrc} />}
      {musicSrc && <Audio src={musicSrc} volume={0.15} />}

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

      <Sequence from={realityEnd} durationInFrames={durationInFrames - realityEnd}>
        <CTA text={cta} palette={p} />
      </Sequence>
    </AbsoluteFill>
  );
};
