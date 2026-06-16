// Alberta Electoral Boundary Audit — map onboarding modal
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Owns every interaction with #map-intro-modal:
//   - initIntroModal()  — wires close button, backdrop click, Escape key
//   - maybeShowIntro()  — show on first overlay open (if user hasn't dismissed)
//   - showIntroNow()    — show unconditionally (used by the toolbar help button)
//   - hideIntro()       — hide without marking seen (used by overlay close)
//
// The overlay's own Escape handler runs first (registered before this module)
// and returns early when the modal is visible — so this Escape handler only
// fires when the overlay Escape has already stood down.
//
// Focus management: createFocusTrap (from a11y/focusTrap) is used imperatively
// to move focus in, trap Tab, and restore focus on close.

import { hasSeenIntro, markIntroSeen } from '../prefs';
import { createFocusTrap } from '../a11y/focusTrap';
import { DOM_IDS } from './domIds';

function _modal(): HTMLElement | null {
  return document.getElementById(DOM_IDS.mapIntroModal) as HTMLElement | null;
}

/** Active trap cleanup — null when the modal is hidden. */
let _trapCleanup: (() => void) | null = null;

function _activateTrap(modal: HTMLElement): void {
  if (_trapCleanup) return; // already active
  _trapCleanup = createFocusTrap(modal, _closeModal);
}

function _deactivateTrap(): void {
  if (_trapCleanup) {
    _trapCleanup();
    _trapCleanup = null;
  }
}

// Forward-declared so _activateTrap can reference it as onEscape.
let _closeModal: () => void = () => {};

export function initIntroModal(): void {
  const modal    = _modal();
  const closeBtn = document.getElementById(DOM_IDS.mapIntroClose);
  if (!modal || !closeBtn) return;

  _closeModal = function close() {
    markIntroSeen();
    _deactivateTrap();
    modal.style.display = 'none';
  };

  closeBtn.addEventListener('click', _closeModal);
  modal.addEventListener('click', function(e) { if (e.target === modal) _closeModal(); });

  // Toolbar help button: re-open the modal unconditionally.
  const helpBtn = document.getElementById(DOM_IDS.tbHelpBtn);
  if (helpBtn) helpBtn.addEventListener('click', showIntroNow);
}

export async function maybeShowIntro(): Promise<void> {
  if (await hasSeenIntro()) return;
  const modal = _modal();
  if (!modal) return;
  modal.style.display = 'flex';
  _activateTrap(modal);
}

export function showIntroNow(): void {
  const modal = _modal();
  if (!modal) return;
  modal.style.display = 'flex';
  _activateTrap(modal);
}

export function hideIntro(): void {
  const modal = _modal();
  if (!modal) return;
  _deactivateTrap();
  modal.style.display = 'none';
}
