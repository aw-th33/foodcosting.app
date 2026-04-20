import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const Problem = ({ text }: { text: string }) => {
  const frame = useCurrentFrame();

  const translateY = interpolate(frame, [0, 20], [40, 0], { extrapolateRight: 'clamp' });
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0F1117',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '80px',
    }}>
      {/* Accent bar */}
      <div style={{
        position: 'absolute',
        top: 0, left: 0, right: 0,
        height: '8px',
        backgroundColor: '#328589',
      }} />

      <div style={{
        transform: `translateY(${translateY}px)`,
        opacity,
        color: '#FFFFFF',
        fontSize: '64px',
        fontWeight: '700',
        fontFamily: 'Inter, sans-serif',
        textAlign: 'center',
        lineHeight: 1.3,
      }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};
