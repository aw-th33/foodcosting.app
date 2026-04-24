import React from 'react';
import { getPalette, type as typ, type Palette } from '../tokens';

type SwipeCueProps = {
  label?: string;
  palette?: Palette;
};

export const SwipeCue: React.FC<SwipeCueProps> = ({
  label = 'Swipe',
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <div
      style={{
        ...typ.caption,
        display: 'flex',
        alignItems: 'center',
        gap: 10,
        color: pal.muted,
        opacity: 0.85,
        textTransform: 'uppercase',
      }}
    >
      <span>{label}</span>
      <svg width="28" height="12" viewBox="0 0 28 12" fill="none">
        <path
          d="M1 6 H24 M18 1 L25 6 L18 11"
          stroke="currentColor"
          strokeWidth="1.6"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
};
