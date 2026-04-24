import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { font, getPalette, type Palette, videoCanvas } from '../carousel/tokens';
import { LogoMark } from '../carousel/primitives/LogoMark';

type CTAProps = {
  text: string;
  palette?: Palette;
};

export const CTA: React.FC<CTAProps> = ({ text, palette: p = 'dark' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(p);

  const scale = spring({ frame, fps, config: { damping: 14, stiffness: 160 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        gap: 48,
        padding: videoCanvas.padding,
      }}
    >
      <div style={{ opacity, transform: `scale(${scale})`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 40 }}>
        <LogoMark size={56} withWordmark colorValue={pal.fg} />

        <div
          style={{
            color: pal.fg,
            fontSize: 52,
            fontWeight: 700,
            fontFamily: font.body,
            textAlign: 'center',
            lineHeight: 1.2,
          }}
        >
          {text}
        </div>

        <div style={{ width: '60%', borderTop: `1px dashed ${pal.divider}` }} />

        <div
          style={{
            background: pal.fg,
            color: pal.bg,
            borderRadius: 999,
            padding: '16px 48px',
            fontFamily: font.body,
            fontSize: 38,
            fontWeight: 600,
          }}
        >
          foodcosting.app
        </div>

        <span
          style={{
            fontFamily: font.mono,
            fontSize: 22,
            color: pal.muted,
            letterSpacing: '0.10em',
          }}
        >
          * * * try it free * * *
        </span>
      </div>
    </AbsoluteFill>
  );
};
