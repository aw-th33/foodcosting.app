import { Composition } from 'remotion';
import { FoodCostTip } from './FoodCostTip';
import { Carousel } from './carousel/Carousel';
import type { Slide } from './carousel/types';

const defaultCarouselSlides: Slide[] = [
  {
    type: 'hook',
    headline: "Most restaurants think they know their food cost. They don't.",
  },
  {
    type: 'content',
    phaseLabel: '01 /',
    keyPoint: 'They use supplier invoices, not recipe costs',
    detail:
      'Knowing what you paid for chicken last week is not the same as knowing what that chicken costs per plate. Invoice totals hide the number that matters — cost per serving.',
  },
  {
    type: 'content',
    phaseLabel: '02 /',
    keyPoint: 'Portions drift without anyone noticing',
    detail:
      'A cook who adds an extra ounce of protein per plate costs you 6-8% on that dish over a month. Without a costed recipe, there\'s no baseline to catch the drift.',
    chart: {
      type: 'horizontal-bar',
      data: [
        { label: 'Target portion: 6oz', value: 6, color: '#328589' },
        { label: 'Actual portion: 7oz', value: 7, color: '#E05252' },
      ],
      unit: 'oz',
    },
  },
  {
    type: 'content',
    phaseLabel: '03 /',
    keyPoint: 'Menu prices were set once and never recalculated',
    detail:
      'Ingredient prices shift 10-20% per quarter. A menu priced 6 months ago is running on outdated math. Every week without recalculating is margin you\'re giving away.',
  },
  {
    type: 'content',
    phaseLabel: '04 /',
    keyPoint: 'The gap between perceived and actual food cost',
    detail:
      'Operators who estimate their food cost vs. those who calculate it see an average gap of 4-7 percentage points. On $50K monthly revenue, that\'s $2,000-$3,500 in invisible loss.',
    chart: {
      type: 'two-column',
      data: [
        { label: 'Estimated', value: 28, color: '#111111' },
        { label: 'Actual', value: 34, color: '#E05252' },
      ],
      unit: '%',
    },
  },
  {
    type: 'cta',
    headline: 'Stop estimating. Start calculating.',
    ctaLine: 'foodcosting.app →',
  },
];

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="FoodCostTip"
        component={FoodCostTip}
        durationInFrames={750}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          hook: "Most restaurants lose money and don't know why",
          problem: "Your food cost % is probably too high",
          tipLines: [
            { label: "Fine dining", value: "28–32%" },
            { label: "Casual dining", value: "25–35%" },
            { label: "Fast food", value: "20–30%" },
          ],
          cta: "Calculate yours free at foodcosting.app",
          audioSrc: null,
          durationInFrames: 750,
        }}
      />
      <Composition
        id="Carousel"
        component={Carousel}
        durationInFrames={defaultCarouselSlides.length}
        fps={1}
        width={1080}
        height={1080}
        defaultProps={{
          slides: defaultCarouselSlides,
        }}
      />
    </>
  );
};
