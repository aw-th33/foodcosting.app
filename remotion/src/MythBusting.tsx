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
