import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { font, getPalette, type Palette, videoCanvas } from '../carousel/tokens';

type MythProps = {
  text: string;
  palette?: Palette;
};

export const Myth: React.FC<MythProps> = ({ text, palette: p = 'dark' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(p);

  const stampScale = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });
  const textOpacity = interpolate(frame, [8, 20], [0, 1], { extrapolateRight: 'clamp' });

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
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 40, width: '100%' }}>
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />

        <span
          style={{
            transform: `scale(${stampScale})`,
            display: 'inline-block',
            background: pal.stamp.bg,
            color: pal.stamp.fg,
            fontFamily: font.mono,
            fontWeight: 700,
            fontSize: 36,
            letterSpacing: '0.05em',
            padding: '10px 24px',
          }}
        >
          MYTH
        </span>

        <div
          style={{
            opacity: textOpacity,
            color: pal.fg,
            fontSize: 60,
            fontWeight: 700,
            fontFamily: font.body,
            fontStyle: 'italic',
            lineHeight: 1.2,
            maxWidth: 900,
          }}
        >
          "{text}"
        </div>

        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />

        <span
          style={{
            opacity: textOpacity,
            fontFamily: font.mono,
            fontSize: 22,
            color: pal.muted,
            letterSpacing: '0.05em',
          }}
        >
          swipe for the truth →
        </span>
      </div>
    </AbsoluteFill>
  );
};
