import React from 'react';
import { Composition } from 'remotion';
import { FoodCostTip } from './FoodCostTip';
import { MythBusting } from './MythBusting';
import { QuickMath } from './QuickMath';
import { Carousel } from './carousel/Carousel';
import './carousel/fonts';
import type { Slide } from './carousel/types';

const defaultCarouselSlides: Slide[] = [
  {
    type: 'cover',
    kicker: 'FOOD COST',
    title: 'Most restaurants calculate food cost after profit is already gone.',
    accent: 'after',
    subtitle:
      'The formula is simple. The hard part is using current prices and real portions before margins drift.',
    issueLabel: 'Field Notes / 02',
  },
  {
    type: 'quote',
    kicker: 'THE OLD HABIT',
    preface: 'You hear it after every busy week -',
    quote: '"Sales were strong, so food cost must be fine."',
    attribution: '- said before the invoices were checked',
  },
  {
    type: 'math',
    kicker: 'FAST MATH',
    headline: 'One burger can move from healthy to risky with a two dollar price gap.',
    lines: [
      { label: 'Plate cost', value: '$3.00' },
      { label: 'Menu price', value: '$10.00' },
      { label: 'Food cost', value: '30%' },
      { label: 'If price drops to $8', value: '37.5%', accent: true },
    ],
    footnote: 'Same burger. Same portion. Very different margin.',
  },
  {
    type: 'list',
    kicker: 'WHAT BREAKS IT',
    headline: 'Three common mistakes make the formula lie.',
    items: [
      { term: 'Portions', description: 'A few extra grams per plate turns a target into a guess.' },
      { term: 'Old prices', description: 'Supplier invoices change before menu prices do.' },
      { term: 'Timing', description: 'Food cost is not a one-time setup task.' },
    ],
  },
  {
    type: 'pullquote',
    kicker: 'DO THIS INSTEAD',
    quote: 'Calculate food cost when prices, portions, or menu items change.',
    meta: [
      { label: 'Best habit', value: 'recalculate before pricing', accent: true },
      { label: 'Watch closely', value: 'prices, portions, menu mix' },
    ],
  },
  {
    type: 'cta',
    kicker: 'PRICE SMARTER',
    headline: 'Cost the plate before you price it.',
    body: 'Use the free calculator to turn ingredient costs into menu prices that leave room for profit.',
    pill: 'link in bio',
    meta: 'save · share · price right',
  },
];

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="FoodCostTip"
        component={FoodCostTip as unknown as React.FC<Record<string, unknown>>}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          hook: 'Sales can hide food cost problems',
          problem: 'Busy restaurants can still lose profit',
          tipLines: [
            { label: 'Formula', value: 'Food cost / sales' },
            { label: 'Example', value: '$1,200 / $4,000' },
            { label: 'Result', value: '30%' },
            { label: 'Target range', value: '28-35%' },
          ],
          cta: 'Know your numbers.\nPrice with confidence.',
          audioSrc: '/audio/foodcosttip-voice.mp3',
          durationInFrames: 450,
          palette: 'dark' as const,
        }}
      />

      <Composition
        id="MythBusting"
        component={MythBusting as unknown as React.FC<Record<string, unknown>>}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          myth: 'Food cost should always be under 30%',
          reality: 'It depends entirely on your concept.',
          realityNumber: '$42',
          realityCaption: 'avg check matters more than %',
          proofTitle: 'The math',
          proofBlocks: [
            {
              label: 'Steakhouse (38% FC)',
              lines: [
                { label: 'Avg check', value: '$42.00' },
                { label: 'Food cost', value: '$15.96' },
                { label: 'Gross profit', value: '$26.04' },
              ],
            },
            {
              label: 'Sandwich shop (28% FC)',
              lines: [
                { label: 'Avg check', value: '$12.00' },
                { label: 'Food cost', value: '$3.36' },
                { label: 'Gross profit', value: '$8.64' },
              ],
            },
          ],
          cta: 'Stop guessing.\nStart calculating.',
          audioSrc: '/audio/mythbusting-voice.mp3',
          durationInFrames: 450,
          palette: 'dark' as const,
        }}
      />

      <Composition
        id="QuickMath"
        component={QuickMath as unknown as React.FC<Record<string, unknown>>}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          question: 'What should a burger cost on your menu?',
          ingredients: [
            { label: 'Bun', value: '$0.45' },
            { label: 'Patty (6oz)', value: '$2.10' },
            { label: 'Cheese', value: '$0.35' },
            { label: 'Toppings', value: '$0.60' },
          ],
          totalCost: '$3.50',
          targetPercent: '30%',
          result: '$11.67',
          resultCaption: 'minimum menu price',
          cta: 'Price every item\nin minutes.',
          audioSrc: '/audio/quickmath-voice.mp3',
          durationInFrames: 450,
          palette: 'dark' as const,
        }}
      />

      <Composition
        id="Carousel"
        component={Carousel as unknown as React.FC<Record<string, unknown>>}
        durationInFrames={defaultCarouselSlides.length}
        fps={30}
        width={1080}
        height={1350}
        defaultProps={{
          slides: defaultCarouselSlides,
          palette: 'light' as const,
        }}
      />
    </>
  );
};
