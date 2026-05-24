// @ts-nocheck
// Alberta Electoral Boundary Audit — map onboarding modal
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Wired once at init time. Shown on first map-tool open, not on page load.
// The overlay's own Escape handler runs first (registered before this module)
// and returns early when the modal is visible — so this handler only fires
// when the overlay Escape has already stood down.

import { markIntroSeen } from '../prefs';

export function initIntroModal(): void {
  const modal    = document.getElementById('map-intro-modal');
  const closeBtn = document.getElementById('map-intro-close');
  if (!modal || !closeBtn) return;

  function _closeModal() {
    markIntroSeen();
    modal.style.display = 'none';
  }

  closeBtn.addEventListener('click', _closeModal);
  modal.addEventListener('click', function(e) { if (e.target === modal) _closeModal(); });

  // Registered AFTER the overlay's Escape handler so ordering is preserved:
  // overlay handler checks modal visibility and returns early → this handler fires.
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal.style.display !== 'none') _closeModal();
  });
}
