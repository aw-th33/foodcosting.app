import React from 'react';
import type { CoverSlide } from '../types';
import { getPalette, type as typ, type Palette } from '../tokens';
import { LogoMark } from '../primitives/LogoMark';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';
import { SwipeCue } from '../primitives/SwipeCue';
import { AccentText } from './AccentText';

type CoverProps = CoverSlide & {
  n: number;
  total: number;
  palette?: Palette;
};

export const Cover: React.FC<CoverProps> = ({
  kicker,
  title,
  accent,
  subtitle,
  issueLabel,
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <SlideFrame palette={p} style={{ justifyContent: 'space-between', paddingBottom: 80 }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <LogoMark size={42} withWordmark colorValue={pal.fg} />
        {issueLabel && (
          <span style={{ ...typ.caption, color: pal.muted, textTransform: 'uppercase' }}>
            {issueLabel}
          </span>
        )}
      </div>

      <div>
        <Rule color={pal.divider} style={{ marginBottom: 40 }} />
        <div
          style={{
            ...typ.label,
            color: pal.muted,
            letterSpacing: '0.18em',
            marginBottom: 40,
          }}
        >
          {kicker}
        </div>
        <h1
          style={{
            ...typ.hero,
            margin: 0,
            maxWidth: 888,
          }}
        >
          <AccentText text={title} accent={accent} palette={p} />
        </h1>
        <Rule color={pal.divider} style={{ marginTop: 40 }} />
      </div>

      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-end',
          gap: 48,
        }}
      >
        <p style={{ ...typ.bodyM, color: pal.muted, maxWidth: 520, margin: 0 }}>
          {subtitle}
        </p>
        <SwipeCue palette={p} />
      </div>
    </SlideFrame>
  );
};
