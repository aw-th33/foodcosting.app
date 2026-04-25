import React from 'react';
import { getPalette, type as typ, type Palette } from '../tokens';
import { SlideCount } from './SlideCount';

type HeaderProps = {
  n: number;
  total: number;
  label: string;
  palette?: Palette;
};

export const Header: React.FC<HeaderProps> = ({
  n,
  total,
  label,
  palette: p = 'light',
}) => {
  const pal = getPalette(p);
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}
    >
      <SlideCount n={n} total={total} palette={p} />
      <span
        style={{
          ...typ.caption,
          color: pal.muted,
          textTransform: 'uppercase',
        }}
      >
        {label}
      </span>
    </div>
  );
};
