import React from 'react';
import { AbsoluteFill } from 'remotion';
import { colors, font, canvas } from './tokens';
import type { ContentSlide as ContentSlideProps } from './types';

const HorizontalBar: React.FC<{
  data: { label: string; value: number; color: string }[];
  unit?: string;
}> = ({ data, unit }) => {
  const maxValue = Math.max(...data.map((d) => d.value));
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 32, width: canvas.contentWidth }}>
      {data.map((item) => (
        <div key={item.label} style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          <div
            style={{
              fontSize: 28,
              fontWeight: 500,
              color: colors.mist,
            }}
          >
            {item.label}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <div
              style={{
                flex: 1,
                height: 48,
                backgroundColor: colors.surface,
                borderRadius: 4,
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  width: `${(item.value / maxValue) * 100}%`,
                  height: '100%',
                  backgroundColor: item.color,
                  borderRadius: 4,
                }}
              />
            </div>
            <div
              style={{
                fontSize: 32,
                fontWeight: 700,
                color: item.color,
                minWidth: 80,
                textAlign: 'right',
              }}
            >
              {item.value}
              {unit || ''}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

const TwoColumn: React.FC<{
  data: { label: string; value: number; color: string }[];
  unit?: string;
}> = ({ data, unit }) => {
  return (
    <div style={{ display: 'flex', width: canvas.contentWidth, position: 'relative' }}>
      {/* Divider */}
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: 0,
          bottom: 0,
          width: 1,
          backgroundColor: colors.divider,
        }}
      />
      {data.slice(0, 2).map((item, i) => (
        <div
          key={item.label}
          style={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 20,
            padding: '20px 0',
          }}
        >
          <div style={{ fontSize: 120, fontWeight: 800, color: item.color, lineHeight: 1 }}>
            {item.value}
            {unit || ''}
          </div>
          <div style={{ fontSize: 28, fontWeight: 400, color: colors.mist }}>
            {item.label}
          </div>
        </div>
      ))}
    </div>
  );
};

export const ContentSlide: React.FC<ContentSlideProps> = ({
  phaseLabel,
  keyPoint,
  detail,
  chart,
}) => {
  // When a chart is present, start content higher to fit everything
  const startY = chart ? 360 : canvas.contentY;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.white,
        fontFamily: font.family,
      }}
    >
      <div
        style={{
          position: 'absolute',
          top: startY,
          left: canvas.padding,
          right: canvas.padding,
          bottom: canvas.padding,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* Phase label at y=640 */}
        <div
          style={{
            fontSize: 28,
            fontWeight: 500,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            color: colors.mist,
            marginBottom: 20,
          }}
        >
          {phaseLabel}
        </div>

        {/* Content headline */}
        <div
          style={{
            fontSize: 56,
            fontWeight: 700,
            color: colors.obsidian,
            lineHeight: 1.1,
            letterSpacing: '-0.02em',
            maxWidth: canvas.contentWidth,
            marginBottom: 40,
          }}
        >
          {keyPoint}
        </div>

        {/* Body text */}
        <div
          style={{
            fontSize: 32,
            fontWeight: 400,
            color: colors.detail,
            lineHeight: 1.5,
            maxWidth: canvas.contentWidth,
          }}
        >
          {detail}
        </div>

        {/* Chart */}
        {chart && (
          <div style={{ marginTop: 48 }}>
            {(chart.type === 'horizontal-bar' || chart.type === 'percentage-bar') && (
              <HorizontalBar data={chart.data} unit={chart.unit} />
            )}
            {chart.type === 'two-column' && (
              <TwoColumn data={chart.data} unit={chart.unit} />
            )}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
