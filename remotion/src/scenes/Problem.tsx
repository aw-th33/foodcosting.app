import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { font, getPalette, signal, type Palette, videoCanvas } from '../carousel/tokens';

type ProblemProps = {
  text: string;
  body?: string;
  palette?: Palette;
};

export const Problem: React.FC<ProblemProps> = ({
  text,
  body,
  palette: p = 'dark',
}) => {
  const frame = useCurrentFrame();
  const pal = getPalette(p);

  const translateY = interpolate(frame, [0, 20], [40, 0], { extrapolateRight: 'clamp' });
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'center',
        padding: videoCanvas.padding,
      }}
    >
      <div
        style={{
          transform: `translateY(${translateY}px)`,
          opacity,
          display: 'flex',
          flexDirection: 'column',
          gap: 32,
        }}
      >
        <span
          style={{
            alignSelf: 'flex-start',
            background: signal.alert,
            color: '#FFFFFF',
            fontFamily: font.mono,
            fontWeight: 700,
            fontSize: 28,
            letterSpacing: '0.05em',
            padding: '8px 20px',
          }}
        >
          THE PROBLEM
        </span>

        <div
          style={{
            color: pal.fg,
            fontSize: 64,
            fontWeight: 700,
            fontFamily: font.body,
            lineHeight: 1.25,
          }}
        >
          {text}
        </div>

        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />

        {body && (
          <div
            style={{
              color: pal.muted,
              fontSize: 36,
              fontFamily: font.body,
              lineHeight: 1.5,
            }}
          >
            {body}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
