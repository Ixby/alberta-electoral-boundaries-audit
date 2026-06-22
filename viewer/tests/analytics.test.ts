// Unit tests for the analytics SDK's pure bucketing helpers.
//
// Only the framework-free, deterministic helpers are tested here: scrollPctBucket,
// secondsBucket, and zoomBucket. The network side of the SDK (track / pageview /
// initEngagement / observeSections) is browser-only, fire-and-forget, and guarded
// by `if (!browser) return`, so it is not exercised in the node test environment —
// importing the module is enough to confirm it loads (and that PUBLIC_SUPABASE_URL
// resolves at module scope via the sveltekit() vitest plugin).

import { describe, it, expect } from 'vitest';
import { scrollPctBucket, secondsBucket, zoomBucket } from '../src/lib/analytics';

describe('scrollPctBucket', () => {
	it('returns 0 below the first milestone', () => {
		expect(scrollPctBucket(0)).toBe(0);
		expect(scrollPctBucket(24)).toBe(0);
	});

	it('floors to the highest crossed milestone (25 / 50 / 75 / 100)', () => {
		expect(scrollPctBucket(25)).toBe(25);
		expect(scrollPctBucket(49)).toBe(25);
		expect(scrollPctBucket(50)).toBe(50);
		expect(scrollPctBucket(74)).toBe(50);
		expect(scrollPctBucket(75)).toBe(75);
		expect(scrollPctBucket(99)).toBe(75);
		expect(scrollPctBucket(100)).toBe(100);
	});

	it('clamps anything past 100 to the 100 bucket', () => {
		expect(scrollPctBucket(140)).toBe(100);
	});
});

describe('secondsBucket', () => {
	it('returns 0 before the first threshold', () => {
		expect(secondsBucket(0)).toBe(0);
		expect(secondsBucket(4)).toBe(0);
	});

	it('floors to the largest threshold not exceeding s', () => {
		expect(secondsBucket(5)).toBe(5);
		expect(secondsBucket(14)).toBe(5);
		expect(secondsBucket(15)).toBe(15);
		expect(secondsBucket(29)).toBe(15);
		expect(secondsBucket(30)).toBe(30);
		expect(secondsBucket(59)).toBe(30);
		expect(secondsBucket(60)).toBe(60);
		expect(secondsBucket(119)).toBe(60);
		expect(secondsBucket(120)).toBe(120);
		expect(secondsBucket(299)).toBe(120);
		expect(secondsBucket(300)).toBe(300);
	});

	it('caps at the top threshold for very long sessions', () => {
		expect(secondsBucket(5000)).toBe(300);
	});
});

describe('zoomBucket', () => {
	it('maps tile levels 0–10 to coarse zoom labels', () => {
		expect(zoomBucket(0)).toBe('province');
		expect(zoomBucket(1)).toBe('province');
		expect(zoomBucket(2)).toBe('region');
		expect(zoomBucket(3)).toBe('region');
		expect(zoomBucket(4)).toBe('city');
		expect(zoomBucket(5)).toBe('city');
		expect(zoomBucket(6)).toBe('district');
		expect(zoomBucket(7)).toBe('district');
		expect(zoomBucket(8)).toBe('street');
		expect(zoomBucket(10)).toBe('street');
	});

	it('returns a non-empty label for every level', () => {
		for (let level = 0; level <= 10; level++) {
			expect(zoomBucket(level).length).toBeGreaterThan(0);
		}
	});
});
