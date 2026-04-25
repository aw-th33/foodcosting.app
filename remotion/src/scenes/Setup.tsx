import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { font, getPalette, type Palette, videoCanvas } from '../carousel/tokens';

type SetupProps = {
  question: string;
  palette?: Palette;
};

export const Setup: React.FC<SetupProps> = ({ question, palette: p = 'dark' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(p);

  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 180 } });
  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'center',
        alignItems: 'center',
        padding: videoCanvas.padding,
        textAlign: 'center',
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 40,
          width: '100%',
        }}
      >
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
        <span
          style={{
            fontFamily: font.mono,
            fontSize: 22,
            letterSpacing: '0.14em',
            textTransform: 'uppercase',
            color: pal.muted,
          }}
        >
          foodcosting.app
        </span>
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />

        <div
          style={{
            color: pal.fg,
            fontSize: 64,
            fontWeight: 800,
            fontFamily: font.body,
            lineHeight: 1.15,
          }}
        >
          {question}
        </div>

        <div
          style={{
            fontFamily: font.mono,
            fontWeight: 700,
            fontSize: 140,
            lineHeight: 1,
            color: pal.fg,
          }}
        >
          $?
        </div>

        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
        <span
          style={{
            fontFamily: font.mono,
            fontSize: 22,
            color: pal.muted,
            letterSpacing: '0.05em',
          }}
        >
          let's do the math →
        </span>
      </div>
    </AbsoluteFill>
  );
};
