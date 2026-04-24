import React from 'react';
import type { MathSlide } from '../types';
import { canvas, getPalette, signal, type as typ, type Palette } from '../tokens';
import { Header } from '../primitives/Header';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';

type MathProps = MathSlide & {
  n: number;
  total: number;
  palette?: Palette;
};

export const Math: React.FC<MathProps> = ({
  n,
  total,
  kicker,
  headline,
  lines,
  footnote,
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <SlideFrame palette={p}>
      <Header n={n} total={total} label={kicker} palette={p} />

      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          gap: 36,
        }}
      >
        <p style={{ ...typ.s, margin: 0 }}>{headline}</p>
        <Rule color={pal.divider} />
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          {lines.map((line, i) => {
            const isLast = i === lines.length - 1;
            return (
              <div
                key={`${line.label}-${line.value}`}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline',
                  padding: '18px 0',
                  borderBottom: isLast
                    ? `2px dashed ${pal.dividerHeavy}`
                    : `1px dashed ${pal.divider}`,
                }}
              >
                <span style={{ ...typ.label, textTransform: 'none', letterSpacing: 0, color: pal.muted }}>
                  {line.label}
                </span>
                <span
                  style={{
                    ...typ.dataM,
                    color: line.accent ? signal.alert : pal.fg,
                  }}
                >
                  {line.value}
                </span>
              </div>
            );
          })}
        </div>
        {footnote && (
          <p style={{ ...typ.bodyL, color: pal.muted, maxWidth: canvas.bodyMaxWidth, margin: 0 }}>
            {footnote}
          </p>
        )}
      </div>
    </SlideFrame>
  );
};
