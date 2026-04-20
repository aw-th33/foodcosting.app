import React from 'react';
import { AbsoluteFill } from 'remotion';
import { colors, font } from './tokens';
import type { DataSlide as DataSlideProps } from './types';

export const DataSlide: React.FC<DataSlideProps> = ({
  number,
  unit,
  context,
  label,
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
      {/* Ghost number — centered, decorative */}
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
        {number}
      </div>

      {/* Label above — y=340 */}
      {label && (
        <div
          style={{
            position: 'absolute',
            top: 340,
            left: 0,
            right: 0,
            textAlign: 'center',
            fontSize: 28,
            fontWeight: 500,
            color: colors.mist,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            zIndex: 1,
          }}
        >
          {label}
        </div>
      )}

      {/* Hero number — centered at y=540 */}
      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          display: 'flex',
          alignItems: 'baseline',
          gap: 8,
          zIndex: 1,
        }}
      >
        <div
          style={{
            fontSize: 200,
            fontWeight: 800,
            color: colors.obsidian,
            letterSpacing: '-0.04em',
            lineHeight: 1,
          }}
        >
          {number}
        </div>
        <div
          style={{
            fontSize: 80,
            fontWeight: 400,
            color: colors.mist,
            lineHeight: 1,
          }}
        >
          {unit}
        </div>
      </div>

      {/* Context line — y=700 */}
      <div
        style={{
          position: 'absolute',
          top: 700,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontSize: 32,
          fontWeight: 400,
          color: colors.detail,
          zIndex: 1,
          padding: '0 80px',
        }}
      >
        {context}
      </div>
    </AbsoluteFill>
  );
};
