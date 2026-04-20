import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const CTA = ({ text }: { text: string }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 14, stiffness: 160 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#328589',
      justifyContent: 'center',
      alignItems: 'center',
      flexDirection: 'column',
      gap: '40px',
      padding: '80px',
    }}>
      <div style={{
        opacity,
        transform: `scale(${scale})`,
        color: '#FFFFFF',
        fontSize: '52px',
        fontWeight: '800',
        fontFamily: 'Inter, sans-serif',
        textAlign: 'center',
        lineHeight: 1.3,
      }}>
        {text}
      </div>

      {/* URL pill */}
      <div style={{
        opacity,
        backgroundColor: 'rgba(255,255,255,0.15)',
        borderRadius: '100px',
        padding: '20px 50px',
        color: '#FFFFFF',
        fontSize: '38px',
        fontFamily: 'Inter, sans-serif',
        fontWeight: '600',
        letterSpacing: '1px',
      }}>
        foodcosting.app
      </div>
    </AbsoluteFill>
  );
};
