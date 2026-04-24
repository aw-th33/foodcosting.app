import React from 'react';
import { AbsoluteFill } from 'remotion';
import { canvas, font, getPalette, type Palette } from '../tokens';

type SlideFrameProps = React.PropsWithChildren<{
  palette?: Palette;
  bg?: string;
  fg?: string;
  style?: React.CSSProperties;
}>;

export const SlideFrame: React.FC<SlideFrameProps> = ({
  palette: p = 'light',
  bg,
  fg,
  style,
  children,
}) => {
  const pal = getPalette(p);
  return (
    <AbsoluteFill
      style={{
        background: bg ?? pal.bg,
        color: fg ?? pal.fg,
        fontFamily: font.body,
        padding: canvas.padding,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        ...style,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
