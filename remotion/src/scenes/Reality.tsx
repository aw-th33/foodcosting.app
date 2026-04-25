import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { font, getPalette, signal, type Palette, videoCanvas } from '../carousel/tokens';

type RealityProps = {
  text: string;
  body?: string;
  number: string;
  numberCaption?: string;
  palette?: Palette;
};

export const Reality: React.FC<RealityProps> = ({
  text,
  body,
  number,
  numberCaption,
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
            background: signal.healthy,
            color: '#FFFFFF',
            fontFamily: font.mono,
            fontWeight: 700,
            fontSize: 28,
            letterSpacing: '0.05em',
            padding: '8px 20px',
          }}
        >
          REALITY
        </span>

        <div
          style={{
            color: pal.fg,
            fontSize: 56,
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

        <div
          style={{
            fontFamily: font.mono,
            fontWeight: 700,
            fontSize: 120,
            lineHeight: 1,
            color: signal.healthy,
            marginTop: 16,
          }}
        >
          {number}
        </div>
        {numberCaption && (
          <span
            style={{
              fontFamily: font.mono,
              fontSize: 22,
              color: pal.muted,
              letterSpacing: '0.05em',
            }}
          >
            {numberCaption}
          </span>
        )}
      </div>
    </AbsoluteFill>
  );
};
