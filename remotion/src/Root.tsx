import React from 'react';
import { Composition, staticFile } from 'remotion';
import { FoodCostTip } from './FoodCostTip';
import { MythBusting } from './MythBusting';
import { QuickMath } from './QuickMath';
import { Carousel } from './carousel/Carousel';
import './carousel/fonts';
import type { Slide } from './carousel/types';

const defaultCarouselSlides: Slide[] = [
  {
    type: 'cover',
    kicker: 'KNOW YOUR NUMBER',
    title: 'Your food cost target depends on how you cook, not just what you sell',
    accent: 'depends',
    subtitle: 'The "keep it low" advice is not a target. Here are the real benchmarks by business type.',
    issueLabel: 'Field Notes / 02',
  },
  {
    type: 'quote',
    kicker: 'THE COMMON BELIEF',
    preface: 'Every operator hears this early on —',
    quote: '"Keep your food cost low and the margins take care of themselves."',
    attribution: '— said without specifying what "low" means for your format',
  },
  {
    type: 'math',
    kicker: 'THE REAL TARGETS',
    headline: 'Five formats, five different numbers. Which one is yours?',
    lines: [
      { label: 'Full-service restaurant', value: '28-35%', accent: false },
      { label: 'Quick-service / fast casual', value: '32-35%', accent: false },
      { label: 'Food truck', value: '28-32%', accent: false },
      { label: 'Caterer', value: '25-35%', accent: false },
      { label: 'Home baker', value: '30-40%', accent: true },
    ],
    footnote: 'Home bakers run highest because they buy ingredients at retail, not wholesale.',
  },
  {
    type: 'list',
    kicker: 'WHERE IT BREAKS',
    headline: 'Each format has one leak that shows up most often.',
    items: [
      { term: 'Restaurant', description: 'Pricing a dish from memory. Costs shift; the card you wrote in January does not match April\'s invoices.' },
      { term: 'Food truck', description: 'Holding prices steady while portion sizes quietly drift heavier each week.' },
      { term: 'Caterer', description: 'Ignoring buffer prep. Cooking for 90 when 80 people show up is a cost whether the food gets eaten or not.' },
      { term: 'Home baker', description: 'Leaving packaging out of the cost calculation. Boxes, labels, and ribbon are part of the product.' },
    ],
  },
  {
    type: 'pullquote',
    kicker: 'START HERE',
    quote: 'Before you raise prices, check whether your portions have crept up.',
    meta: [
      { label: 'Then check', value: 'supplier invoices vs. six months ago', accent: false },
      { label: 'Then reprice', value: 'if portions are right and costs are market rate', accent: true },
    ],
  },
  {
    type: 'cta',
    kicker: 'CALCULATE YOURS',
    headline: 'Find your food cost in two minutes.',
    body: 'Enter your ingredients and menu price at foodcosting.app. No spreadsheet, no formula — just your number.',
    pill: 'link in bio',
    meta: 'Save this for the next time a dish feels off.',
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
          hook: 'Food trucks need tighter food cost than restaurants',
          problem: "No lease sounds like breathing room. It isn't.",
          tipLines: [
            { label: 'Restaurant ceiling', value: '35%' },
            { label: 'Food truck ceiling', value: '32%' },
            { label: 'Most common cause', value: 'Portion creep' },
            { label: 'First fix', value: 'Re-weigh your top 3 dishes' },
          ],
          cta: 'Calculate yours free at foodcosting.app',
          audioSrc: staticFile('audio/foodcosttip-voice.mp3'),
          musicSrc: staticFile('audio/bg-music.mp3'),
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
          audioSrc: staticFile('audio/mythbusting-voice.mp3'),
          musicSrc: staticFile('audio/bg-music.mp3'),
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
          audioSrc: staticFile('audio/quickmath-voice.mp3'),
          musicSrc: staticFile('audio/bg-music.mp3'),
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
