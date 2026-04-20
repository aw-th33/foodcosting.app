import React from 'react';
import { AbsoluteFill } from 'remotion';
import { colors, font, canvas } from './tokens';
import type { HookSlide as HookSlideProps } from './types';

export const HookSlide: React.FC<HookSlideProps> = ({
  headline,
  subtext,
  ghostNumber,
}) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.white,
        fontFamily: font.family,
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {ghostNumber && (
        <div
          style={{
            position: 'absolute',
            fontSize: 360,
            fontWeight: 800,
            color: colors.ghost,
            letterSpacing: '-0.06em',
            lineHeight: 1,
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            userSelect: 'none',
            zIndex: 0,
          }}
        >
          {ghostNumber}
        </div>
      )}

      {/* Headline centered around y=400-680 */}
      <div
        style={{
          position: 'absolute',
          top: 400,
          left: canvas.padding,
          right: canvas.padding,
          bottom: 400,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1,
          gap: 40,
        }}
      >
        <div
          style={{
            fontSize: 80,
            fontWeight: 800,
            color: colors.obsidian,
            letterSpacing: '-0.03em',
            lineHeight: 1.1,
            textAlign: 'center',
            maxWidth: canvas.contentWidth,
          }}
        >
          {headline}
        </div>

        {subtext && (
          <div
            style={{
              fontSize: 36,
              fontWeight: 400,
              color: colors.mist,
              lineHeight: 1.4,
              textAlign: 'center',
            }}
          >
            {subtext}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
