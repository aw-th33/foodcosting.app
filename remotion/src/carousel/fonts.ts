import { loadFont as loadIBMPlexMono } from '@remotion/google-fonts/IBMPlexMono';
import { loadFont as loadInter } from '@remotion/google-fonts/Inter';

loadIBMPlexMono('normal', {
  weights: ['400', '500', '700'],
  subsets: ['latin'],
});

loadInter('normal', {
  weights: ['400', '600', '700', '800'],
  subsets: ['latin'],
});
