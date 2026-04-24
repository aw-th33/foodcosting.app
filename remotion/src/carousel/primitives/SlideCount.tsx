import React from 'react';
import { getPalette, type as typ, type Palette } from '../tokens';

type SlideCountProps = {
  n: number;
  total: number;
  palette?: Palette;
  style?: React.CSSProperties;
};

export const SlideCount: React.FC<SlideCountProps> = ({
  n,
  total,
  palette: p = 'light',
  style,
}) => {
  const pal = getPalette(p);
  return (
    <span
      style={{
        ...typ.count,
        color: pal.muted,
        ...style,
      }}
    >
      {String(n).padStart(2, '0')} / {String(total).padStart(2, '0')}
    </span>
  );
};
