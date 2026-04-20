import { AbsoluteFill, interpolate, useCurrentFrame, spring, useVideoConfig } from 'remotion';

export const Hook = ({ text }: { text: string }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 180 } });
  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#328589',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '80px',
    }}>
      <div style={{
        transform: `scale(${scale})`,
        opacity,
        color: '#FFFFFF',
        fontSize: '72px',
        fontWeight: '800',
        fontFamily: 'Inter, sans-serif',
        textAlign: 'center',
        lineHeight: 1.2,
        letterSpacing: '-1px',
      }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};
