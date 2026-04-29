import React from 'react';
import type { CTASlide } from '../types';
import { palette, type as typ, font } from '../tokens';
import { LogoMark } from '../primitives/LogoMark';
import { Rule } from '../primitives/Rule';
import { SlideFrame } from '../primitives/SlideFrame';

type CTAProps = CTASlide & {
  n: number;
  total: number;
};

export const CTA: React.FC<CTAProps> = ({
  kicker,
  headline,
  body,
  pill = 'link in bio',
  meta = 'save · share · price right',
}) => {
  const pal = palette.dark;
  return (
    <SlideFrame palette="dark" style={{ justifyContent: 'space-between' }}>
      <LogoMark size={48} withWordmark colorValue={pal.fg} />

      <div>
        <Rule color={pal.divider} style={{ marginBottom: 32 }} />
        <div
          style={{
            ...typ.label,
            color: pal.muted,
            letterSpacing: '0.16em',
            marginBottom: 32,
          }}
        >
          {kicker}
        </div>
        <h2 style={{ ...typ.xl, margin: '0 0 40px' }}>{headline}</h2>
        <p style={{ ...typ.bodyL, color: pal.muted, maxWidth: 720, margin: 0 }}>
          {body}
        </p>
      </div>

      <div
        style={{
          display: 'flex',
          alignItems: 'flex-start',
          gap: 48,
        }}
      >
        <div
          style={{
            flexShrink: 0,
            fontFamily: font.body,
            fontSize: 30,
            fontWeight: 600,
            lineHeight: 1,
            padding: '20px 32px',
            background: pal.fg,
            color: pal.bg,
            borderRadius: 999,
          }}
        >
          {pill}
        </div>
        <span
          style={{
            ...typ.caption,
            flex: 1,
            maxWidth: 420,
            color: pal.muted,
          }}
        >
          * * * {meta}
        </span>
      </div>
    </SlideFrame>
  );
};
