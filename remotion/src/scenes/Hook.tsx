import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { font, getPalette, type Palette, videoCanvas } from '../carousel/tokens';

type HookProps = {
  text: string;
  number?: string;
  numberCaption?: string;
  palette?: Palette;
};

export const Hook: React.FC<HookProps> = ({
  text,
  number,
  numberCaption,
  palette: p = 'dark',
}) => {
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
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
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
            fontSize: 72,
            fontWeight: 800,
            fontFamily: font.body,
            lineHeight: 1.15,
            letterSpacing: '-1px',
          }}
        >
          {text}
        </div>

        {number && (
          <>
            <div
              style={{
                fontFamily: font.mono,
                fontWeight: 700,
                fontSize: 120,
                lineHeight: 1,
                color: '#C0392B',
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
          </>
        )}

        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
      </div>
    </AbsoluteFill>
  );
};
