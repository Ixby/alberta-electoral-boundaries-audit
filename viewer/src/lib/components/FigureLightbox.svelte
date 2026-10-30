<!--
  Alberta Electoral Boundary Audit — figure lightbox
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  Any <figure><img> on the page opens here when clicked: pinch, drag, wheel,
  double-tap and keyboard pan/zoom ($lib/panZoom). An image's data-full
  attribute (the vector SVG behind a WebP/JPEG render) is preferred, so deep
  zoom stays sharp and the SVG loads only on demand. One delegated listener,
  so figures added later (language switch, client navigation) work too.
-->
<script lang="ts">
	import { onMount } from 'svelte';
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
	import { attachPanZoom } from '$lib/panZoom';

	let lb: HTMLDivElement;
	let lbImg: HTMLImageElement;
	let closeBtn: HTMLButtonElement;

	onMount(() => {
		let prevFocus: Element | null = null;
		const pz = attachPanZoom(lb, lbImg);

		function open(img: HTMLImageElement) {
			pz.reset();
			lbImg.src = img.dataset.full ?? img.currentSrc ?? img.src;
			lbImg.alt = img.alt;
			lb.style.display = 'flex';
			prevFocus = document.activeElement;
			lb.focus();
		}
		function close() {
			lb.style.display = 'none';
			pz.reset();
			if (prevFocus instanceof HTMLElement) prevFocus.focus();
			prevFocus = null;
		}

		const onDocClick = (e: MouseEvent) => {
			const img = (e.target as Element | null)?.closest?.('figure img');
			if (img instanceof HTMLImageElement) open(img);
		};
		// A tap on the dark backdrop closes. A tap on the image does not (it may be
		// the first half of a double-tap zoom), and neither does the end of a drag.
		const onLbClick = (e: MouseEvent) => {
			if (e.target === lb && !pz.wasDrag() && !pz.onTarget(e.clientX, e.clientY)) close();
		};
		const onKey = (e: KeyboardEvent) => {
			if (e.key === 'Escape') close();
			if (e.key === 'Tab') {
				e.preventDefault();
				closeBtn.focus();
			}
		};

		document.addEventListener('click', onDocClick);
		lb.addEventListener('click', onLbClick);
		lb.addEventListener('keydown', onKey);
		closeBtn.addEventListener('click', close);
		return () => {
			pz.destroy();
			document.removeEventListener('click', onDocClick);
			lb.removeEventListener('click', onLbClick);
			lb.removeEventListener('keydown', onKey);
			closeBtn.removeEventListener('click', close);
		};
	});
</script>

<div id="fig-lightbox" bind:this={lb} role="dialog" aria-modal="true" aria-label={t(lang.current, 'chrome.lightbox.fig_aria')} tabindex="-1">
	<button id="fig-lightbox-close" bind:this={closeBtn} aria-label={t(lang.current, 'chrome.lightbox.fig_close_aria')}>&times;</button>
	<img id="fig-lightbox-img" bind:this={lbImg} alt="" />
</div>

<style>
	:global(figure img) {
		cursor: zoom-in;
	}
	#fig-lightbox {
		position: fixed;
		inset: 0;
		/* Above the site header (z 9100). */
		z-index: 9800;
		background: rgba(0, 0, 0, 0.9);
		display: none;
		align-items: center;
		justify-content: center;
		cursor: default;
		touch-action: none;
		overflow: hidden;
	}
	#fig-lightbox:focus {
		outline: none;
	}
	#fig-lightbox-close {
		position: absolute;
		top: 12px;
		inset-inline-end: 16px;
		background: rgba(255, 255, 255, 0.12);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: #fff;
		font-size: 1.4rem;
		line-height: 1;
		width: 36px;
		height: 36px;
		border-radius: 50%;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1;
	}
	#fig-lightbox-close:hover {
		background: rgba(255, 255, 255, 0.22);
	}
	#fig-lightbox img {
		max-width: 92vw;
		max-height: 92dvh;
		object-fit: contain;
		border-radius: 4px;
		box-shadow: 0 0 60px rgba(0, 0, 0, 0.6);
		/* panZoom maps screen points through this origin — keep it centred. */
		transform-origin: center center;
		pointer-events: none;
		user-select: none;
		-webkit-user-drag: none;
	}
</style>
