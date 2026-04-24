import React from 'react';
import { font, getPalette, type Palette } from '../tokens';

type AccentTextProps = {
  text: string;
  accent?: string;
  palette?: Palette;
};

export const AccentText: React.FC<AccentTextProps> = ({
  text,
  accent,
  palette: p = 'light',
}) => {
  if (!accent) {
    return <>{text}</>;
  }

  const pal = getPalette(p);
  const start = text.toLowerCase().indexOf(accent.toLowerCase());
  if (start === -1) {
    return <>{text}</>;
  }

  const before = text.slice(0, start);
  const matched = text.slice(start, start + accent.length);
  const after = text.slice(start + accent.length);

  return (
    <>
      {before}
      <span
        style={{
          background: pal.stamp.bg,
          color: pal.stamp.fg,
          fontFamily: font.mono,
          fontWeight: 700,
          padding: '0 12px',
          fontStyle: 'normal',
        }}
      >
        {matched}
      </span>
      {after}
    </>
  );
};
