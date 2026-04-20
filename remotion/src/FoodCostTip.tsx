import { AbsoluteFill, Audio, Sequence, useVideoConfig } from 'remotion';
import { Hook } from './scenes/Hook';
import { Problem } from './scenes/Problem';
import { Tip } from './scenes/Tip';
import { CTA } from './scenes/CTA';

type TipLine = { label: string; value: string };

type Props = {
  hook: string;
  problem: string;
  tipLines: TipLine[];
  cta: string;
  audioSrc: string | null;
  durationInFrames: number;
};

export const FoodCostTip = ({
  hook,
  problem,
  tipLines,
  cta,
  audioSrc,
  durationInFrames,
}: Props) => {
  const fps = 30;

  // Scene timing — adjust these ratios to taste
  const hookEnd =     Math.floor(durationInFrames * 0.12);  // ~first 12%
  const problemEnd =  Math.floor(durationInFrames * 0.28);  // next 16%
  const tipEnd =      Math.floor(durationInFrames * 0.82);  // bulk of video
  // CTA runs from tipEnd to end

  return (
    <AbsoluteFill style={{ backgroundColor: '#0F1117' }}>

      {/* Audio layer */}
      {audioSrc && <Audio src={audioSrc} />}

      {/* Hook scene */}
      <Sequence from={0} durationInFrames={hookEnd}>
        <Hook text={hook} />
      </Sequence>

      {/* Problem scene */}
      <Sequence from={hookEnd} durationInFrames={problemEnd - hookEnd}>
        <Problem text={problem} />
      </Sequence>

      {/* Tip scene */}
      <Sequence from={problemEnd} durationInFrames={tipEnd - problemEnd}>
        <Tip lines={tipLines} />
      </Sequence>

      {/* CTA scene */}
      <Sequence from={tipEnd} durationInFrames={durationInFrames - tipEnd}>
        <CTA text={cta} />
      </Sequence>

    </AbsoluteFill>
  );
};
