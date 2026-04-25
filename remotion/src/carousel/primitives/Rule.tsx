import React from 'react';

type RuleProps = {
  heavy?: boolean;
  color?: string;
  style?: React.CSSProperties;
};

export const Rule: React.FC<RuleProps> = ({
  heavy = false,
  color = '#DDD8CC',
  style,
}) => {
  return (
    <div
      style={{
        width: '100%',
        height: 0,
        borderTop: `${heavy ? 2 : 1}px dashed ${color}`,
        ...style,
      }}
    />
  );
};
