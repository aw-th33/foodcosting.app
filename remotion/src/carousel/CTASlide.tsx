import React from 'react';
import { AbsoluteFill } from 'remotion';
import { colors, font } from './tokens';
import type { CTASlide as CTASlideProps } from './types';

export const CTASlide: React.FC<CTASlideProps> = ({
  headline,
  ctaLine,
  socialProof,
}) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.obsidian,
        fontFamily: font.family,
        position: 'relative',
      }}
    >
      {/* Centered content */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 40,
        }}
      >
        <div
          style={{
            fontSize: 60,
            fontWeight: 700,
            color: colors.white,
            lineHeight: 1.1,
            letterSpacing: '-0.02em',
            textAlign: 'center',
            maxWidth: 800,
          }}
        >
          {headline}
        </div>

        <div
          style={{
            fontSize: 32,
            fontWeight: 400,
            color: colors.white,
          }}
        >
          {ctaLine}
        </div>

        {socialProof && (
          <div
            style={{
              fontSize: 24,
              fontWeight: 400,
              color: colors.proofText,
              marginTop: 20,
            }}
          >
            {socialProof}
          </div>
        )}
      </div>

      {/* Wordmark — bottom-right, x=960 (right-aligned), y=1048 */}
      <div
        style={{
          position: 'absolute',
          bottom: 32,
          right: 80,
          fontSize: 24,
          fontWeight: 500,
          color: colors.wordmark,
          letterSpacing: '0.04em',
        }}
      >
        foodcosting.app
      </div>
    </AbsoluteFill>
  );
};
