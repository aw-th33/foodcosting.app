import React from 'react';
import type { QuoteSlide } from '../types';
import { getPalette, type as typ, type Palette } from '../tokens';
import { Header } from '../primitives/Header';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';

type QuoteRuleProps = QuoteSlide & {
  n: number;
  total: number;
  palette?: Palette;
};

export const QuoteRule: React.FC<QuoteRuleProps> = ({
  n,
  total,
  kicker,
  preface,
  quote,
  attribution,
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
        }}
      >
        <Rule color={pal.divider} style={{ marginBottom: 40 }} />
        {preface && (
          <div
            style={{
              ...typ.bodyL,
              color: pal.muted,
              marginBottom: 40,
              textTransform: 'uppercase',
              letterSpacing: '0.10em',
            }}
          >
            {preface}
          </div>
        )}
        <p
          style={{
            ...typ.l,
            fontStyle: 'italic',
            margin: 0,
          }}
        >
          {quote}
        </p>
        <Rule color={pal.divider} style={{ marginTop: 40 }} />
      </div>

      {attribution && (
        <div style={{ ...typ.caption, color: pal.muted }}>
          {attribution}
        </div>
      )}
    </SlideFrame>
  );
};
