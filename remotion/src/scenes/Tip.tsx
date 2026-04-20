import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

type TipLine = { label: string; value: string };

export const Tip = ({ lines }: { lines: TipLine[] }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0F1117',
      justifyContent: 'center',
      alignItems: 'flex-start',
      padding: '100px 80px',
      flexDirection: 'column',
      gap: '0px',
    }}>
      {/* Header */}
      <div style={{
        color: '#328589',
        fontSize: '36px',
        fontWeight: '600',
        fontFamily: 'Inter, sans-serif',
        marginBottom: '60px',
        opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' }),
        letterSpacing: '2px',
        textTransform: 'uppercase',
      }}>
        Ideal food cost %
      </div>

      {/* Staggered lines */}
      {lines.map((line, i) => {
        const delay = i * 25;
        const opacity = interpolate(frame, [delay, delay + 20], [0, 1], { extrapolateRight: 'clamp' });
        const translateX = interpolate(frame, [delay, delay + 20], [-30, 0], { extrapolateRight: 'clamp' });

        return (
          <div key={i} style={{
            opacity,
            transform: `translateX(${translateX}px)`,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            width: '100%',
            borderBottom: '1px solid #1E2330',
            paddingBottom: '40px',
            marginBottom: '40px',
          }}>
            <span style={{
              color: '#A0A8B8',
              fontSize: '52px',
              fontFamily: 'Inter, sans-serif',
              fontWeight: '400',
            }}>
              {line.label}
            </span>
            <span style={{
              color: '#328589',
              fontSize: '60px',
              fontFamily: 'Inter, sans-serif',
              fontWeight: '700',
            }}>
              {line.value}
            </span>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
