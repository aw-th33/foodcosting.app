import React from 'react';
import { font } from '../tokens';

type LogoMarkProps = {
  size?: number;
  withWordmark?: boolean;
  colorValue?: string;
};

export const LogoMark: React.FC<LogoMarkProps> = ({
  size = 42,
  withWordmark = true,
  colorValue = '#111111',
}) => {
  const borderSize = Math.max(2, Math.round(size / 20));
  const fontSize = Math.round(size * 0.55);
  const wordmarkSize = Math.round(size * 0.65);
  const suffixSize = Math.round(size * 0.45);

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: Math.round(size * 0.2),
        color: colorValue,
      }}
    >
      <span
        style={{
          width: size,
          height: size,
          border: `${borderSize}px solid currentColor`,
          borderRadius: 3,
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: font.mono,
          fontWeight: 700,
          fontSize,
          lineHeight: 1,
        }}
      >
        f
      </span>
      {withWordmark && (
        <span
          style={{
            display: 'inline-flex',
            alignItems: 'baseline',
            gap: 2,
          }}
        >
          <span
            style={{
              fontFamily: font.mono,
              fontWeight: 700,
              fontSize: wordmarkSize,
              letterSpacing: '0.05em',
              lineHeight: 1,
            }}
          >
            foodcosting
          </span>
          <span
            style={{
              fontFamily: font.mono,
              fontWeight: 500,
              fontSize: suffixSize,
              lineHeight: 1,
              opacity: 0.5,
            }}
          >
            .app
          </span>
        </span>
      )}
    </span>
  );
};
