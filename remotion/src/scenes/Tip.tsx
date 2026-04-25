import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { font, getPalette, signal, type Palette, videoCanvas } from '../carousel/tokens';
import type { TipLine } from '../carousel/types';

type TipProps = {
  lines: TipLine[];
  title?: string;
  totalLabel?: string;
  totalValue?: string;
  palette?: Palette;
};

export const Tip: React.FC<TipProps> = ({
  lines,
  title = 'Ideal food cost %',
  totalLabel,
  totalValue,
  palette: p = 'dark',
}) => {
  const frame = useCurrentFrame();
  const pal = getPalette(p);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: pal.bg,
        justifyContent: 'center',
        padding: videoCanvas.padding,
        flexDirection: 'column',
      }}
    >
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
      <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}`, marginBottom: 32 }} />

      {lines.map((line, i) => {
        const delay = i * 8;
        const lineOpacity = interpolate(frame, [delay, delay + 20], [0, 1], {
          extrapolateRight: 'clamp',
        });
        const translateX = interpolate(frame, [delay, delay + 20], [-30, 0], {
          extrapolateRight: 'clamp',
        });

        return (
          <div
            key={`${line.label}-${i}`}
            style={{
              opacity: lineOpacity,
              transform: `translateX(${translateX}px)`,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'baseline',
              padding: '24px 0',
              borderBottom: `1px dashed ${pal.divider}`,
            }}
          >
            <span
              style={{
                fontFamily: font.mono,
                fontSize: 32,
                color: pal.muted,
                letterSpacing: '0.04em',
              }}
            >
              {line.label}
            </span>
            <span
              style={{
                fontFamily: font.mono,
                fontWeight: 700,
                fontSize: 40,
                color: pal.fg,
              }}
            >
              {line.value}
            </span>
          </div>
        );
      })}

      {totalLabel && totalValue && (
        <>
          <div
            style={{ width: '100%', borderTop: `2px dashed ${pal.dividerHeavy}`, marginTop: 8 }}
          />
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'baseline',
              padding: '24px 0',
            }}
          >
            <span
              style={{
                fontFamily: font.mono,
                fontWeight: 700,
                fontSize: 32,
                color: pal.fg,
              }}
            >
              {totalLabel}
            </span>
            <span
              style={{
                fontFamily: font.mono,
                fontWeight: 700,
                fontSize: 48,
                color: signal.healthy,
              }}
            >
              {totalValue}
            </span>
          </div>
        </>
      )}

      <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}`, marginTop: 16 }} />
    </AbsoluteFill>
  );
};
