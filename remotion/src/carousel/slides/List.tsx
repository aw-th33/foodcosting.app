import React from 'react';
import type { ListSlide } from '../types';
import { getPalette, type as typ, type Palette } from '../tokens';
import { Header } from '../primitives/Header';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';

type ListProps = ListSlide & {
  n: number;
  total: number;
  palette?: Palette;
};

export const List: React.FC<ListProps> = ({
  n,
  total,
  kicker,
  headline,
  items,
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <SlideFrame palette={p}>
      <Header n={n} total={total} label={kicker} palette={p} />

      <h2 style={{ ...typ.m, margin: '24px 0 48px' }}>{headline}</h2>

      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-start',
        }}
      >
        {items.map((item, index) => (
          <div
            key={`${item.term}-${index}`}
            style={{
              display: 'grid',
              gridTemplateColumns: '60px 280px 1fr',
              alignItems: 'baseline',
              padding: '28px 0',
              borderTop: `1px dashed ${pal.divider}`,
            }}
          >
            <span style={{ ...typ.count, color: pal.divider }}>
              {String(index + 1).padStart(2, '0')}
            </span>
            <span
              style={{
                fontFamily: typ.s.fontFamily,
                fontSize: 56,
                lineHeight: 1,
                fontWeight: 700,
              }}
            >
              {item.term}
            </span>
            <span style={{ ...typ.bodyM, fontSize: 30, color: pal.muted }}>
              {item.description}
            </span>
          </div>
        ))}
        <Rule color={pal.divider} />
      </div>
    </SlideFrame>
  );
};
