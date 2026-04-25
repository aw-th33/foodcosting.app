import React from 'react';
import type { PullquoteSlide } from '../types';
import { getPalette, signal, type as typ, type Palette } from '../tokens';
import { Header } from '../primitives/Header';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';

type PullquoteProps = PullquoteSlide & {
  n: number;
  total: number;
  palette?: Palette;
};

export const Pullquote: React.FC<PullquoteProps> = ({
  n,
  total,
  kicker,
  quote,
  meta,
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
          alignItems: 'center',
          textAlign: 'center',
        }}
      >
        <p style={{ ...typ.s, fontSize: 92, lineHeight: 1.08, margin: '0 0 48px' }}>
          {quote}
        </p>
        <Rule color={pal.divider} style={{ marginBottom: 40 }} />
        <div
          style={{
            display: 'flex',
            gap: 48,
          }}
        >
          {meta.map((item) => (
            <div key={`${item.label}-${item.value}`} style={{ textAlign: 'center' }}>
              <div
                style={{
                  ...typ.label,
                  fontSize: 20,
                  color: pal.muted,
                  marginBottom: 8,
                }}
              >
                {item.label}
              </div>
              <div
                style={{
                  ...typ.dataM,
                  fontSize: 34,
                  color: item.accent ? signal.healthy : pal.fg,
                }}
              >
                {item.value}
              </div>
            </div>
          ))}
        </div>
      </div>
    </SlideFrame>
  );
};
