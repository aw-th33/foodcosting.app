import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { font, getPalette, signal, type Palette, videoCanvas } from '../carousel/tokens';
import type { TipLine } from '../carousel/types';

type ProofBlock = {
  label: string;
  lines: TipLine[];
};

type ProofProps = {
  title?: string;
  blocks: ProofBlock[];
  palette?: Palette;
};

export const Proof: React.FC<ProofProps> = ({
  title = 'The math',
  blocks,
  palette: p = 'dark',
}) => {
  const frame = useCurrentFrame();
  const pal = getPalette(p);

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

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 32 }}>
        {blocks.map((block, bi) => {
          const blockDelay = bi * 15;
          const blockOpacity = interpolate(frame, [blockDelay, blockDelay + 15], [0, 1], {
            extrapolateRight: 'clamp',
          });

          return (
            <div key={block.label} style={{ opacity: blockOpacity }}>
              <div
                style={{
                  fontFamily: font.mono,
                  fontSize: 22,
                  color: pal.muted,
                  letterSpacing: '0.05em',
                  textTransform: 'uppercase',
                  marginBottom: 12,
                }}
              >
                {block.label}
              </div>
              {block.lines.map((line, li) => {
                const isLast = li === block.lines.length - 1;
                const lineDelay = blockDelay + (li + 1) * 8;
                const lineOpacity = interpolate(frame, [lineDelay, lineDelay + 12], [0, 1], {
                  extrapolateRight: 'clamp',
                });

                const valueColor = line.label.toLowerCase().includes('profit')
                  ? signal.healthy
                  : line.label.toLowerCase().includes('cost')
                    ? signal.caution
                    : pal.fg;

                return (
                  <div
                    key={`${line.label}-${li}`}
                    style={{
                      opacity: lineOpacity,
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'baseline',
                      padding: '16px 0',
                      borderBottom: isLast
                        ? `2px dashed ${pal.dividerHeavy}`
                        : `1px dashed ${pal.divider}`,
                    }}
                  >
                    <span
                      style={{
                        fontFamily: font.mono,
                        fontSize: 28,
                        color: pal.muted,
                      }}
                    >
                      {line.label}
                    </span>
                    <span
                      style={{
                        fontFamily: font.mono,
                        fontWeight: 700,
                        fontSize: 36,
                        color: valueColor,
                      }}
                    >
                      {line.value}
                    </span>
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>

      <div style={{ width: '100%', borderTop: `1px dashed ${pal.divider}` }} />
    </AbsoluteFill>
  );
};
