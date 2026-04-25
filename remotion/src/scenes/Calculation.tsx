import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { font, getPalette, signal, type Palette, videoCanvas } from '../carousel/tokens';
import type { TipLine } from '../carousel/types';

type CalculationProps = {
  title?: string;
  ingredients: TipLine[];
  totalCost: string;
  targetPercent: string;
  result: string;
  resultCaption?: string;
  palette?: Palette;
};

export const Calculation: React.FC<CalculationProps> = ({
  title = 'Menu price calc',
  ingredients,
  totalCost,
  targetPercent,
  result,
  resultCaption = 'minimum menu price',
  palette: p = 'dark',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(p);

  const resultScale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 160 },
  });
  const resultOpacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'space-between',
        padding: videoCanvas.padding,
        flexDirection: 'column',
      }}
    >
      <div>
        <div
          style={{
            textAlign: 'center',
            fontFamily: font.mono,
            fontSize: 22,
            letterSpacing: '0.14em',
            textTransform: 'uppercase',
            color: pal.muted,
            marginBottom: 16,
          }}
        >
          — {title} —
        </div>
        <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
      </div>

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        {ingredients.map((item, i) => (
          <div
            key={`${item.label}-${i}`}
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'baseline',
              padding: '20px 0',
              borderBottom: `1px dashed ${pal.divider}`,
            }}
          >
            <span style={{ fontFamily: font.mono, fontSize: 28, color: pal.muted }}>
              {item.label}
            </span>
            <span style={{ fontFamily: font.mono, fontWeight: 700, fontSize: 36, color: pal.fg }}>
              {item.value}
            </span>
          </div>
        ))}

        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'baseline',
            padding: '20px 0',
            borderBottom: `2px dashed ${pal.dividerHeavy}`,
          }}
        >
          <span style={{ fontFamily: font.mono, fontWeight: 700, fontSize: 28, color: pal.fg }}>
            TOTAL COST
          </span>
          <span style={{ fontFamily: font.mono, fontWeight: 700, fontSize: 44, color: pal.fg }}>
            {totalCost}
          </span>
        </div>

        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'baseline',
            padding: '20px 0',
            borderBottom: `1px dashed ${pal.divider}`,
          }}
        >
          <span style={{ fontFamily: font.mono, fontSize: 28, color: pal.muted }}>
            Target food cost
          </span>
          <span style={{ fontFamily: font.mono, fontWeight: 700, fontSize: 36, color: signal.caution }}>
            {targetPercent}
          </span>
        </div>

        <div
          style={{
            textAlign: 'center',
            marginTop: 40,
            opacity: resultOpacity,
            transform: `scale(${resultScale})`,
          }}
        >
          <div
            style={{
              fontFamily: font.mono,
              fontWeight: 700,
              fontSize: 120,
              lineHeight: 1,
              color: signal.healthy,
            }}
          >
            {result}
          </div>
          <span
            style={{
              fontFamily: font.mono,
              fontSize: 22,
              color: pal.muted,
              letterSpacing: '0.05em',
            }}
          >
            {resultCaption}
          </span>
        </div>
      </div>

      <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
    </AbsoluteFill>
  );
};
