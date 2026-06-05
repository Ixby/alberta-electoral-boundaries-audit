// Pure tests for the ready-state helper. No DOM needed.
import { describe, it, expect } from 'vitest';
import { awaitReady, notifyReady } from '../src/lib/mapEngine/readyState';
import type { MapCtx } from '../src/lib/mapEngine/types';

function mkCtx(ready: boolean): MapCtx {
	return { ready, readyWaiters: [] } as unknown as MapCtx;
}

describe('awaitReady', () => {
	it('resolves immediately when ctx.ready is already true', async () => {
		const ctx = mkCtx(true);
		await expect(awaitReady(ctx)).resolves.toBeUndefined();
		expect(ctx.readyWaiters).toEqual([]);
	});

	it('resolves after notifyReady is called', async () => {
		const ctx = mkCtx(false);
		const promise = awaitReady(ctx, 5000);
		expect(ctx.readyWaiters.length).toBe(1);
		notifyReady(ctx);
		await expect(promise).resolves.toBeUndefined();
		expect(ctx.readyWaiters).toEqual([]);
	});

	it('rejects after timeout elapses without notifyReady', async () => {
		const ctx = mkCtx(false);
		await expect(awaitReady(ctx, 30)).rejects.toThrow(/not ready/);
	});

	it('cleans up its waiter on timeout (no leak)', async () => {
		const ctx = mkCtx(false);
		try { await awaitReady(ctx, 20); } catch (_) {}
		expect(ctx.readyWaiters).toEqual([]);
	});

	it('drains multiple concurrent waiters on a single notifyReady', async () => {
		const ctx = mkCtx(false);
		const p1 = awaitReady(ctx, 5000);
		const p2 = awaitReady(ctx, 5000);
		const p3 = awaitReady(ctx, 5000);
		expect(ctx.readyWaiters.length).toBe(3);
		notifyReady(ctx);
		await expect(Promise.all([p1, p2, p3])).resolves.toEqual([undefined, undefined, undefined]);
		expect(ctx.readyWaiters).toEqual([]);
	});

	it('notifyReady on an empty waiter list is a no-op', () => {
		const ctx = mkCtx(false);
		expect(() => notifyReady(ctx)).not.toThrow();
		expect(ctx.readyWaiters).toEqual([]);
	});

	it('a waiter that throws does not block other waiters', async () => {
		const ctx = mkCtx(false);
		const goodPromise = awaitReady(ctx, 5000);
		// Simulate a throwing waiter being pushed directly
		ctx.readyWaiters.unshift(() => { throw new Error('boom'); });
		notifyReady(ctx);
		await expect(goodPromise).resolves.toBeUndefined();
	});
});
